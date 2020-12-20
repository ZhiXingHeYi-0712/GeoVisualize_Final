import rasterio as rio
from rasterstats import zonal_stats
import geopandas as gpd
import numpy as np

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimSun'

year_list = [1970, 1980, 1995, 2000, 2005, 2010, 2015, 2018]
guangdong = gpd.read_file('data/全国市级边界_融合/CN-shi-A-dissolve.shp')
guangdong.query('F4 == "广东省"', inplace=True) # 换省1

first = True
for year in year_list:
    year_string = ''

    if year == 1970 or year == 1980:
        year_string = '{}s'.format(year)
    else:
        year_string = str(year)

    # 换省2
    file_path = 'data/lucc/{year_string}/guangdong/ld{year_string}'.format(year_string=year_string)

    raster: rio.DatasetReader = rio.open(file_path)
    lucc: np.ndarray = raster.read(1)
    lucc = np.where((lucc >= 51) & (lucc <= 53), 1, 0)

    stats_result = zonal_stats(guangdong, lucc,
                stats=['count', 'sum'], affine = raster.transform,
                geojson_out=True, nodata=raster.nodata)

    if first:
        geo_result = gpd.GeoDataFrame.from_features(stats_result)
        geo_result['FUA_{}'.format(year)] = geo_result['sum'] / geo_result['count']
        geo_result.set_index('CityNameC', inplace=True)
        first = False
    else:
        geo_this_year = gpd.GeoDataFrame.from_features(stats_result)
        geo_this_year['FUA_{}'.format(year)] = geo_this_year['sum'] / geo_this_year['count']
        geo_this_year.set_index('CityNameC', inplace=True)

        geo_result = geo_result.join(geo_this_year[['FUA_{}'.format(year)]])

    pic: plt.Axes = geo_result.plot(column='FUA_{}'.format(year), cmap='OrRd',
                    scheme='quantiles', legend=True, edgecolor='black', linewidth=0.3,
                    legend_kwds={
                        'fmt': '{:.3f}',
                        'title': 'FUA',
                        'loc': 'lower left',
                        'bbox_to_anchor': (1, 0),
                        'borderaxespad': 0
                    },
                    k=5)
    pic.axis('off')
    # 换省3
    pic.set_title('广东省{}年FUA'.format(year))
    pic.plot()
    plt.show()

#换市
plot_data = geo_result.loc[['广州市']].T['FUA_1970':'FUA_2018']
plot_data.rename(lambda s : s.replace('FUA_', ''), inplace=True)
plot_data.plot()
plt.show()


