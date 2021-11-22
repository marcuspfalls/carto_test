### Obtains the data from Google Cloud, discards those that are outside of the Madrid domain and those 150m from a cinema. The cinema data is obtained from the 
### website of the ayuntamiento of Madrid. 

def cluster_analysis():

    #from google.cloud import bigquery
    import numpy as np
    import pandas as pd
    import geopy.distance
    import geopandas
    from shapely.geometry import Point, mapping
    from shapely.geometry.polygon import Polygon
    from sklearn.cluster import SpectralClustering

    # obtaining the data
    bqclient=bigquery.Client()
    table = bigquery.TableReference.from_string('carto-ps-bq-developers.data_test.osm_spain_pois')
    rows = bqclient.list_rows(table)
    spain_pois = rows.to_dataframe(create_bqstorage_client=True)
    # spain_pois.to_csv('spain_pois.csv')
    # spain_pois=pd.read_csv('spain_pois.csv')

    ## Discarding the points outside of the Madrid Region

    min_lon = -3.93455628
    min_lat = 40.25387182
    max_lon = -3.31993445
    max_lat = 40.57085727
    madrid_pois = spain_pois.loc[(spain_pois['lon'] >= min_lon) & (spain_pois['lon'] <= max_lon) &
                                 (spain_pois['lat'] >= min_lat) & (spain_pois['lat'] <= max_lat)]
    madrid_pois=madrid_pois.reset_index()
    
    ## Cinemas

    # obtained .csv from ayuntamiento of Madrid website 
    madrid_cinemas = pd.read_csv('208862-7650164-ocio_salas.csv',sep=';')

    # defined functions to convert the coordinates to km, using (min_lat,min_lon) as the origin. 
    def lat_to_m(mlat,lat,mlon):
        return geopy.distance.distance((mlon, lat), (mlon, mlat)).km
    def lon_to_m(mlon,lon,mlat):
        return geopy.distance.distance((lon, mlat), (mlon, mlat)).km
    vlat_to_m = np.vectorize(lat_to_m)
    vlon_to_m = np.vectorize(lon_to_m)

    madrid_pois['y_metres'] = vlat_to_m(min_lat, np.array(madrid_pois['lat']), min_lon)
    madrid_pois['x_metres'] = vlon_to_m(min_lon, np.array(madrid_pois['lon']), min_lat)
    madrid_cinemas['y_metres'] = vlat_to_m(min_lat, np.array(madrid_cinemas['LATITUD']), min_lon)
    madrid_cinemas['x_metres'] = vlon_to_m(min_lon, np.array(madrid_cinemas['LONGITUD']), min_lat)

    # Defining the region of Madrid that is less than 0.15kn from a cinema
    cinema_locs = geopandas.GeoSeries([Point(madrid_cinemas['y_metres'][i], madrid_cinemas['x_metres'][i]) for i in range(madrid_cinemas.shape[0])])
    cinema_buffer = cinema_locs.buffer(0.15)

    # Using numpy vectorize to discard the pois near cinemas
    madrid_pois['near_cinema'] = [0 for i in range(madrid_pois.shape[0])]

    def in_buffer(p):
        p = Point(madrid_pois['y_metres'][p], madrid_pois['x_metres'][p])
        for buff in cinema_buffer:
            if buff.contains(p):
                return 1

    vin_buffer = np.vectorize(in_buffer)
    madrid_pois['near_cinema'] = vin_buffer(range(madrid_pois.shape[0]))
    madrid_pois_nocinema = madrid_pois.loc[madrid_pois['near_cinema']!=1]

    # taking a 20000 sample
    madrid_pois_nocinema = madrid_pois_nocinema.sample(n=20000)

    ## performing the cluster analysis
    
    X = np.zeros((madrid_pois_nocinema.shape[0],2))
    X[:,0],X[:,1]  = np.array(madrid_pois_nocinema['lat']), np.array(madrid_pois_nocinema['lon'])
    model = SpectralClustering(n_clusters=5)
    yhat = model.fit_predict(X)

    out = pd.DataFrame({'lat':np.array(madrid_pois_nocinema['lat']),
                        'lon':np.array(madrid_pois_nocinema['lon']),
                        'point_id':np.array(madrid_pois_nocinema['id']),
                        'cluster_id':yhat})

    out.to_csv('madrid_poi_clusters.csv')

if __name__ == '__main__':
    cluster_analysis()
