#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: Tenge1-3-56.cr2.%CITY3.content-core.net

city: FRA, NBG,...

abroad:

network: ge5-1.cr1.ams2.nl.content-core.net

"""

class ContentCore(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\d\.content-core\.net$")
	applre_ext = re.compile(r".*\.(\w*)\d\.(\w*)\.content-core\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = ContentCore.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				returninfo['company'] = 'IP Exchange GmbH'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/ipexchange.json'))
					c = jsondb[city_code.upper()]
					returninfo['country'] = c['country']
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
				except:
					pass
				return returninfo
			else:
				match = ContentCore.applre_ext.match(hostname)
				if match:
					city_code, country_code = match.group(1,2)
					returninfo = base.returninfo.copy()
					country = base.get_country_by_iso(country_code)
					returninfo['country'] = country['name']
					returninfo['accuracy'] = 'country'
					returninfo['lat'] = country['lat']
					returninfo['lng'] = country['lng']
					returninfo['company'] = 'IP Exchange GmbH'
					returninfo['info'] = 'carrier'
					try:
						jsondb = json.load(open('./database/ipexchange.json'))
						key = "%s-%s" % (country_code.upper(), city_code.upper())
						c = jsondb[key]
						returninfo['city'] = c['city']
						returninfo['accuracy'] = 'city'
						returninfo['lat'] = c['lat']
						returninfo['lng'] = c['lng']
					except:
						pass
					return returninfo
		raise exceptions.NotApplicable()
