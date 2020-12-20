import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

fua = gpd.read_file('processed_data/FUA_guangdong.shp', encoding='utf-8')

aoi_file = pd.ExcelFile('data/PM2.5CitiesChina2015.xlsx')
aoi = pd.read_excel(aoi_file, sheet_name=aoi_file.sheet_names[-1])
guangdong_data = pd.ExcelFile('data/广东省各市2010-2019数据2.xlsx')
gdp = pd.read_excel(guangdong_data, sheet_name=guangdong_data.sheet_names[0])
pop = pd.read_excel(guangdong_data, sheet_name=guangdong_data.sheet_names[-1])


def generateQueryString(city_names: pd.Series):
    base_query_string = '城市名称 == "{}"'
    query_string_node = []
    for city in city_names:
        query_string_node.append(base_query_string.format(city))
    return ' or '.join(query_string_node)


query_string = generateQueryString(gdp['city'])
aoi_region = aoi.query(query_string)
fua.set_index('CityNameC', inplace=True)
aoi_region.set_index('城市名称', inplace=True)
gdp.set_index('city', inplace=True)
pop.set_index('city', inplace=True)

aoi_region.index += '市'
gdp.index += '市'
pop.index += '市'

fua = fua.join(aoi_region).join(gdp).join(pop)

gdps = ['gdp_2010', 'gdp_2011', 'gdp_2012', 'gdp_2013',
        'gdp_2014', 'gdp_2015', 'gdp_2016', 'gdp_2017',
        'gdp_2018', 'gdp_2019']
# for gdp_year in gdps:
#     pic: plt.Axes = fua.plot(column=gdp_year, cmap='OrRd',
#                              scheme='quantiles', legend=True,
#                              edgecolor='black', linewidth=0.3,
#                              legend_kwds={
#                                  'fmt': '{:.0f}',
#                                  'title': 'GDP',
#                                  'loc': 'lower left',
#                                  'bbox_to_anchor': (1, 0),
#                                  'borderaxespad': 0
#                              },
#                              k=5)
#     pic.axis('off')
# plt.show()
fua['UR'] = (fua['FUA_2018'] - fua['FUA_1970']) / fua['FUA_1970']
y_list = ['PM2_5','gdp_2015', 'pop_2015']

# for y in y_list:
#     pic = pd.DataFrame(fua).plot.scatter(x='UR', y=y)
#     pic.get_figure().savefig('{}.png'.format(y))
# plt.show()

gdp_guangzhou = fua.loc['广州市']['gdp_2010':'gdp_2019']
# gdp_guangzhou.rename(lambda x : x.replace('gdp_', ''))
gdp_guangzhou.rename({'gdp_2010': 2010, 'gdp_2011': 2011, 'gdp_2012': 2012, 'gdp_2013': 2013, 'gdp_2014': 2014,'gdp_2015':  2015, 'gdp_2016': 2016, 'gdp_2017': 2017, 'gdp_2018': 2018, 'gdp_2019': 2019}).plot()