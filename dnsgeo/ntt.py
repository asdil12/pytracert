#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: frnkge03.de.bb.gin.ntt.net

also seen ce insted of bb...

"""

class NTT(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\d\d\.(\w*)\.\w\w\.gin\.ntt\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = NTT.applre.match(hostname)
			if match:
				city_code, country_code = match.group(1,2)
				returninfo = base.returninfo.copy()
				country = base.get_country_by_iso(country_code)
				returninfo['country'] = country['name']
				returninfo['accuracy'] = 'country'
				returninfo['lat'] = country['lat']
				returninfo['lng'] = country['lng']
				returninfo['company'] = 'Nippon Telegraph and Telephone'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/carriers/ntt.json'))
					c = jsondb[city_code.upper()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
