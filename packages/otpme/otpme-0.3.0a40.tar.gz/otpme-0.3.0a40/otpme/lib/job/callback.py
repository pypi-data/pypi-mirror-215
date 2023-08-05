# -*- coding: utf-8 -*-
# Copyright (C) 2014 the2nd <the2nd@otpme.org>
# Distributed under the terms of the GNU General Public License v2
import os
import sys
import functools

try:
    if os.environ['OTPME_DEBUG_MODULE_LOADING'] == "True":
        print(_("Loading module: %s") % __name__)
except:
    pass

from otpme.lib import stuff
from otpme.lib import config
from otpme.lib import multiprocessing
from otpme.lib.protocols.utils import ask
from otpme.lib.protocols.utils import sign
from otpme.lib.protocols.utils import scauth
from otpme.lib.protocols.utils import askpass
from otpme.lib.protocols.utils import sshauth
from otpme.lib.protocols.utils import encrypt
from otpme.lib.protocols.utils import decrypt
from otpme.lib.protocols.utils import auth_jwt
from otpme.lib.protocols.utils import send_msg
from otpme.lib.protocols.utils import dump_data
from otpme.lib.protocols.utils import gen_user_keys

from otpme.lib.exceptions import *

class JobCallback(object):
    """ Class to handle user messages from job child processes. """
    def __init__(self, job=None, uuid=None, api_mode=None):
        class FakeJob(object):
            def __init__(self, uuid=None, api_mode=True):
                self.uuid = uuid
                self.exit_info = {}
                self._caller = "API"
        if job:
            self.job = job
            if api_mode is None:
                self.api_mode = False
            else:
                self.api_mode = api_mode
            self.api_exception = None
        else:
            if api_mode is None:
                self.api_mode = True
            else:
                self.api_mode = api_mode
            self.api_exception = "Cannot callback in API mode!"
            self.job = FakeJob(uuid=uuid, api_mode=self.api_mode)
        # Indicates that there was a exception in the callback chain that
        # needs to stop the job.
        self._exception = None
        # Indicates that self.error() should always raise an exception.
        self.raise_exception = False
        # Indicates if this callback will send messages to its client.
        self.enabled = True
        # Will hold all (modified objects this callback was used. in.
        self.modified_objects = []
        # Get logger.
        self.logger = config.logger

    def add_modified_object(self, o):
        """ Add modified object to callback. """
        if o.oid in self.modified_objects:
            return
        self.modified_objects.append(o.oid)

    def write_modified_objects(self):
        """ Write objects modified by this callback. """
        from otpme.lib import cache
        #from otpme.lib import backend
        objects_written = []
        for object_id in list(self.modified_objects):
            o = cache.get_modified_object(object_id)
            cache.remove_modified_object(object_id)
            self.modified_objects.remove(object_id)
            if not o or not o._modified:
                continue
            msg = "Writing modified object (Job): %s" % o
            self.logger.debug(msg)
            o._write(callback=self)
            objects_written.append(o.oid.full_oid)
        return objects_written

    def handle_exception(method):
        """ Raise exception. """
        def wrapper(self, *args, **kwargs):
            # If there was a exception in our calling chain we have to raise it.
            if config.raise_exceptions:
                if self._exception:
                    raise self._exception
            return method(self, *args, **kwargs)

        # Update func/method.
        functools.update_wrapper(wrapper, method)
        if not hasattr(wrapper, '__wrapped__'):
            # Python 2.7
            wrapper.__wrapped__ = method

        return wrapper

    def exception(self, exception):
        """ Handle exceptions. """
        # We need to remember the exception and re-raise it each time the
        # callback is called. This way we should get a useful stacktrace.
        self._exception = exception
        raise exception

    def _gen_query_id(self):
        """ Generate query ID. """
        # Gen query ID.
        query_id = "callback:%s" % stuff.gen_secret()
        return query_id

    def _send(self, query, command=None, timeout=1):
        if command is None:
            command = "query"
        comm_handler = self.job.comm_queue.get_handler("callback")
        try:
            comm_handler.send(recipient="client",
                            command=command,
                            data=query,
                            timeout=timeout)
        except ExitOnSignal:
            self.job.stop()

    def _send_query(self, query_id, query, timeout=1):
        """ Send query to client and handle answer. """
        # Send query to client.
        self._send(query, timeout=timeout)
        # Receive answer
        comm_handler = self.job.comm_queue.get_handler("callback")
        try:
            sender, \
            answer_id, \
            answer = comm_handler.recv(sender="client")
        except ExitOnSignal:
            self.job.stop()
            answer_id = None
        if answer_id != query_id:
            msg = "Received wrong answer ID: %s <> %s" % (query_id, answer_id)
            raise OTPmeException(msg)
        # Wait for answer from peer.
        if self.job.check_timeout():
            # Do some cleanup.
            multiprocessing.cleanup()
            #os._exit(0)
            sys.exit(0)
        # FIXME: Converting from string to type() leads to some "reserved"
        #        strings (True, False and None) because they are converted
        #        to the corresponding python types. This means that e.g. a
        #        password that is just the string "False" will fail.
        # Convert string to type().
        reply = stuff.string_to_type(answer)

        return reply

    def send(self, message='\0OTPME_NULL\0', error=False,
        command=None, timeout=1, ignore_escaping=False):
        """ Send message to user. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            return message
        # In API mode we have to print the given message.
        if self.api_mode:
            print(message)
            return
        # No need to add message for API/RAPI calls.
        if self.job._caller != "CLIENT":
            return message
        if message == '\0OTPME_NULL\0':
            return True
        # Send message.
        _message = (True, message)
        if error:
            _message = (False, message)
        if ignore_escaping:
            query = dump_data(job_id=self.job.uuid, message=_message)
        else:
            query = send_msg(job_id=self.job.uuid, message=_message)
        self._send(query, command=command, timeout=timeout)
        return True

    @handle_exception
    def ok(self, message='\0OTPME_NULL\0', timeout=1):
        """ Return given message or just True. """
        if message != '\0OTPME_NULL\0':
            if self.job._caller == "CLIENT":
                return self.send(message, timeout=timeout)
            # For API/RAPI calls we have to set the return value.
            if self.job._caller == "RAPI":
                self.job.return_value = message
                return True
            return message
        return True

    @handle_exception
    def abort(self, message='\0OTPME_NULL\0', timeout=1):
        """ Return None and send 'message' if given. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            return None
        # For API/RAPI calls we do not have to send the abort message.
        if self.job._caller != "CLIENT":
            return None
        if message == '\0OTPME_NULL\0':
            return
        # Send message.
        self.send(message, timeout=timeout)
        return None

    @handle_exception
    def error(self, message='\0OTPME_NULL\0',
        raise_exception=None, exception=None, timeout=1):
        """ Send error message to user. """
        if self.enabled:
            if message != '\0OTPME_NULL\0':
                if self.job._caller == "CLIENT":
                    # Make sure message is string.
                    exit_info = str(message)
                    # Set jobs last error.
                    if len(exit_info) > 0:
                        try:
                            self.job.exit_info['last_error'] = exit_info
                        except Exception as e:
                            msg = ("Error updating jobs last error: %s" % e)
                            self.logger.critical(msg)

                    # Add the message to callback channel.
                    if not raise_exception:
                        try:
                            self.send(message, error=True, timeout=timeout)
                        except:
                            pass
                else:
                    # For API/RAPI calls we have to set the return value.
                    if self.job._caller != "CLIENT":
                        self.job.return_value = message

            # When enabled and not in API mode we will not raise any exception.
            if not self.api_mode:
                if raise_exception is None:
                    raise_exception = False

        if raise_exception is None:
            if self.raise_exception:
                raise_exception = True

        if raise_exception:
            # If we got no exception to raise use the default.
            if not exception:
                exception = Exception
            # Finally raise our exception.
            raise exception(message)

        # And return False which is useful for "return callback.error("Foo")"
        return False

    @handle_exception
    def ask(self, message, input_prefill=None, timeout=1):
        """ Send query to ask the user for some input. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Make sure message is string.
        message = str(message)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = ask(query_id=query_id,
                        input_prefill=input_prefill,
                        prompt=message)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def askpass(self, prompt, null_ok=False, timeout=1):
        """ Send query to ask the user for a password. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = askpass(query_id=query_id,
                                prompt=prompt,
                                null_ok=null_ok)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def sshauth(self, challenge, timeout=1):
        """ Send query to ask the user/client to authenticate via ssh key. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = sshauth(query_id, challenge)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def scauth(self, smartcard_type, smartcard_data, timeout=1):
        """
        Send query to ask the user/client to authenticate via
        smartcard (e.g. fido2 tokens).
        """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = scauth(query_id=query_id,
                    smartcard_type=smartcard_type,
                    smartcard_data=smartcard_data)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def auth_jwt(self, reason, challenge, timeout=1):
        """
        Send query to ask the user/client to get a JWT.
        """
        from otpme.lib import backend
        from otpme.lib import jwt as _jwt
        from otpme.lib.pki.cert import SSLCert
        from otpme.lib.encryption.rsa import RSAKey
        if not config.auth_token:
            msg = "Cannot do JWT auth without auth token."
            raise OTPmeException(msg)
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Get user.
        user = backend.get_object(uuid=config.auth_token.owner_uuid)
        # Build query string.
        query = auth_jwt(query_id=query_id,
                        username=user.name,
                        reason=reason,
                        challenge=challenge)
        # Send query.
        jwt = self._send_query(query_id, query, timeout=timeout)
        user_site = backend.get_object(uuid=user.site_uuid)
        site_cert = SSLCert(cert=user_site.cert)
        try:
            jwt_key = RSAKey(key=site_cert.public_key())
        except Exception as e:
            msg = (_("Unable to get public key of site "
                    "certificate: %s: %s") % (user.site, e))
            raise OTPmeException(msg)
        try:
            jwt_data = _jwt.decode(jwt=jwt,
                                   key=jwt_key,
                                   algorithm='RS256')
        except Exception:
            return False
        jwt_token = jwt_data['login_token']
        jwt_challenge = jwt_data['challenge']
        if jwt_challenge == challenge:
            if jwt_token == config.auth_token.uuid:
                return jwt_data
        return False

    @handle_exception
    def dump(self, message,  timeout=1):
        """ Dump some data on client site. """
        return self.send(message, timeout=timeout, ignore_escaping=True)

    @handle_exception
    def gen_user_keys(self, username,
        key_len=2048, stdin_pass=False, timeout=1):
        """ Send query to client to generate users privat/public keys. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = gen_user_keys(query_id,
                            username=username,
                            key_len=key_len,
                            stdin_pass=stdin_pass)
        # Send query.
        reply = self._send_query(query_id, query, timeout=timeout)
        return reply

    @handle_exception
    def sign(self, data, timeout=1):
        """ Send query to client to sign given data. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = sign(query_id, data=data)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def encrypt(self, data, use_rsa_key=True, timeout=1):
        """ Send query to client to encrypt given data. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = encrypt(query_id, use_rsa_key=use_rsa_key, data=data)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def decrypt(self, data, timeout=1):
        """ Send query to client to decrypt given data. """
        # If the callback is disabled we do not send anything to the client.
        if not self.enabled:
            raise OTPmeException(self.api_exception)
        if self.api_mode:
            raise OTPmeException(self.api_exception)
        # Gen query ID.
        query_id = self._gen_query_id()
        # Build query string.
        query = decrypt(query_id, data=data)
        # Send query.
        return self._send_query(query_id, query, timeout=timeout)

    @handle_exception
    def enable(self):
        """ Enable callback. """
        self.enabled = True

    @handle_exception
    def disable(self):
        """ Disable callback. """
        self.enabled = False

    @handle_exception
    def stop(self, status, message="", timeout=1,
        raise_exception=True, exception=None):
        """ Set exit code and message that should be sent to the user. """
        if message is None:
            message = ""
        # Make sure message is string.
        if self.job._caller == "CLIENT":
            message = str(message)

        # In API mode "message" is the Exception we have to raise when status=False.
        if self.api_mode or not self.enabled:
            if status is False and raise_exception:
                if not exception:
                    exception = OTPmeException
                raise exception(message)
        else:
            # Update jobs exit infos.
            try:
                self.job.exit_info['exit_status'] = status
                if len(message) > 0:
                    self.job.exit_info['exit_message'] = message
            except:
                pass

        # Wakeup mgmtd waiting for new job messages/queries.
        self.send(None, command="job_end", timeout=timeout)

        return status, message
