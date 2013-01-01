#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: ffm-b12-link.telia.net
         CTY

"""

class TeliaSonera(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r"^([a-z]*)-.*-link\.telia\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = TeliaSonera.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				returninfo['company'] = 'TeliaSonera International Carrier AB'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/carriers/telia.json'))
					c = jsondb[city_code.lower()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
					returninfo['country'] = c['country']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
