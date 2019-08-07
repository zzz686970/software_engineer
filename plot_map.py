import folium

colors = {
	'A': 'red',
	'B': 'blue'
}
map_osm = folium.Map(location =[40.742, -73.956], zoom_start = 11)
train_df.apply(lambda row: folium.CircleMarker(location=[row['lat'], row['lon']],
                                               radius = 10,
                                               fill_color = colors[row['class']],
                                               popup=row['class'])
			.add_to(map_osm), axis=1)



## another way
from folium.features import DivIcon
colors = {
	'A': 'red',
	'B': 'blue'
}
map_osm = folium.Map(location =[40.742, -73.956], zoom_start = 11)
for _, row in df.iterrows():
	folium.CircleMarker(location=[row['lat'], row['lon']],
                        radius = 10,
                       	fill_color = colors[row['class']])
					 	.add_to(map_osm)

	folium.Marker(locations=[row['lat'], row['lon']],
	              icon = DivIcon(icon_size=(150, 36), icon_anchor=(0,0),
	                             htmp='<div style="font-size: 16pt; color: {}">{}</div>'.format(colors[row['class']], row['class'])))
				.add_to(map_osm)


## fast way
import dask.dataframe as dd, geoviews as gv, cartopy.crs as crs
from colorcet import fire
from holoviews.operation.datashader import datashade
from geoviews.tile_sources import CartoLight
gv.extension('bokeh')

tiles = CartoLight.options(width=700, height=600, xaxis=None, yaxis=None, show_grid=False)
taxi = dd.read_parquet('../data/nyc_taxi.parq').persist()
pts = gv.Points(taxi, ['pickup_x', 'pickup_y'], crs = crs.GOOGLE_MERCATOR)
trips = datashade(pts, cmap=fire, width=1000, height=600, x_sampling=0.5 y_sampling=0.5)
tiles * trips
