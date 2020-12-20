import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('processed_data/FUA_AOI_guangdong.csv')

y_list = ['gdp_2015', 'pop_2015', 'FUA_2015']

for y in y_list:
    data.plot.scatter(x='aoi', y=y)
    print(data['aoi'].corr(data[y]))
plt.show()

