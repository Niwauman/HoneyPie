import pandas as pd
import geopandas as gpd
from shapely import LineString
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # ignore deprecation warning - GH pysal/spaghetti#649
import spaghetti
import pulp
from spopt.locate import LSCP



class SocialObjectsLocation:
    # LOCATION social_objects

    # Creation a variant of road graph. Will be used in LSCP

    def create_graph(gdf, LOCAL_CRS):
        lines_dict = pd.DataFrame(columns = ['name','geometry']) 
        num =0
        points_gdf = gdf.copy()
        points_gdf['geometry'] = points_gdf['geometry'].centroid
        for i in range(len(gdf)):
            list_point = []
            neighbours_point = points_gdf[points_gdf.geometry.within(gdf.loc[i, 'geometry'].buffer(120))].reset_index()
            point_start = gdf.geometry[i].centroid
            for p in range(len(neighbours_point)):
                point_end = neighbours_point.loc[p, 'geometry']
                lines_dict.loc[num, 'geometry'] = LineString([point_start, point_end])
                num += 1
        gdf_line = gpd.GeoDataFrame(lines_dict, geometry='geometry', crs = LOCAL_CRS)
        gdf_line.reset_index(inplace=True)
        return gdf_line    

    def network_contruction(gdf, LOCAL_CRS):
        lines_dict = pd.DataFrame(columns = ['name','geometry']) 
        num =0
        points_gdf = gdf.copy()
        points_gdf['geometry'] = points_gdf['geometry'].centroid
        for i in range(len(gdf)):
            list_point = []
            neighbours_point = points_gdf[points_gdf.geometry.within(gdf.loc[i, 'geometry'].buffer(120))].reset_index()
            point_start = gdf.geometry[i].centroid
            for p in range(len(neighbours_point)):
                point_end = neighbours_point.loc[p, 'geometry']
                lines_dict.loc[num, 'geometry'] = LineString([point_start, point_end])
                num += 1
        gdf_line = gpd.GeoDataFrame(lines_dict, geometry='geometry', crs = LOCAL_CRS)
        gdf_line.reset_index(inplace=True)
        #ntw_file = create_graph(hex_territory[hex_territory['population'] > 0].reset_index())
        #ntw_file = gpd.read_file('streets_plan.geojson')
        ntw_file = gdf_line
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
    # ignore deprecation warning - GH pysal/libpysal#468
        ntw = spaghetti.Network(in_data=ntw_file)
        streets = spaghetti.element_as_gdf(ntw, arcs=True)

        streets_buffered = gpd.GeoDataFrame(
            gpd.GeoSeries(streets["geometry"].buffer(0.2).unary_union),
            crs=streets.crs,
            columns=["geometry"],
        )
        return(ntw)
    
    
    def school(gdf, ntw, LOCAL_CRS):
        solver = pulp.PULP_CBC_CMD(keepFiles=True, msg=False)
        SERVICE_RADIUS_SCHOOL = 500
        client_points = gdf[gdf['population'] > 0].copy().to_crs(LOCAL_CRS)
        client_points['geometry'] = client_points['geometry'].centroid
        client_points = client_points.reset_index()
        facility_points = client_points.copy()
        facility_points['capacity_school'] = 550
        facility_points['capacity_kindergarten'] = 200

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        # ignore deprecation warning - GH pysal/libpysal#468
        ntw.snapobservations(client_points, "clients", attribute=True)
        clients_snapped = spaghetti.element_as_gdf(ntw, pp_name="clients", snapped=True)
        clients_snapped.drop(columns=["id", "comp_label"], inplace=True)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        # ignore deprecation warning - GH pysal/libpysal#468
        ntw.snapobservations(facility_points, "facilities", attribute=True)
        facilities_snapped = spaghetti.element_as_gdf(ntw, pp_name="facilities", snapped=True)
        facilities_snapped.drop(columns=["id", "comp_label"], inplace=True)


        cost_matrix = ntw.allneighbordistances(
            sourcepattern=ntw.pointpatterns["clients"],
            destpattern=ntw.pointpatterns["facilities"],
        )
        school = LSCP.from_cost_matrix(
        cost_matrix,
        SERVICE_RADIUS_SCHOOL,
        demand_quantity_arr=client_points["population_teens"],
        facility_capacity_arr=facility_points["capacity_school"],
        name="schools"
        )

        school = school.solve(solver)

        selected_indices = school.cli2fac
        selected_indices = str(selected_indices).replace(']', '').replace('[', '').split(', ')
        schools_places = []
        for item in selected_indices:
            item = int(item)
            if item not in schools_places:
                schools_places.append(item)

        gdf.loc[facility_points.loc[schools_places, 'index'].to_list(), 'landuse'] = 'social'
        gdf.loc[facility_points.loc[schools_places, 'index'].to_list(), 'func_zone'] = 'school'
        gdf.loc[facility_points.loc[schools_places, 'index'].to_list(), 'population'] = 0
        return(gdf)
    

    def kindergarten(gdf, ntw, LOCAL_CRS):
        solver = pulp.PULP_CBC_CMD(keepFiles=True, msg=False)
        SERVICE_RADIUS_KINDERGARTEN = 500
        client_points = gdf[gdf['population'] > 0].copy().to_crs(LOCAL_CRS)
        client_points['geometry'] = client_points['geometry'].centroid
        client_points = client_points.reset_index()
        facility_points = client_points.copy()
        facility_points['capacity_school'] = 550
        facility_points['capacity_kindergarten'] = 200

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        # ignore deprecation warning - GH pysal/libpysal#468
        ntw.snapobservations(client_points, "clients", attribute=True)
        clients_snapped = spaghetti.element_as_gdf(ntw, pp_name="clients", snapped=True)
        clients_snapped.drop(columns=["id", "comp_label"], inplace=True)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        # ignore deprecation warning - GH pysal/libpysal#468
        ntw.snapobservations(facility_points, "facilities", attribute=True)
        facilities_snapped = spaghetti.element_as_gdf(ntw, pp_name="facilities", snapped=True)
        facilities_snapped.drop(columns=["id", "comp_label"], inplace=True)


        cost_matrix = ntw.allneighbordistances(
            sourcepattern=ntw.pointpatterns["clients"],
            destpattern=ntw.pointpatterns["facilities"],
        )
        #kindergartens
        kindergarten = LSCP.from_cost_matrix(
            cost_matrix,
            SERVICE_RADIUS_KINDERGARTEN,
            demand_quantity_arr=client_points["population_schildren"],
            facility_capacity_arr=facility_points["capacity_kindergarten"],
            name="kindergartens"
        )

        kindergarten = kindergarten.solve(solver)
        selected_indices = kindergarten.cli2fac
        selected_indices = str(selected_indices).replace(']', '').replace('[', '').split(', ')
        kindergarten_places = []
        for item in selected_indices:
            item = int(item)
            if item not in kindergarten_places:
                kindergarten_places.append(item)

        gdf.loc[facility_points.loc[kindergarten_places, 'index'].to_list(), 'landuse'] = 'social'
        gdf.loc[facility_points.loc[kindergarten_places, 'index'].to_list(), 'func_zone'] = 'kindergarten'
        gdf.loc[facility_points.loc[kindergarten_places, 'index'].to_list(), 'population'] = 0
        return(gdf)