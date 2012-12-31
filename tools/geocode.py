#!/usr/bin/python2

import urllib2
import simplejson as json
import sys

if len(sys.argv) > 2:
	key = sys.argv[1]
	query = " ".join(sys.argv[2:])
else:
	query = sys.argv[1]

j = urllib2.urlopen("http://nominatim.openstreetmap.org/search?q=%s&format=json&addressdetails=1&limit=1&accept-language=en" % query.replace(' ', '+')).read()
try:
	c = json.loads(j)
	c = c[0]
	a = c['address']

	try:
		city = a['city']
	except:
		city = query.split(',')[0]

	#cityk = city.replace(' ', '')
	try:
		print '"'+key+'":'+json.dumps({
			'city': city,
			'country_code': a['country_code'].upper(),
			'country': a['country'],
			'lat': float(c['lat']),
			'lng': float(c['lon'])
		})+","
	except NameError:
		pass

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
