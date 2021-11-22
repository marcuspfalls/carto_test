# carto_test
Package for technical test for Carto job application. 

Contains:
* cluster_analysis.py - Python module that obtains and reads the POI data, filters out those outside of the Madrid domain and within 150m of a cinema and uses a spectral analysis to sort the remaining POIs into 5 categories. Outputs a .csv file, madrid_poi_clusters.csv that contains the latitude, longitude, point_id and cluster_id. 
* cluster_analysis.ipynb - Jupyter notebook containing the same code as cluster_analysis, with each code block annotated with explanations. 
* plot_results.ipynb - Jupyter notebook that reads madrid_poi_clusters.csv, and uses its contents to perform nearest-point interpolation to define the 5 zones of each cluster. It then plots these zones over a map of Madrid. Each code block is also annotated. 
* 208862-7650164-ocio_salas.csv - Contains the information of the cinemas of the City of Madrid. Obtained from https://datos.madrid.es/portal/site/egob/
