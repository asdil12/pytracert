#!/usr/bin/python2

import base
import exceptions

import re

"""
network: %CITY-foo.%CITY.%COUNTRY.NET.DTAG.DE

city equals the number plate in germany

"""

class DTag(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\.(\w*)\.NET\.DTAG\.DE$")

	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = DTag.applre.match(hostname)
			if match:
				city_code, country_code = match.group(1,2)
				returninfo = base.returninfo.copy()
				country = base.get_country_by_iso(country_code)
				returninfo['country'] = country['name']
				returninfo['lat'] = country['lat']
				returninfo['lng'] = country['lng']
				returninfo['company'] = 'Deutsche Telekom AG'
				returninfo['info'] = 'carrier'
				# try city
				returninfo['city'] = city_code
				if country_code.upper() in base.get_available_opengeodbs():
					try:
						city = base.get_city_by_plate(country_code, city_code)
						returninfo['city'] = city['name']
						returninfo['lat'] = city['lat']
						returninfo['lng'] = city['lng']
					except:
						pass
				return returninfo
		raise exceptions.NotApplicable()
