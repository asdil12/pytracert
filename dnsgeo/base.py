#!/usr/bin/python2

import exceptions

import simplejson as json
import os
import csv

returninfo = {
	'lat': None,
	'lng': None,
	'city': None,
	'state': None,
	'country': None,
	'company': None,
	'info': None # carrier/dialin...
}

class DNSGeoBase:
	# 0-100 - defines order of checking
	# 0 = disabled
	priority = 0

	def __init__(self):
		self.initialized = False

	def _initialize(self):
		self.initialized = True
	
	def lookup(self, ip=None, hostname=None):
		raise exceptions.NotApplicable()
		if not self.initialized: self._inizialize()
		return returninfo


# helpers

def get_country_by_iso(isocode):
	"""
		param: ISO-3166-1 Alpha-2 country code
		returns: {name, lat, lng}
	"""
	isodb = json.load(open('./database/iso3166-1.json'))
	c = isodb[isocode.upper()]
	return {
		'name': c[2],
		'lat': c[0],
		'lng': c[1]
	}

def get_state_by_code(isocode, state_code):
	"""
		param: ISO-3166-1 Alpha-2 country code, state_code in format common for country
		returns: {name, lat, lng}
	"""
	statedb = json.load(open('./database/states/%s.json' % isocode.lower()))
	c = statedb[state_code.upper()]
	return {
		'name': c[2],
		'lat': c[0],
		'lng': c[1]
	}

def get_available_opengeodbs():
	"""
		returns: [DE, AT...]
	"""
	return [s.replace('.tab', '') for s in os.listdir('./database/opengeodb')]

def get_city_by_plate(isocode, city_code):
	"""
		param: iso country code, number plate prefix
		returns: {name, lat, lng}
	"""
	city_code = city_code.upper()
	csvfile = open("./database/opengeodb/%s.tab" % isocode.upper(), 'r')
	csvdb= csv.reader(csvfile, delimiter='	')
	#loc_id ags ascii   name    lat lon amt plz vorwahl einwohner   flaeche kz  typ level   of  invalid
	for e in csvdb:
		if e[11] == city_code:
			return {
				'name': e[3],
				'lat': float(e[4]),
				'lng': float(e[5])
			}

