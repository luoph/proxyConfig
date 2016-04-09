#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Update hosts for *nix
Author: luopeihuan@gmail.com
Version: 0.0.1
Date: 2016-03-02
'''

import string
import sys
import urllib2
import re
from os.path import expanduser

# HOSTS_SOURCE = "http://freedom.txthinking.com/hosts"
HOSTS_SOURCE = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
SEARCH_STRING = "# Modified hosts start"

SURGE_WITHOUT_HOST = expanduser("~") + "/Library/Mobile Documents/iCloud~run~surge/Documents/nohost.conf"
SURGE_WITH_HOST = expanduser("~") + "/Library/Mobile Documents/iCloud~run~surge/Documents/hosts.conf"

def GetRemoteHosts(url):
    f = urllib2.urlopen(url, timeout=5)
    hosts = [line for line in f]
    f.close()
    return hosts


def main():
    try:
        hosts = GetRemoteHosts(HOSTS_SOURCE)
    except IOError:
        print "Could't connect to %s. Try again." % HOSTS_SOURCE
        sys.exit(1)

    surge_conf_file = open(SURGE_WITHOUT_HOST, 'r')
    surge_conf = surge_conf_file.read()

    surgeHosts = ""
    start = False
    for line in hosts:
        ip = ""
        domain = ""
        if start:
            if (not line.startswith('#')) and (not line.startswith('\n')):
                ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                if len(ip) > 0:
                    ip_len = len(ip[0])
                    domain = line[ip_len:].strip()
                else:
                    surgeHosts += line

                if ip[0] and domain:
                    new_item = domain + ' = ' + ip[0] + '\n';
                    surgeHosts += new_item
                else:
                    surgeHosts += line
            else:
                surgeHosts += line

        elif line.startswith(SEARCH_STRING):
            surgeHosts += line
            start = True

    surge_conf += surgeHosts

    fp = open(SURGE_WITH_HOST, "w")
    fp.write(surge_conf)
    fp.close()

    print "Success"


if __name__ == "__main__":
    main()
