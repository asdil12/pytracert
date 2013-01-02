#!/usr/bin/python2

import sys
import gtk.gdk
gtk.gdk.threads_init()
import gobject
import threading

import osmgpsmap

from traceroute import Traceroute
import georesolve

print "using library: %s (version %s)" % (osmgpsmap.__file__, osmgpsmap.__version__)


class UI(gtk.Window):
	def __init__(self):
		self.trace_thread = None
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

		self.set_default_size(800, 600)
		self.old_height = 0
		self.connect("check-resize", self.on_window_resize)
		self.connect('destroy', lambda x: gtk.main_quit())
		self.set_title('PYTrace')

		if 0:
			self.osm = DummyMapNoGpsPoint()
		else:
			self.osm = osmgpsmap.GpsMap()
		self.osm.layer_add(
					osmgpsmap.GpsMapOsd(
						show_dpad=True,
						show_zoom=True))


		self.osm.connect('button_release_event', self.map_clicked)

		#connect keyboard shortcuts
		self.osm.set_keyboard_shortcut(osmgpsmap.KEY_FULLSCREEN, gtk.gdk.keyval_from_name("F11"))
		self.osm.set_keyboard_shortcut(osmgpsmap.KEY_UP, gtk.gdk.keyval_from_name("Up"))
		self.osm.set_keyboard_shortcut(osmgpsmap.KEY_DOWN, gtk.gdk.keyval_from_name("Down"))
		self.osm.set_keyboard_shortcut(osmgpsmap.KEY_LEFT, gtk.gdk.keyval_from_name("Left"))
		self.osm.set_keyboard_shortcut(osmgpsmap.KEY_RIGHT, gtk.gdk.keyval_from_name("Right"))

		#connect to tooltip
		self.show_tooltips = False
		self.osm.props.has_tooltip = True
		self.osm.connect("query-tooltip", self.on_query_tooltip)


		self.vbox = gtk.VBox(False, 0)
		self.add(self.vbox)

		self.vp = gtk.VPaned()
		self.vbox.pack_start(self.vp, True, True)


		self.vp.add1(self.osm)

		vb2 = gtk.VBox(False, 0)
		self.vp.add2(vb2)

		# begin control ui
		self.target_entry = gtk.Entry()
		self.target_entry.connect("activate", self.trace_initiated)

		self.tr_button = gtk.Button('Trace')
		self.tr_button.connect("clicked", self.trace_initiated)

		hbox = gtk.HBox(False, 0)
		hbox.pack_start(self.target_entry)
		hbox.pack_start(self.tr_button, False)
		vb2.pack_start(hbox, False)
		# end control ui

		self.tb = gtk.TextBuffer()
		self.tv = gtk.TextView()
		self.tv.set_buffer(self.tb)
		self.tv.set_property('editable', False)
		
		vb2.pack_start(self.tv, True, True)


	def on_query_tooltip(self, widget, x, y, keyboard_tip, tooltip, data=None):
		if keyboard_tip:
			return False

		if self.show_tooltips:
			p = osmgpsmap.point_new_degrees(0.0, 0.0)
			self.osm.convert_screen_to_geographic(x, y, p)
			lat,lon = p.get_degrees()
			tooltip.set_markup("%+.4f, %+.4f" % p.get_degrees())
			return True

		return False
	
	def on_window_resize(self, window):
		height = self.vp.get_allocation()[3]
		if height != self.old_height:
			self.old_height = height
			self.vp.set_position(int(self.vp.get_allocation()[3] * 0.8))

	def trace_callback(self, ttl, payload):
		payload_p = "%(hostname)s (%(ip)s)" % payload if payload else '*'
		print "%s\t%s" % (ttl, payload_p)
		self.tb.insert_at_cursor("%s\t%s\n" % (ttl, payload_p))
		if payload:
			res = georesolve.lookup(**payload)
			if georesolve.ACCURACY[res['accuracy']] > georesolve.ACCURACY['none']:
				print "\t",
				print res
				lat = res['lat']
				lng = res['lng']
				self.osm.gps_add(lat, lng, heading=osmgpsmap.INVALID);

	def trace_initiated(self, button):
		def _trace_thread(target, cb):
			self.tr_button.set_label('Stop')
			self.tb.set_text('')
			try:
				print "thread run"
				t = Traceroute()
				t.set_callback(cb)
				self.osm.gps_clear()
				t.run(target)
				print "thread exit"
			finally:
				self.tr_button.set_label('Trace')
		print "thread ready"
		#FIXME: only launch when not already running
		self.trace_thread = threading.Thread(target=_trace_thread, args=(self.target_entry.get_text(), self.trace_callback))
		self.trace_thread.start()
		print "thread launched"

	def map_clicked(self, osm, event):
		lat,lon = self.osm.get_event_location(event).get_degrees()
		print (lat,lon)
		#if event.button == 1:
		#	self.latlon_entry.set_text(
		#		'Map Centre: latitude %s longitude %s' % (
		#			self.osm.props.latitude,
		#			self.osm.props.longitude
		#		)
		#	)
		if event.button == 2:
			self.osm.gps_add(lat, lon, heading=osmgpsmap.INVALID);
		elif event.button == 3:
			pb = gtk.gdk.pixbuf_new_from_file_at_size ("poi.png", 24,24)
			self.osm.image_add(lat,lon,pb)


if __name__ == "__main__":
	u = UI()
	u.show_all()
	gtk.gdk.threads_enter()
	if len(sys.argv) > 1:
		u.target_entry.set_text(sys.argv[1])
		u.target_entry.activate()
	gtk.main()
	gtk.gdk.threads_leave()
