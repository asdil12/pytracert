#!/usr/bin/python2

import base
import exceptions

import simplejson as json
import re

class DECIX(base.DNSGeoBase):
	priority = 20
	applre = re.compile(r"de-?cix", re.I)
	applre_num = re.compile(r"de-?cix-?(\d)", re.I)
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = DECIX.applre.search(hostname)
			if match:
				returninfo = base.returninfo.copy()
				returninfo['country'] = 'Germany'
				returninfo['city'] = 'Frankfurt'
				returninfo['info'] = 'exchange'
				returninfo['lat'] = 50.12128335
				returninfo['lng'] = 8.661885971
				returninfo['company'] = 'DE-CIX Management GmbH'
				# try to get street
				match = DECIX.applre_num.search(hostname)
				if match:
					decix_code = match.group(1)
					try:
						jsondb = json.load(open('./database/decix.json'))
						c = jsondb[decix_code]
						returninfo['lat'] = c['lat']
						returninfo['lng'] = c['lng']
					except:
						pass
				return returninfo
		raise exceptions.NotApplicable()
