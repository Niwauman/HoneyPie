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