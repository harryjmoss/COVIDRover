import geopandas as gpd
import fiona, os

def get_geo_dataframe_from_url(geo_url):
    geo_df=gpd.read_file(geo_url)
    return geo_df

def get_geomap_path():
    geopath="data/geofiles/geofile.shp"
    #geopath="data/geofile.geojson"
    if not(os.path.exists(geopath)):
        print("Getting geographical information...")
        geo_url="https://opendata.arcgis.com/datasets/a8531598f29f44e7ad455abb6bf59c60_0.geojson"
        geo_dataframe=get_geo_dataframe_from_url(geo_url)
        geo_dataframe=geo_dataframe[['lad19cd','geometry']]
        geo_dataframe.columns=['Area code','geometry']  
        geo_dataframe.to_file(geopath)
    return geopath
if __name__ == '__main__':
    get_geomap_path()
