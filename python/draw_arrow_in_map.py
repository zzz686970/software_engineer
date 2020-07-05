import folium
import numpy as np
import pandas as pd
from collections import namedtuple

def get_bearing(p1, p2):
	"""return compass bearing from p1 to p2

	[description]

	Arguments:
		p1 {[type]} -- namedtuple with lat lon
		p2 {[type]} -- namedtuple with lat lon
	"""
	long_diff = np.radians(p2.lon - p1.lon)
	lat1 = np.radians(p1.lat)
	lat2 = np.radians(p2.lat)
	x = np.sin(long_diff) * np.cos(lat2)
	y = (np.cos(lat1) * np.sin(lat2)
		- (np.sin(lat1) * np.cos(lat2)
		* np.cos(long_diff)))
	bearing = np.degrees(np.arctan2(x, y))

	## adjust
	if bearing < 0:
		return bearing + 360

	return bearing

def get_arrows(locations, color = 'blue', size=6, n_arrows=3):
	"""get a list of placed and rotated arrows/markers

	[description]

	Arguments:
		locations {[type]} -- list of lists of lat lon that represent start and end

	Keyword Arguments:
		color {str} -- [description] (default: {'blue'})
		size {number} -- [description] (default: {6})
		n_arrows {number} -- number of arrows to create (default: {3})
	"""
	Point = namedtuple('Point', field_names=['lat', 'lon'])
	p1 = Point(locations[0][0], locations[0][1])
	p2 = Point(locations[1][0], locations[1][1])

	## gettting the rotation needed, subtracting 90 to account for marker's orientation
	rotation = get_bearing(p1, p2) - 90

	## get evenly space list of lats and lons
	arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)[1:n_arrows+1]
	arrow_lons = np.linspace(p1.lon, p2.lon, n_arrows + 2)[1:n_arrows+1]
	arrows = []

	for points in zip(arrow_lats, arrow_lons):
		arrows.append(folium.RegularPolygonMarker(location=points,
												  fill_color=color,
												  number_of_sides=3,
												  radius=size,
												  rotation=rotation))

	return arrows

center_lat = 41.257160
center_lon = -95.995102

lats = np.random.uniform(low=center_lat - .25, high = center_lat + .25, size=(2,))
lons = np.random.uniform(low=center_lon - .25, high = center_lon + .25, size=(2,))

p1, p2 = [lats[0], lons[0]], [lats[1], lons[1]]

map1 = folium.Map(location=[center_lat, center_lon], zoom_start = 10)
folium.Marker(location = p1, icon=folium.Icon(color='green')).add_to(map1)
folium.Marker(location = p2, icon=folium.Icon(color='red')).add_to(map1)

## lines to connect
folium.PolyLine(locations=[p1, p2], color = 'blue').add_to(map1)

arrows = get_arrows(locations=[p1, p2], n_arrows=3)
for arrow in arrows:
	arrow.add_to(map1)
map1.save('test.html')
