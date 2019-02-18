'''
input: lat, lng, shp file
output: boolean, true if in boundary, false if not in boundary

cite code from 
https://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile

us nation shape file: https://www.census.gov/geo/maps-data/data/cbf/cbf_nation.html

for using fiona, could create a new environment 
conda create -n test_fiona python=3.5 fiona --yes -c conda-forge #change to your python version
source activate test_fiona
'''

import fiona
import shapely
from shapely import geometry


def inside_boundary_checker(shp_file_path, lat, lng):
    with fiona.open(shp_file_path) as fiona_collection:
        # In this case, we'll assume the shapefile only has one record/layer (e.g., the shapefile
        # is just for the borders of a single country, etc.).
        shapefile_record = next(iter(fiona_collection))
        # Use Shapely to create the polygon
        shape = shapely.geometry.asShape( shapefile_record['geometry'] )
        print(type(shape))
        if type(shape) is shapely.geometry.multipolygon.MultiPolygonAdapter:
            raise ValueError('multiple polygons have been created!')
        #create box to fast filter out data
        minx, miny, maxx, maxy = shape.bounds
        print("minx:" + str(minx) + ", miny:"+ str(miny) + ", maxx:" + str(maxx) + ", maxy" + str(maxy))
        bounding_box = shapely.geometry.box(minx, miny, maxx, maxy)
        #create point
        point = shapely.geometry.Point(lat, lng) # longitude, latitude

        if bounding_box.contains(point) is False:
            print("outside the box")
            return False
        else:
            if shape.contains(point):
                print("in the shape")
                return True
            else:
                print("outside the shape")
                return False


def us_lower48_checker(lat, lng, zip):
    # http://en.wikipedia.org/wiki/Extreme_points_of_the_United_States#Westernmost
    #https://gist.github.com/jsundram/1251783
    top = 49.3457868 # north lat
    left = -124.7844079 # west long
    right = -66.9513812 # east long
    bottom =  24.7433195 # south lat
    if bottom <= lat <= top and left <= lng <= right and len(zip) == 5 and zip.isdigit():
        return True
    return False


if __name__ == '__main__':
    shp_file_path = './data/cb_2017_us_nation_5m/cb_2017_us_nation_5m.shp'

    #restaurant 1, in canada 
    print("restaurant in canada :" + ("true" if us_lower48_checker(43.651070, -79.347015) else  "false"))
    #restaurant 2, in us
    print("restaurant in u.s :" + ("true" if us_lower48_checker(42.3012621, -83.7171617) else  "false"))
    #restaurant 3, in mexican 
    print("restaurant in mexican :" + ("true" if us_lower48_checker(19.42847, -99.12766) else  "false"))
    
    