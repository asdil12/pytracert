#!/usr/bin/python2

from traceroute import Traceroute
import dnsgeo
import sys

def print_callback(ttl, payload):
	if payload:
		curr_host = "%(hostname)s (%(ip)s)" % payload
		print "%d\t%s" % (ttl, curr_host)
		print "\t",
		print dnsgeo.lookup(**payload)
	else:
		print "%d\t*" % ttl

if __name__ == "__main__":
	t = Traceroute(timeout=1)
	t.set_callback(print_callback)
	t.run(target=sys.argv[1])
