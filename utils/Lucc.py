import os
import rasterio
import numpy as np
import geopandas as gpd
from rasterstats import zonal_stats
from rasterio.mask import mask

class Lucc():
    def __init__(self, province: str, province_zh:str, year: int, data_folder: str = 'data/lucc'):
        self.province = province
        self.province_zh = province_zh
        self.year = year

        if year not in [1970, 1980, 1995, 2000, 2005, 2010, 2015, 2018]:
            raise Exception('year {} has no data.'.format(year))

        year_str = str(year)
        if year == 1970 or year == 1980:
            year_str += 's'

        self.data_position = os.path.join(data_folder, year_str, province, 'ld{}'.format(year_str))

    def initRasterData(self):
        self.raster_data: rasterio.DatasetReader = rasterio.open(self.data_position)

    def getSubregionFUA(self, first: bool = True) -> gpd.GeoDataFrame:
        fua_column_name = 'FUA_{}'.format(self.year)
        lucc: np.ndarray = self.raster_data.read(1)
        lucc = np.where((lucc >= 51) & (lucc <= 53), 1, 0)
        gdf = gpd.read_file('data/全国市级边界/CN-shi-A.shp')
        gdf = gdf[gdf['F4'] == self.province_zh]
        stat_result = zonal_stats(gdf, lucc,
                                  stats=['count', 'sum'], affine=self.raster_data.transform,
                                  geojson_out=True, nodata=self.raster_data.nodata)
        geo_result = gpd.GeoDataFrame.from_features(stat_result)
        geo_result[fua_column_name] = geo_result['sum'] / geo_result['count']
        del geo_result['count']
        del geo_result['sum']
        geo_result.set_index('CityNameC', inplace=True)
        if first:
            return geo_result
        else:
            return geo_result[[fua_column_name]]

    def getProvinceFUA(self):
        lucc: np.ndarray = self.raster_data.read(1).ravel()
        lucc = lucc[lucc != 255]
        city: np.ndarray = lucc[np.where((51 <= lucc) & (lucc <= 53))]
        return {'year': self.year, 'FUA': len(city) / len(lucc)}
