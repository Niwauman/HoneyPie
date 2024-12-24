import matplotlib.pyplot as plt

class StatsFuncZones:
    def calculate_zones(gdf):
            dict_stat = {}
            grouped_zones = gdf[['hex_id', 'func_zone']].groupby('func_zone').count()
            try:
                dict_stat['middle_living'] = grouped_zones.loc['middle_living'].iloc[0]
            except KeyError:
                dict_stat['middle_living'] = 0       
            try:
                dict_stat['low_living'] = grouped_zones.loc['low_living'].iloc[0]
            except KeyError:
                dict_stat['low_living'] = 0
            try:
                dict_stat['cottage_living'] = grouped_zones.loc['cottage_living'].iloc[0]
            except KeyError:
                dict_stat['cottage_living'] = 0
            try:
                dict_stat['school'] = grouped_zones.loc['school'].iloc[0]
            except KeyError:
                dict_stat['school'] = 0
            try:
                dict_stat['kindergarten'] = grouped_zones.loc['kindergarten'].iloc[0]
            except KeyError:
                dict_stat['kindergarten'] = 0
            try:
                dict_stat['policlinic'] = grouped_zones.loc['policlinic'].iloc[0]
            except KeyError:
                dict_stat['policlinic'] = 0
            try:
                dict_stat['park'] = grouped_zones.loc['park'].iloc[0]
            except KeyError:
                dict_stat['park'] = 0
            try:
                dict_stat['garden'] = grouped_zones.loc['garden'].iloc[0]
            except KeyError:
                dict_stat['garden'] = 0
            try:
                dict_stat['green_buffer'] = grouped_zones.loc['green_buffer'].iloc[0]
            except KeyError:
                dict_stat['green_buffer'] = 0
            try:
                dict_stat['industrial'] = grouped_zones.loc['industrial'].iloc[0]
            except KeyError:
                dict_stat['industrial'] = 0
            return(dict_stat)

    def calculate_percent_zones(gdf,total_area):
        dict_stat_p = {}
        dict_stat = StatsFuncZones.calculate_zones(gdf)
        total = sum(dict_stat.values())
        dict_stat_p['middle_living'] = round(dict_stat['middle_living'] / total_area,2)
        dict_stat_p['low_living'] = round(dict_stat['low_living'] / total_area,2)
        dict_stat_p['cottage_living'] = round(dict_stat['cottage_living'] / total,2)
        dict_stat_p['school'] = round(dict_stat['school'] / total_area,2)
        dict_stat_p['kindergarten'] = round(dict_stat['kindergarten'] / total,2)
        dict_stat_p['policlinic'] = round(dict_stat['policlinic'] / total,2)
        dict_stat_p['park'] = round(dict_stat['park'] / total_area,2)
        dict_stat_p['garden'] = round(dict_stat['garden'] / total_area,2)
        dict_stat_p['green_buffer'] = round(dict_stat['green_buffer'] / total_area,2)
        dict_stat_p['industrial'] = round(dict_stat['industrial'] / total_area,2)
        dict_stat_p['transport'] = round((total_area - total) / total_area,2)
        return(dict_stat_p)
        
    def plot_balance_calculated(gdf, total_area):
        zones = ['middle', 'low', 'cottage', 'school', 'kindergaten','policlinic', 'park', 'garden', 'buffer', 'industrial', 'transport'] #
        values = StatsFuncZones.calculate_percent_zones(gdf,total_area)
        colors = ['azure','cyan','lightblue','plum', 'orchid','tan','green','lightgreen','darkgreen','coral', 'goldenrod'] #

        list_values = []
        for i in values.values():
            list_values.append(float(i))
            
        fig, ax = plt.subplots(facecolor='w')
        ax.set_facecolor('k')
        ax.bar(zones, list_values,label='Territory balance',edgecolor="w", color='w')
        plt.xlabel('Function zone', color='k', fontsize = 15)
        plt.ylabel('Percent', color='k', fontsize = 15)
        plt.title('Balance of calculated terriotory, %', color='k', fontsize = 20)
        ax.grid(color='w', linestyle='--', linewidth=0.5)
        plt.show()

        explode = (0, 0, 0, 0, 0,0,0,0,0,0,0)
        fig, ax = plt.subplots(facecolor='k')
        ax.set_facecolor('k')
        patches, texts, autotexts = ax.pie(list_values, 
                                           explode=explode, 
                                           labels=zones, 
                                           colors=colors, 
                                           autopct='%1.1f%%',
                                           shadow=True, 
                                           startangle=90)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(12)
        for text in texts:
            text.set_color('white')
        plt.title('Balance of calculated terriotory', color='w', x=0.55)
        plt.show()




