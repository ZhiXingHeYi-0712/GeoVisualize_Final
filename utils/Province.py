from utils.Lucc import Lucc
import geopandas as gpd
import rasterio.mask
import matplotlib.pyplot as plt


class Province():
    def __init__(self, province: str, province_zh: str):
        plt.rcParams['font.family'] = 'SimSun'
        self.province = province
        self.province_zh = province_zh
        self.luccs = [Lucc(province, province_zh, year)
                      for year in [1970, 1980, 1995, 2000, 2005, 2010, 2015, 2018]]

    def initProvinceRaster(self):
        for lucc in self.luccs:
            lucc.initRasterData()

    def generateProvinceData(self):
        fua_info = None
        gdf = gpd.read_file('data/全国市级边界_融合/CN-shi-A-dissolve.shp')
        for i, lucc in enumerate(self.luccs):
            if i == 0:
                fua_info = lucc.getSubregionFUA(gdf=gdf)
            else:
                fua_info = fua_info.join(lucc.getSubregionFUA(first=False, gdf=gdf))
        self.FUAs: gpd.GeoDataFrame = fua_info

    def plotProvince(self, year: int, cmap: str = 'OrRd',
                     scheme: str = 'quantiles', scheme_kinds: int = 5,
                     title: str = None, save_file: bool = False, save_filename: str = None):
        pic: plt.Axes = self.FUAs.plot(column='FUA_{}'.format(year), cmap=cmap,
                                       scheme=scheme, legend=True,
                                       edgecolor='black', linewidth=0.3,
                                       legend_kwds={
                                           'fmt': '{:.3f}',
                                           'title': 'FUA',
                                           'loc': 'lower left',
                                           'bbox_to_anchor': (1, 0),
                                           'borderaxespad': 0
                                       },
                                       k=scheme_kinds)
        pic.axis('off')
        if title != None:
            pic.set_title(title)
        else:
            pic.set_title('{province}{year}年各地市城市面积比分布图'
                          .format(province=self.province_zh, year=year))

        if save_file:
            if save_filename != None:
                filename = save_filename
                if save_filename.split('.')[-1] not in ['png', 'jpg', 'jpeg', 'gif']:
                    filename += '.png'
            else:
                filename = 'FUA_{province}_{year}.png'.format(province=self.province, year=year)
            pic.get_figure().savefig(filename, dpi=300)

        else:
            pic.plot()
            plt.show()

    def plotTimeSeries(self, region: str, save_file: bool = False, save_filename: str = None):
        region_data = self.FUAs.loc[[region]]
        plot_data: gpd.GeoDataFrame = region_data.T['FUA_1970':'FUA_2018']
        plot_data.rename(lambda s : s.replace('FUA_', ''), inplace=True)

        plot_data.plot()
        plt.show()