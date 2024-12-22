import math

class ChoosingHex:
    def choose_north_west(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        gdf = gdf[gdf['geometry'].centroid.y >= gdf['geometry'].centroid.y.quantile(q = 0.90)]
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.min()].index
        return index

    def choose_north(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        index = gdf[gdf['geometry'].centroid.centroid.y == gdf['geometry'].centroid.y.max()].index
        return index

    def choose_north_east(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        gdf = gdf[gdf['geometry'].centroid.y >= gdf['geometry'].centroid.y.quantile(q = 0.90)]
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.max()].index
        return index

    def choose_east(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.max()].index
        return index

    def choose_south_east(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        gdf = gdf[gdf['geometry'].centroid.y <= gdf['geometry'].centroid.y.quantile(q = 0.10)]
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.max()].index
        return index

    def choose_south(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        index = gdf[gdf['geometry'].centroid.y == gdf['geometry'].centroid.y.min()].index
        return index

    def choose_south_west(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        gdf = gdf[gdf['geometry'].centroid.y <= gdf['geometry'].centroid.y.quantile(q = 0.10)]
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.min()].index
        return index

    def choose_west(gdf):
        gdf = gdf[gdf['landuse'] == 'not_defined']
        index = gdf[gdf['geometry'].centroid.x == gdf['geometry'].centroid.x.min()].index
        return index
    

class ChoosingHexFunczone:
    def choose_north_west(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        gdf = gdf[gdf['geometry_point'].y >= gdf['geometry_point'].y.quantile(q = 0.90)]
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.min()].index
        return index

    def choose_north(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        index = gdf[gdf['geometry_point'].y == gdf['geometry_point'].y.max()].index
        return index

    def choose_north_east(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        gdf = gdf[gdf['geometry_point'].y >= gdf['geometry_point'].y.quantile(q = 0.90)]
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.max()].index
        return index

    def choose_east(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.max()].index
        return index

    def choose_south_east(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        gdf = gdf[gdf['geometry_point'].y <= gdf['geometry_point'].y.quantile(q = 0.10)]
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.max()].index
        return index

    def choose_south(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        index = gdf[gdf['geometry_point'].y == gdf['geometry_point'].y.min()].index
        return index

    def choose_south_west(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        gdf = gdf[gdf['geometry_point'].y <= gdf['geometry_point'].y.quantile(q = 0.10)]
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.min()].index
        return index

    def choose_west(gdf):
        gdf = gdf[gdf['func_zone'] == 'not_defined']
        index = gdf[gdf['geometry_point'].x == gdf['geometry_point'].x.min()].index
        return index
    
class Points:
    def point_direction(point_1, point_2): # point_1 - start point_2 - end
        delta_x = point_2.x - point_1.x
        delta_y = point_2.y - point_1.y
        rymb = abs(math.atan((point_1.x - point_2.x) / (point_1.y - point_2.y))*60)
        if delta_x < 0 and delta_y < 0:
            angle = rymb + 180
        elif delta_x < 0 and delta_y >= 0:
            angle = 360 - rymb
        elif delta_x >= 0 and delta_y < 0:
            angle = 180 - rymb
        else: angle = rymb

        if angle > 360:
            angle -= 360

        if angle >= 337.5 and angle < 22.5:
            direction = 'north'
        elif angle >= 22.5 and angle < 67.5:
            direction = 'north_east'
        elif angle >= 67.5 and angle < 112.5:
            direction = 'east'
        elif angle >= 112.5 and angle < 157.5:
            direction = 'south_east'
        elif angle >= 157.5 and angle < 202.5:
            direction = 'south'
        elif angle >= 202.5 and angle < 247.5:
            direction = 'south_west'
        elif angle >= 247.5 and angle < 292.5:
            direction = 'west'
        elif angle >= 292.5 and angle < 337.5:
            direction = 'north_west'
        else: 
            direction = 'north'
        return(direction)