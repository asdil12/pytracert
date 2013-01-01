#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: te0-0-0-11.mpd21.jfk02.atlas.cogentco.com
                          CTY

"""

class CogentCO(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.([a-z]*)\d+\.atlas\.cogentco\.com$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = CogentCO.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				returninfo['company'] = 'Cogent Communications, Inc.'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/cogentco.json'))
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
