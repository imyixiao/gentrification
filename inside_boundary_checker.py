'''
input: lat, lng, shp file
output: boolean, true if in boundary, false if not in boundary

cite code from 
https://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile

us nation shape file: https://www.census.gov/geo/maps-data/data/cbf/cbf_nation.html
'''

import fiona
import shapely

def inside_boundary_checker(shp_file_path, lat, lng):
    with fiona.open(shp_file_path) as fiona_collection:
        # In this case, we'll assume the shapefile only has one record/layer (e.g., the shapefile
        # is just for the borders of a single country, etc.).
        shapefile_record = fiona_collection.next()
        # Use Shapely to create the polygon
        shape = shapely.geometry.asShape( shapefile_record['geometry'] )
        #create box to fast filter out data
        minx, miny, maxx, maxy = shape.bounds
        bounding_box = shapely.geometry.box(minx, miny, maxx, maxy)
        #create point
        point = shapely.geometry.Point(lat, lng) # longitude, latitude

        if bounding_box.contains(point) is False:
            return False
        else:
            if shape.contains(point):
                return True
            else:
                return False


if __name__ == '__main__':
    shp_file_path = '../data/cb_2017_us_nation_5m.shp'
    #restaurant 1, in canada 
    print("restaurant in canada :" + "true" if inside_boundary_checker(shp_file_path,49.246292, -123.116226) else "false")
    #restaurant 2, in us
    print("restaurant in u.s :" + "true" if inside_boundary_checker(shp_file_path,36.778259, -119.417931) else "false")
    #restaurant 3, in mexican 
    print("restaurant in mexican :" + "true" if inside_boundary_checker(shp_file_path,19.42847, -99.12766) else "false")