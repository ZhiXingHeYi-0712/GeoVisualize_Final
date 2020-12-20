import geopandas as gpd
import pandas as pd
import utils.CityNameTools as tools
import matplotlib.pyplot as plt


fua = gpd.read_file('processed_data/FUA_guangdong.shp', encoding='utf-8')

aoi_file = pd.ExcelFile('data/PM2.5CitiesChina2015.xlsx')
aoi = pd.read_excel(aoi_file, sheet_name=aoi_file.sheet_names[-1])
guangdong_data = pd.ExcelFile('data/广东省各市2010-2019数据.xlsx')
gdp = pd.read_excel(guangdong_data, sheet_name=guangdong_data.sheet_names[0])
pop = pd.read_excel(guangdong_data, sheet_name=guangdong_data.sheet_names[-1])

aoi_data_list = []
for city in fua['CityNameC']:
    city_name_format = tools.formatCityName(city)
    query_result = aoi[aoi['城市名称'].str.contains(city_name_format)]
    finish = False
    if not query_result.empty:
        aoi_data_list.append(aoi.loc[aoi['城市名称'].str.contains(city_name_format)]['PM2_5'].iloc[0])
        continue
    else:
        for i in aoi.iterrows():
            if tools.isNameEquivalent(i[1]['城市名称'], city_name_format):
                aoi_data_list.append(i[1]['PM2_5'].iloc[0])
                finish = True
                break
            if not finish:
                aoi_data_list.append(None)
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@\n WARNING: {} is not matched!\n @@@@@@@@@@@@@@@@@@@@@@@@@@'
                      .format(city))

fua['aoi'] = aoi_data_list
fua: gpd.GeoDataFrame = fua.set_index('CityNameC').join(gdp.set_index('city')).join(pop.set_index('city'))
# fua.to_file('processed_data/FUA_AOI_guangdong.shp')

gdps = ['gdp_{}'.format(year) for year in range(2010, 2020)]
for gdp_year in gdps:
    pic: plt.Axes = fua.plot(column=gdp_year, cmap='OrRd',
                                   scheme='quantiles', legend=True,
                                   edgecolor='black', linewidth=0.3,
                                   legend_kwds={
                                       'fmt': '{:.0f}',
                                       'title': 'GDP',
                                       'loc': 'lower left',
                                       'bbox_to_anchor': (1, 0),
                                       'borderaxespad': 0
                                   },
                                   k=5)
    pic.axis('off')
plt.show()
# fua[[col for col in fua.columns if col not in ['OBJECTID','Shape_Area','Shape_Leng','geometry']]]\
#     .to_csv('processed_data/FUA_AOI_guangdong.csv', encoding='utf-8')


