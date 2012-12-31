#!/usr/bin/python2

import dnsgeo
import sys

if len(sys.argv) > 1:
	print dnsgeo.lookup(hostname=sys.argv[1])
	exit(0)


testdomains = [
	# isp's
	"hos-tr2.ex3k13.rz1.hetzner.de",
	"GW-NEFkom-FOO.142.nefkom.de",

	# carriers
	"bt-sa1-i.BT.DE.NET.DTAG.DE",
	"xe-10-1-0.bar1.Munich1.Level3.net",
	"er1.ams1.nl.above.net",
	"Tenge1-3-56.cr2.FRA3.content-core.net",
	"ge5-1.cr1.ams2.nl.content-core.net",
	"xr-bay1-te1-1.x-win.dfn.de",
	"xe-1-1-0.rt-decix-1.m-online.net",
	"decix2.superkabel.de",
	"ae-5.r21.frnkge03.de.bb.gin.ntt.net",
	"POS7-0.GW3.DEN4.ALTER.NET",
	"0.xe-2-3-0.BR3.CHI13.ALTER.NET",
	"te4-3.ccr01.phl03.atlas.cogentco.com",
	"sjo-bb1-link.telia.net",
	"prag-bb1-link.telia.net",
	"cr1.n54ny.ip.att.net",
	"te1-1.c321.f.de.plusline.net",
]

print

for domain in testdomains:
	print "%s: " % domain
	print dnsgeo.lookup(hostname=domain)
	print
