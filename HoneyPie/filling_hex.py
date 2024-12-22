import HoneyPie.direction as direction


def check_neighbours_one_hex(gdf, index_gdf, buf = 120):
    list_point = []
    #gdf = gdf.to_crs('EPSG:32636')
    vacant_points = gdf.loc[gdf.index != index_gdf].copy().reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf.loc[index_gdf, 'geometry'].buffer(buf)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    return list_point

# the last variant
def define_first_func_zone(gdf, func_zone, func_zone_count, WIND_DIRECTION, centre_territory):
    gdf_vacant = gdf[gdf['func_zone'] == 'not_defined']
    index_gdf = gdf_vacant[gdf_vacant['score_' + str(func_zone)] == gdf_vacant['score_' + str(func_zone)].max()].index
    for i in index_gdf:
        gdf_vacant.loc[i, 'direction'] = direction.Points.point_direction(centre_territory,gdf.loc[i, 'geometry'].centroid)
    try: 
        grouped_values = gdf_vacant.loc[index_gdf].groupby('direction').count()
        func = direction.direction_choosing_hex[grouped_values.loc[grouped_values[grouped_values['geometry'] == grouped_values['geometry'].max()].index].reset_index().loc[0, 'direction']]
    except KeyError:
        func = direction.direction_choosing_hex[WIND_DIRECTION]
    if len(index_gdf) <= func_zone_count:
        gdf.loc[index_gdf, 'func_zone'] = func_zone
    else:

        gdf.loc[func(gdf_vacant), 'func_zone'] = func_zone
    return(gdf, func)

def check_neighbours_func_zone(gdf, func_zone):
    list_point = []
    vacant_points = gdf[gdf['func_zone'] == 'not_defined'].reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf[gdf['func_zone'] == func_zone].union_all().buffer(120)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    return list_point


def set_func_zone(gdf, func_zone, total_area, func, number):
    for area in range(total_area//number):
        count_hex = len(gdf[gdf['func_zone'] == func_zone])
        list_neighbours = check_neighbours_func_zone(gdf, func_zone)
        if total_area > count_hex:
            gdf.loc[func(gdf.loc[list_neighbours]), 'func_zone'] = func_zone
            count_hex += 1
    return gdf

# good function
def check_neighbours(gdf, landuse, buf = 120):
    list_point = []
    gdf = gdf.to_crs('EPSG:32636')
    vacant_points = gdf[gdf['landuse'] == 'not_defined'].reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf[gdf['landuse'] == landuse].union_all().buffer(buf)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    return list_point

def check_neighbours_personal(gdf, index_gdf, buf = 120):
    list_point = []
    gdf = gdf.to_crs('EPSG:32636')
    vacant_points = gdf.copy().reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf.loc[index_gdf].union_all().buffer(buf)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    return list_point



# fill functional zones
def check_neighbours_func_zone(gdf, func_zone):
    list_point = []
    #gdf = gdf[gdf['landuse'] == landuse]
    gdf = gdf.to_crs('EPSG:32636')
    vacant_points = gdf[gdf['func_zone'] == 'not_defined'].reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf[gdf['func_zone'] == func_zone].union_all().buffer(120)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    return list_point


def set_func_zone(gdf, func_zone, total_area, func, number):
    for area in range(total_area//number):
        count_hex = len(gdf[gdf['func_zone'] == func_zone])
        list_neighbours = check_neighbours_func_zone(gdf, func_zone)
        if total_area > count_hex:
            gdf.loc[func(gdf.loc[list_neighbours]), 'func_zone'] = func_zone
            count_hex += 1
    return gdf



# mark hex in the territory
def invasion(gdf, gdf_neighbour, ind,soc,mid,low,cot,gar,par,grb): # gdf_neighbour - layer with the extant territory, gdf - layer with territory hex
    list_point = []
    gdf = gdf.to_crs('EPSG:32636')
    gdf_neighbour = gdf_neighbour.to_crs('EPSG:32636')
    vacant_points = gdf[gdf['func_zone'] == 'not_defined'].reset_index()
    if len(vacant_points) != 0:
        vacant_points['geometry'] = vacant_points['geometry'].centroid
        unioned_polygon = gdf_neighbour.union_all().buffer(500)
        for point_index in range(len(vacant_points)):
            if unioned_polygon.contains(vacant_points['geometry'][point_index]):
                list_point.append(vacant_points.loc[point_index, 'index'])
    gdf.loc[list_point,'score_industrial'] += ind
    gdf.loc[list_point,'score_social'] += soc
    gdf.loc[list_point,'score_middle_living'] += mid
    gdf.loc[list_point,'score_low_living'] += low
    gdf.loc[list_point,'score_cottage_living'] += cot
    gdf.loc[list_point,'score_garden'] += gar
    gdf.loc[list_point,'score_park'] += par
    gdf.loc[list_point,'score_green_buffer'] += grb
    gdf['score_living'] = gdf['score_middle_living'] + gdf['score_low_living'] + gdf['score_cottage_living']
    return gdf