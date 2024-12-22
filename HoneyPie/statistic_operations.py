import matplotlib.pyplot as plt

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

def calculate_percent_zones(gdf):
    dict_stat_p = {}
    dict_stat = calculate_zones(gdf)
    total = sum(dict_stat.values())
    dict_stat_p['middle_living'] = round(dict_stat['middle_living'] / total,2)
    dict_stat_p['low_living'] = round(dict_stat['low_living'] / total,2)
    dict_stat_p['cottage_living'] = round(dict_stat['cottage_living'] / total,2)
    dict_stat_p['school'] = round(dict_stat['school'] / total,2)
    dict_stat_p['kindergarten'] = round(dict_stat['kindergarten'] / total,2)
    dict_stat_p['park'] = round(dict_stat['park'] / total,2)
    dict_stat_p['garden'] = round(dict_stat['garden'] / total,2)
    dict_stat_p['green_buffer'] = round(dict_stat['green_buffer'] / total,2)
    dict_stat_p['industrial'] = round(dict_stat['industrial'] / total,2)
    return(dict_stat_p)
    
def plot_balance_calculated(gdf):
    zones = ['middle', 'low', 'cottage', 'school', 'kindergaten', 'park', 'garden', 'buffer', 'industrial']
    values = calculate_percent_zones(gdf).values()
    plt.bar(zones, values, label='Territory balance', edgecolor="black")
    plt.xlabel('Function zone, %')
    plt.ylabel('Percent')
    plt.title('Balance of calculated terriotory')
    plt.legend()
    plt.show()

    plt.pie(values, labels=zones, autopct='%1.1f%%')
    plt.title('Balance of calculated terriotory')
    plt.show()