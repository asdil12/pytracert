#!/usr/bin/python2

import dnsgeo

ACCURACY = {
	'none':    0,
	'country': 1,
	'state':   2,
	'city':    3,
	'site':    4
}

def lookup(ip, hostname):
	return dnsgeo.lookup(ip=ip, hostname=hostname)