class StatsLanduse:
    def calculate_landuse(gdf):
        dict_stat = {}
        grouped_zones = gdf[['hex_id', 'landuse']].groupby('landuse').count()
        try:
            dict_stat['living'] = grouped_zones.loc['living'].iloc[0]
        except KeyError:
            dict_stat['living'] = 0       
        try:
            dict_stat['social'] = grouped_zones.loc['social'].iloc[0]
        except KeyError:
            dict_stat['social'] = 0
        try:
            dict_stat['recreation'] = grouped_zones.loc['recreation'].iloc[0]
        except KeyError:
            dict_stat['recreation'] = 0
        try:
            dict_stat['industrial'] = grouped_zones.loc['industrial'].iloc[0]
        except KeyError:
            dict_stat['industrial'] = 0
        return(dict_stat)

    def calculate_percent_landuse(gdf, total_area):
        dict_stat_p = {}
        dict_stat = StatsLanduse.calculate_landuse(gdf)
        total = sum(dict_stat.values())
        dict_stat_p['living'] = round(dict_stat['living'] / total_area,2)
        dict_stat_p['social'] = round(dict_stat['social'] / total_area,2)
        dict_stat_p['recreation'] = round(dict_stat['recreation'] / total_area,2)
        dict_stat_p['industrial'] = round(dict_stat['industrial'] / total_area,2)
        dict_stat_p['transport'] = round((total_area - total) / total,2)
        return(dict_stat_p)
        
    def plot_balance_calculated(gdf, total_area):
        fig, ax = plt.subplots(facecolor='w')
        ax.set_facecolor('k')
        zones = ['living', 'social', 'recreation', 'industrial', 'transport']
        values = StatsLanduse.calculate_percent_landuse(gdf, total_area)

        list_values = []
        for i in values.values():
            list_values.append(float(i))


        ax.bar(zones, list_values,label='Territory balance',edgecolor="w", color='w')
        plt.xlabel('Landuse', color='k', fontsize = 15)
        plt.ylabel('Percent', color='k', fontsize = 15)
        plt.title('Balance of calculated terriotory, %', color='k', fontsize = 20)
        ax.grid(color='w', linestyle='--', linewidth=0.5)
        plt.show()


        colors = ['lightblue','plum','lightgreen','coral', 'goldenrod']
        explode = (0, 0, 0, 0, 0)
        fig, ax = plt.subplots(facecolor='k')
        ax.set_facecolor('k')
        patches, texts, autotexts = ax.pie(list_values, explode=explode, labels=zones, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(12)
        for text in texts:
            text.set_color('white')
        plt.title('Balance of calculated terriotory', color='w', x=0.55)
        plt.show()

class StatsSocial:
    def print_social_objects(gdf):
        schools = len(gdf[gdf['func_zone'] == 'school'])
        kindergartens = len(gdf[gdf['func_zone'] == 'kindergarten'])
        print(f"It's required {schools} schools")
        print(f"It's required {kindergartens} kindergartens")

def plot_population(gdf):
    labels = ['under 6 years', '7-18 years', 'over 18 years old']
    total = gdf['population'].sum()
    schildren = gdf['population_schildren'].sum() / total
    teens =  gdf['population_teens'].sum() / total
    adults = 1 - schildren - teens
    sizes = [schildren, teens, adults]
    colors = ['gold', 'yellowgreen', 'lightblue']
    explode = (0, 0, 0)
    fig, ax = plt.subplots(facecolor='k')
    ax.set_facecolor('k')

    patches, texts, autotexts = ax.pie(sizes, 
                                       explode=explode, 
                                       labels=labels, 
                                       colors=colors, 
                                       autopct='%1.1f%%',
                                       shadow=True,
                                       startangle=90)   
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(12)
    for text in texts:
        text.set_color('white')
    plt.suptitle(f'Total population: {total}', y=0.9, x=0.51, color='w')
    plt.title('Age distribution', y=1.05, fontsize=18, color='w')
    plt.show()
    return()