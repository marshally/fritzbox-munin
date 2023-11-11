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
USAGE = ["channelDs", "channelUs"]


def get_power_levels():
    """get power levels"""

    server = os.environ["fritzbox_ip"]
    username = os.environ["fritzbox_username"]
    password = os.environ["fritzbox_password"]

    session_id = fh.get_session_id(server, username, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)

    for usage in USAGE:
        for docsis in data['data'][usage]:
            for channel in data['data'][usage][docsis]:
                print("%s%spower.value %s" % (usage, channel['channelID'], channel['powerLevel']))


def print_config():
    print("graph_title AVM Fritz!Box Channel Power Level")
    print("graph_vlabel dBmV")
    print("graph_args -r --lower-limit 0")
    print("graph_category system")
    print("graph_info This graph shows power level for each channel.")
    print("graph_scale no")

    for i in range(1, 33):
        name = "channelDs%spower" % (i)
        print("%s.label Channel %s Down Power Level (dBmV)" % (name, i))
        print("%s.type GAUGE" % name)
        print("%s.graph LINE1" % name)

    for i in range(5, 9):
        name = "channelUs%spower" % (i)
        print("%s.label Channel %s Up Power Level (dBmV)" % (name, i))
        print("%s.type GAUGE" % name)
        print("%s.graph LINE1" % name)

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
            get_power_levels()
        except:
            import traceback
            traceback.print_exc()
            sys.exit("Couldn't retrieve fritzbox channel power")
