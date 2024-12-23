import HoneyPie.filling_hex as filling_hex
import HoneyPie.direction as direction

class TerritoryAssessment:
    def wind(gdf, WIND_DIRECTION):
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 100),'score_industrial'] += 1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 100),'score_middle_living'] += -1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 100),'score_low_living'] += -1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 100),'score_cottage_living'] += -1

        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 200),'score_green_buffer'] += 1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 200),'score_park'] += -1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 200),'score_middle_living'] += -1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 200),'score_low_living'] += -1
        gdf.loc[filling_hex.check_neighbours_personal(gdf, direction.wind_choosing_hex[WIND_DIRECTION](gdf), 200),'score_cottage_living'] += -1
        return(gdf)
    
    def sun(gdf):
        sun_east = gdf['geometry'].centroid.x >= gdf['geometry'].centroid.x.quantile(q = 0.80)
        sun_south = gdf['geometry'].centroid.y <= gdf['geometry'].centroid.y.quantile(q = 0.40)
        sun_west = gdf['geometry'].centroid.x <= gdf['geometry'].centroid.x.quantile(q = 0.10)
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_park'] += 1
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_garden'] += 1
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_social'] += 1
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_middle_living'] += 1
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_low_living'] += 1
        gdf.loc[gdf[sun_east | sun_south | sun_west].index, 'score_cottage_living'] += 1
        return(gdf)
    
    def exist_city(gdf, gdf_city):
        gdf = filling_hex.invasion(gdf, gdf_city[gdf_city['Floors'] >= 4], -1,1,1,0,0,1,1,1)
        gdf = filling_hex.invasion(gdf, gdf_city[gdf_city['Floors'] == 3], -1,1,0,1,1,1,1,1)
        gdf = filling_hex.invasion(gdf, gdf_city[gdf_city['Floors'] >= 2], -1,1,0,1,1,1,1,1)
        gdf = filling_hex.invasion(gdf, gdf_city[gdf_city['Floors'] >= 1], -1,0,0,0,1,1,1,1)
        return(gdf)
    

class TerritoryPlanner:
    def set_middle_living(gdf, hex_count, WIND_DIRECTION, centre): 
        gdf, func = filling_hex.define_first_func_zone(gdf, 'middle_living', hex_count['middle_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'middle_living', hex_count['middle_living'], func,1)
        gdf, func = filling_hex.define_first_func_zone(gdf, 'middle_living', hex_count['middle_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'middle_living', hex_count['middle_living'], func,1)
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'middle_living'].index, 300), 'score_industrial'] += -5
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'middle_living'].index), 'score_low_living'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'middle_living'].index, 300), 'score_park'] += 5
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'middle_living'].index), 'score_garden'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'middle_living'].index), 'score_green_buffer'] += 3
        return(gdf)
    
    def set_low_living(gdf, hex_count, WIND_DIRECTION, centre):
        gdf, func = filling_hex.define_first_func_zone(gdf, 'low_living', hex_count['low_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'low_living', hex_count['low_living'], func, 2)
        gdf, func = filling_hex.define_first_func_zone(gdf, 'low_living', hex_count['low_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'low_living', hex_count['low_living'], func, 2)
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'low_living'].index), 'score_industrial'] += -3
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'low_living'].index), 'score_cottage_living'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'low_living'].index), 'score_park'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'low_living'].index), 'score_garden'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'low_living'].index, 300), 'score_green_buffer'] += 2
        return(gdf)
    
    def set_cottage_living(gdf, hex_count, WIND_DIRECTION, centre):
        gdf, func = filling_hex.define_first_func_zone(gdf, 'cottage_living', hex_count['cottage_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'cottage_living', hex_count['cottage_living'], func, 2)
        gdf, func = filling_hex.define_first_func_zone(gdf, 'cottage_living', hex_count['cottage_living'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'cottage_living', hex_count['cottage_living'], func, 2)
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'cottage_living'].index), 'score_garden'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'cottage_living'].index), 'score_green_buffer'] += 2
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'cottage_living'].index), 'score_industrial'] += -3
        return(gdf)
    
    def set_industrial(gdf, hex_count, WIND_DIRECTION, centre):
        gdf, func = filling_hex.define_first_func_zone(gdf, 'industrial', hex_count['industrial'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'industrial', hex_count['industrial'], func,1)
        gdf.loc[filling_hex.check_neighbours_personal(gdf, gdf[gdf['func_zone'] == 'industrial'].index), 'score_green_buffer'] += 5
        return(gdf)

    def set_green_buffer(gdf, hex_count, WIND_DIRECTION, centre):
        gdf, func = filling_hex.define_first_func_zone(gdf, 'park', hex_count['recreation'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'green_buffer', hex_count['recreation'], func,4)
        gdf, func = filling_hex.define_first_func_zone(gdf, 'garden', hex_count['recreation'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'green_buffer', hex_count['recreation'], func,4)
        gdf, func = filling_hex.define_first_func_zone(gdf, 'green_buffer', hex_count['recreation'], WIND_DIRECTION, centre)
        gdf = filling_hex.set_func_zone(gdf, 'green_buffer', hex_count['recreation'], func,2)
        return(gdf)