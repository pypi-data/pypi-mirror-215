# -*- coding: utf-8 -*-
# Copyright (C) 2014 the2nd <the2nd@otpme.org>
# Distributed under the terms of the GNU General Public License v2
import os
import atexit

try:
    if os.environ['OTPME_DEBUG_MODULE_LOADING'] == "True":
        print(_("Loading module: %s") % __name__)
except:
    pass

from otpme.lib import stuff
from otpme.lib import config
from otpme.lib import multiprocessing
from otpme.lib.classes.agent_conn import AgentConn

from otpme.lib.exceptions import *

logger = config.logger

connections = {}

REGISTER_BEFORE = []
REGISTER_AFTER = []

def register():
    register_config()

def register_config():
    """ Register config stuff. """
    # Use session from otpme-agent to connect to daemons.
    config.register_config_var("use_agent", None, "auto")

def atfork():
    """ Make sure we close connections on fork. """
    global connections
    connections.clear()

def cleanup():
    """ Cleanup on process/daemon shutdown. """
    close_connections()

def close_connections(proc_id=None):
    """ Close all connections. """
    global connections
    for x_proc_id in dict(connections):
        if proc_id is not None:
            if x_proc_id == proc_id:
                continue
        for daemon in dict(connections[x_proc_id]):
            for key in dict(connections[x_proc_id][daemon]):
                conn = connections[x_proc_id][daemon][key]
                if not conn.connected:
                    continue
                #msg = "Closing connection: %s" % conn
                #logger.debug(msg)
                try:
                    conn.close()
                except Exception as e:
                    msg = ("Failed to close connection: %s: %s"
                            % (conn, e))
                    logger.warning(msg)
                connections[x_proc_id][daemon].pop(key)
atexit.register(close_connections)

def add_connection(proc_id, daemon, key, connection):
    """ Add connection to dict. """
    global connections
    if not proc_id in connections:
        connections[proc_id] = {}
    if not daemon in connections[proc_id]:
        connections[proc_id][daemon] = {}
    connections[proc_id][daemon][key] = connection

