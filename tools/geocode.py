#!/usr/bin/python2

import urllib2
import json
import sys

j = urllib2.urlopen("http://nominatim.openstreetmap.org/search?q=%s&format=json&addressdetails=1&limit=1&accept-language=en" % " ".join(sys.argv[1:]).replace(' ', '+')).read()
try:
	c = json.loads(j)
	c = c[0]
	a = c['address']

	try:
		city = a['city']
	except:
		city = sys.argv[1].split(',')[0]

	city = city.replace(' ', '')
	print '"'+sys.argv[1].split(',')[0]+'":'+json.dumps({
		'city': city,
		'country_code': a['country_code'].upper(),
		'country': a['country'],
		'lat': float(c['lat']),
		'lng': float(c['lon'])
	})+","

	print >> sys.stderr, {
		'city': city,
		'country_code': a['country_code'].upper(),
		'country': a['country'],
		'lat': float(c['lat']),
		'lng': float(c['lon'])
	}
except:
	print >> sys.stderr, "ERROR: %s" % ",".join(sys.argv[1:])
	print "ERROR: %s" % ",".join(sys.argv[1:])
