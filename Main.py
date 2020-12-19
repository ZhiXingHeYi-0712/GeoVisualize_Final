from utils.Province import Province
import os
import pandas as pd

province = Province('guangdong', '广东省')
province.initProvinceRaster()
province.generateProvinceData()
# province.plotTimeSeries('广州市')
province.plotProvince(2010)