def get(daemon, **kwargs):
    """ Get connection to OTPme daemons. """
    from otpme.lib.protocols.otpme_client import OTPmeClient
    global connections

    kwargs['daemon'] = daemon
    try:
        realm = kwargs['realm']
    except:
        realm = None
        kwargs['realm'] = realm
    try:
        site = kwargs['site']
    except:
        site = None
        kwargs['site'] = site
    try:
        use_agent = kwargs['use_agent']
    except:
        use_agent = None
    try:
        use_ssh_agent = kwargs['use_ssh_agent']
    except:
        # FIXME: implement use_ssh_agent="auto"!!!!!!
        use_ssh_agent = False
        kwargs['use_ssh_agent'] = use_ssh_agent
    try:
        use_smartcard = kwargs['use_smartcard']
    except:
        use_smartcard = "auto"
        kwargs['use_smartcard'] = use_smartcard
    try:
        user = kwargs['user']
    except:
        user = None
        kwargs['user'] = user
    try:
        username = kwargs['username']
    except:
        username = None
        kwargs['username'] = username
    try:
        password = kwargs['password']
    except:
        password = None
        kwargs['password'] = password
    try:
        aes_pass = kwargs['aes_pass']
    except:
        aes_pass = None
        kwargs['aes_pass'] = aes_pass
    try:
        socket_uri = kwargs['socket_uri']
    except:
        socket_uri = None
        kwargs['socket_uri'] = socket_uri
    try:
        autoconnect = kwargs['autoconnect']
    except:
        autoconnect = True
        kwargs['autoconnect'] = autoconnect
    try:
        timeout = kwargs['timeout']
    except:
        timeout = config.connection_timeout
        kwargs['timeout'] = timeout
    try:
        connect_timeout = kwargs['connect_timeout']
    except:
        connect_timeout = config.connect_timeout
        kwargs['connect_timeout'] = connect_timeout
    try:
        interactive = kwargs['interactive']
    except:
        interactive = None
        kwargs['interactive'] = interactive
    try:
        login_session_id = kwargs['login_session_id']
    except:
        login_session_id = None
        kwargs['login_session_id'] = login_session_id
    try:
        print_messages = kwargs['print_messages']
    except:
        print_messages = None
        kwargs['print_messages'] = print_messages

    conn_kwargs = dict(kwargs)

    # Generate key from func/method name and args.
    arguments = {
                'args'      : (),
                'kwargs'    : conn_kwargs,
                }
    try:
        conn_key = stuff.args_to_hash(arguments)
    except Exception as e:
        config.raise_exception()
        msg = ("Failed to parse function args.")
        raise OTPmeException(msg)

    # Get job ID.
    proc_id = multiprocessing.get_id()

    try:
        conn = connections[proc_id][daemon][conn_key]
    except:
        conn = None
    if conn is not None:
        if conn.connected:
            try:
                status, \
                status_code, \
                reply = conn.send("ping", timeout=3)
            except Exception as e:
                reply = ""

            if daemon != "agent":
                if not conn.print_messages \
                and isinstance(reply, list):
                    reply = reply[-1]

            if reply == "pong":
                return conn
        connections[proc_id][daemon].pop(conn_key)

    # Handle agent connections.
    if daemon == "agent":
        try:
            user = kwargs['user']
        except:
            user = None
            kwargs['user'] = user
        logger.debug("Trying to get agent connection...")
        # Try to get agent connection
        try:
            agent_conn = AgentConn(user=user,
                            autoconnect=autoconnect,
                            login_session_id=login_session_id)
        except Exception as e:
            msg = (_("Error getting agent connection: %s") % e)
            raise OTPmeException(msg)
        add_connection(proc_id, daemon, conn_key, agent_conn)
        return agent_conn

    # Connections to syncd work independently of the agent
    if daemon == "syncd":
        use_agent = False
    # Connections to authd work independently of the agent
    if daemon == "authd":
        use_agent = False
    # Connections to hostd work independently of the agent
    if daemon == "hostd":
        use_agent = False
    # Connections to clusterd work independently of the agent
    if daemon == "clusterd":
        use_agent = False

    agent_user = None
    if interactive is None:
        if config.daemon_mode:
            interactive = False
        else:
            interactive = True
    conn_kwargs['interactive'] = interactive

    # FIXME: Currently we only use an agent for connections in our own realm.
    #        Maybe we should extend it to other realms too but it may not be a
    #        good idea to let otpme-agent send an SOTP or any other auth data
    #        to an other realm....
    if use_agent is None:
        if realm and realm != config.realm:
            if config.use_agent and not config.use_api:
                logger.warning("Cannot use agent connection for other realms.")
            use_agent = False
        else:
            use_agent = config.use_agent

    agent_user = None
    if interactive is None:
        if config.daemon_mode:
            interactive = False
        else:
            interactive = True
    conn_kwargs['interactive'] = interactive

    # FIXME: Currently we only use an agent for connections in our own realm.
    #        Maybe we should extend it to other realms too but it may not be a
    #        good idea to let otpme-agent send an SOTP or any other auth data
    #        to an other realm....
    if use_agent is None:
        if realm and realm != config.realm:
            if config.use_agent and not config.use_api:
                logger.warning("Cannot use agent connection for other realms.")
            use_agent = False
        else:
            use_agent = config.use_agent
        # No agent in daemon mode.
        if config.daemon_mode:
            use_agent = False

    need_user = True
    if config.daemon_mode:
        need_user = False
    if daemon == "hostd":
        need_user = False
    if daemon == "syncd":
        need_user = False
    if daemon == "clusterd":
        need_user = False

    # Check if we should use a running agent
    if need_user:
        if not username:
            if not config.use_api and (use_agent or use_agent == "auto"):
                use_agent = False
                # Try to get username from running otpme-agent.
                try:
                    agent_user = stuff.get_agent_user()
                    use_agent = True
                except Exception as e:
                    if use_agent is True:
                        msg = (_("Error getting agent user: %s") % e)
                        raise Exception(msg)
                    else:
                        logger.debug(str(e))

        # Check which name to use as OTPme user
        if not username and not config.use_api:
            # If user was set via "-u" command line option use it
            if config.login_user:
                username = config.login_user
            else:
                # Else use already logged in user from agent if possible
                if agent_user:
                    username = agent_user
                    logger.debug("Using username '%s' got from agent as OTPme user."
                                % username)
                else:
                    # Set login user to system user as last resort
                    username = config.system_user()
                    logger.debug("Using current system user '%s' as OTPme user."
                                % username)
            if use_agent:
                # If selected user is not == agent user do not use agent
                # connection.
                if not agent_user or username != agent_user:
                    msg = ("User '%s' is not logged in. Not using agent "
                            "connection, trying normal authentication..."
                            % username)
                    #raise Exception(msg)
                    logger.info(msg)
                    use_agent = False

    # Connections to host daemon go via unix socket.
    if daemon == "hostd":
        conn_kwargs['use_ssl'] = False
        conn_kwargs['auto_auth'] = False
        conn_kwargs['auto_preauth'] = False
        conn_kwargs['local_socket'] = True
        conn_kwargs['handle_host_auth'] = False
        conn_kwargs['handle_user_auth'] = False

    # Set agent parameter.
    conn_kwargs['use_agent'] = use_agent
    # Set username.
    conn_kwargs['username'] = username

    # Get daemon connection.
    daemon_conn = OTPmeClient(**conn_kwargs)
    # Cache connection.
    add_connection(proc_id, daemon, conn_key, daemon_conn)

    return daemon_conn
