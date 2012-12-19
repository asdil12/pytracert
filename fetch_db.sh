#!/bin/bash

cd database

# geoIP
mkdir -p geoip
cd geoip
test -e country-ipv4.dat || wget http://www.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz -O - | gzip -d > country-ipv4.dat
test -e country-ipv6.dat || wget http://www.maxmind.com/download/geoip/database/GeoIPv6.dat.gz -O - | gzip -d > country-ipv6.dat
test -e city-ipv4.dat || wget http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.xz -O - | xz -d > city-ipv4.dat
test -e city-ipv6.dat || wget http://www.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz -O - | gzip -d > city-ipv6.dat
cd ..


# OpenGeoDB (KFZ)
mkdir opengeodb
cd opengeodb
for country in AT BE CH DE LI ; do
	wget -c http://fa-technik.adfc.de/code/opengeodb/$country.tab
done
cd ..
