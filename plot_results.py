import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from scipy import interpolate

#import cluster_analysis
#cluster_analysis.cluster_analysis()

min_lon = -3.93455628
min_lat = 40.25387182
max_lon = -3.31993445
max_lat = 40.57085727

lats=np.arange(min_lat,max_lat,0.001)
lons=np.arange(min_lon,max_lon,0.001)
lons_grid, lats_grid = np.meshgrid(lons,lats)

ref_grid = np.zeros((np.size(lats_grid), 2))
ref_grid[:, 0] = np.ravel(lats_grid)
ref_grid[:, 1] = np.ravel(lons_grid)

pointdata=pd.read_csv('madrid_poi_clusters.csv')

values = np.array(pointdata['cluster_id'])
points = np.array([pointdata['lat'],pointdata['lon']])

data = interpolate.griddata(points.T, values, ref_grid, method = 'nearest')

data=np.reshape(data,np.shape(lats_grid))
data = data.astype('float32')

map = Basemap(llcrnrlon=min_lon,llcrnrlat=min_lat,urcrnrlon=max_lon,urcrnrlat=max_lat, resolution = 'h', epsg=2062)

map.arcgisimage(service='World_Shaded_Relief', xpixels = 3000, verbose= True, zorder=1)

map.readshapefile('/home/Earth/mfalls/Downloads/gadm36_ESP_4', '') # map of Madrid municipal boundries

map_min_lon,map_min_lat = map(min_lon, min_lat)
map_max_lon,map_max_lat = map(max_lon, max_lat)

x = np.linspace(0, map.urcrnrx, data.shape[1])  # the mesh must be plotted using the maps own coords, not geographical ones
y = np.linspace(0, map.urcrnry, data.shape[0])

xx, yy = np.meshgrid(x, y)

# pxs = []
# pys = []
#
# for p in range(len(pointdata.index)):
#     px,py = map(pointdata['lon'][p], pointdata['lat'][p])
#     pxs.append(px)
#     pys.append(py)
#     map.plot(px, py, marker='.', color='r',markersize=0.1,zorder=3)   # how do these appear on the map?

px,py = map(np.array(pointdata['lon']), np.array(pointdata['lat']))
map.scatter(px, py, marker='.', color='r',s=0.1,zorder=3)

map.pcolormesh(xx, yy, data,zorder=2,alpha=0.2)

plt.show()

plt.savefig('madrid_poi_clusters.png')

