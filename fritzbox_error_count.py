#!/usr/bin/env python3
"""
  fritzbox_errors - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_username [fritzbox username]
  env.fritzbox_password [fritzbox password]

  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""
import json
import os
import sys
import fritzbox_helper as fh

PAGE = "docInfo"
USAGE = ["nonCorrErrors", "corrErrors"]


def get_errors():
    """get error counts"""

    server = os.environ["fritzbox_ip"]
    username = os.environ["fritzbox_username"]
    password = os.environ["fritzbox_password"]

    session_id = fh.get_session_id(server, username, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)

    for docsis in data['data']['channelDs']:
        sums = {}

        for status in data['data']['channelDs'][docsis]:
            for k in USAGE:
                if k in status:
                    key = docsis + k
                    if key not in sums:
                        sums[key] = 0
                    sums[key] += status[k]

        for k in sums:
            print("%s.value %s" % (k, sums[k]))


def print_config():
    print("graph_title AVM Fritz!Box Errors")
    print("graph_vlabel errors")
    print("graph_args -r --lower-limit 0")
    print("graph_category system")
    print("graph_info This graph shows correctable and non-correctable errors.")
    print("graph_scale no")

    print("docsis30nonCorrErrors.label DOCSIS 3.0 Non-correctable errors")
    print("docsis30nonCorrErrors.type DERIVE")
    print("docsis30nonCorrErrors.graph LINE1")
    print("docsis30nonCorrErrors.min 0")
    print("docsis30nonCorrErrors.max 10000")

    print("docsis30corrErrors.label DOCSIS 3.0 Correctable errors")
    print("docsis30corrErrors.type DERIVE")
    print("docsis30corrErrors.graph LINE1")
    print("docsis30corrErrors.min 0")
    print("docsis30corrErrors.max 10000")

    print("docsis31nonCorrErrors.label DOCSIS 3.1 Non-correctable errors")
    print("docsis31nonCorrErrors.type DERIVE")
    print("docsis31nonCorrErrors.graph LINE1")
    print("docsis31nonCorrErrors.min 0")
    print("docsis31nonCorrErrors.max 10000")

    print("docsis31corrErrors.label DOCSIS 3.1 Correctable errors")
    print("docsis31corrErrors.type DERIVE")
    print("docsis31corrErrors.graph LINE1")
    print("docsis31corrErrors.min 0")
    print("docsis31corrErrors.max 10000")

    if os.environ.get("host_name"):
        print("host_name " + os.environ["host_name"])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "config":
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == "autoconf":
        print("yes")
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "fetch":
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_errors()
        except:
            import traceback
            traceback.print_exc()
            sys.exit("Couldn't retrieve fritzbox errors")
