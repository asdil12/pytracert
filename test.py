#!/usr/bin/python2

import dnsgeo
import sys

if len(sys.argv) > 1:
	print dnsgeo.lookup(hostname=sys.argv[1])
	exit(0)


testdomains = [
	"bt-sa1-i.BT.DE.NET.DTAG.DE",
	"xe-10-1-0.bar1.Munich1.Level3.net",
	"er1.ams1.nl.above.net",
	"Tenge1-3-56.cr2.FRA3.content-core.net",
	"ge5-1.cr1.ams2.nl.content-core.net",
	"xr-bay1-te1-1.x-win.dfn.de",
	"xe-1-1-0.rt-decix-1.m-online.net",
	"decix2.superkabel.de",
]

print

for domain in testdomains:
	print "%s: " % domain
	print dnsgeo.lookup(hostname=domain)
	print
