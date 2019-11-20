# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# **[Geospatial Analysis Home Page](https://www.kaggle.com/learn/geospatial-analysis)**
#
# ---
#

# # Introduction
#
# You are a bird conservation expert and want to understand migration patterns of purple martins.  In your research, you discover that these birds typically spend the summer breeding season in the eastern United States, and then migrate to South America for the winter.  But since this bird is under threat of endangerment, you'd like to take a closer look at the locations that these birds are more likely to visit.
#
# <center>
# <img src="https://i.imgur.com/qQcS0KM.png" width="1000"><br/>
# </center>
#
# There are several [protected areas](https://www.iucn.org/theme/protected-areas/about) in South America, which operate under special regulations to ensure that species that migrate (or live) there have the best opportunity to thrive.  You'd like to know if purple martins tend to visit these areas.  To answer this question, you'll use some recently collected data that tracks the year-round location of eleven different birds.
#
# Before you get started, run the code cell below to set everything up.

# 關於地圖投影法 
# 動機 : 地圖投影是2D的，但地球是3D的，換句話說，2D投影會有一些誤導
# 因此有各式各樣的投影法
# 兩個最常用的 : 
# 1. 等面積投影(equal-area projection)，當你需要計算某個效應的影響面積，或是某個城市的面積，這會很有用
# 2. 等距離投影(equidistant projections，舉例 方位角等距投影(Azimuthal Equidistant projection"))，當你需要計算例如航線距離，A點到B點的球面距離，但你擁有的是地圖數據時，這會很有用
#
# 各種投影法的集合被稱為座標參考系統(coordinate reference system, CRS)

# +
import pandas as pd
import geopandas as gpd

from shapely.geometry import LineString

from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex2 import *
# -

# # Exercises
#
# ### 1) Load the data.
#
# Run the next code cell (without changes) to load the GPS data into a pandas DataFrame `birds_df`.  

# Load the data and print the first 5 rows
birds_df = pd.read_csv("../input/geospatial-learn-course-data/purple_martin.csv", parse_dates=['timestamp'])
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))
birds_df.head()

# There are 11 birds in the dataset, where each bird is identified by a unique value in the "tag-local-identifier" column.  Each bird has several measurements, collected at different times of the year.
#
# Use the next code cell to create a GeoDataFrame `birds`.  
# - `birds` should have all of the columns from `birds_df`, along with a "geometry" column that contains Point objects with (longitude, latitude) locations.  
# - Set the CRS of `birds` to `{'init': 'epsg:4326'}`.

# GeoDataFrame中有一個屬性被稱為crs，指的就是這個GeoDataFrame使用的crs為哪一個投影法，各種投影法可以在 European Petroleum Survey Group (EPSG)查到，
# 最常用的是麥卡托投影法(Mercator projection)，這個投影法保證角度一定是和原本3D地球一樣，在航海定位時非常有用，而且扭曲地圖的程度也較低，其編號為(init : 'epsg:32630')

# +
# Your code here: Create the GeoDataFrame
birds = gpd.GeoDataFrame(birds_df, 
                         geometry=gpd.points_from_xy(
                         birds_df['location-long'],
                         birds_df['location-lat']))

# Your code here: Set the CRS to {'init': 'epsg:4326'}
birds.crs = {'init':'epsg:4326'}

# Check your answer
q_1.check()
# -

display(birds.head(),
       birds.crs)

# +
# Lines below will give you a hint or solution code
#q_1.hint()
#q_1.solution()
# -

# ### 2) Plot the data.
#
# Next, we load in the `'naturalearth_lowres'` dataset from GeoPandas, and set `americas` to a GeoDataFrame containing the boundaries of all countries in the Americas (both North and South America).  Run the next code cell without changes.

# * 當我們在畫地圖時，投影方式很重要，一定要加入確認項目，避免一些不必要的bug
# * 而修正投影方式的"方法" `to_crs` 使用方式 : GeoDataFrame.to_crs(epsg=77665)，只會修改`geometry` 這個 column
# * 如果想要使用的編碼方式再GeoPandas中沒有，我們可以使用CRS的proj4字符串
# `+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs`

# Load a GeoDataFrame with country boundaries in North/South America, print the first 5 rows
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
americas = world.loc[world['continent'].isin(['North America', 'South America'])]
display(americas.head(),
       americas.crs)


# Use the next code cell to create a single plot that shows both: (1) the country boundaries in the `americas` GeoDataFrame, and (2) all of the points in the `birds_gdf` GeoDataFrame.  
#
# Don't worry about any special styling here; just create a preliminary plot, as a quick sanity check that all of the data was loaded properly.  In particular, you don't have to worry about color-coding the points to differentiate between birds, and you don't have to differentiate starting points from ending points.  We'll do that in the next part of the exercise.

# +
# Your code here
# world
ax = americas.plot(figsize=(8,8), color='whitesmoke', linestyle='--', edgecolor='black')
# birds
birds.plot(markersize=3, ax=ax)

# Uncomment to see a hint
#q_2.hint()
# -

# try different projection
PROJECTION_CODE = 32630
ax2 = americas.to_crs(epsg=PROJECTION_CODE).plot(figsize=(8,8), color='whitesmoke', linestyle='--', edgecolor='black')
birds.to_crs(epsg=32630).plot(markersize=3, ax=ax2)
# just awful result, see?

# +
# Get credit for your work after you have created a map
q_2.check()

# Uncomment to see our solution (your code may look different!)
##q_2.solution()
# -

# 關於geometry的方法及屬性?
print(
    [attr for attr in dir(birds.geometry)
          if attr not in dir(birds_df.geometry)]
)
# Point : 事件中心, 震央
# LineString : 街道, 路線
# Polygon : 邊界, 城市邊界, 國家邊界, 
# x, y
# 我們可以看到GeoDataFrame的geometry特有的屬性, 
# 例如 x, y, area, boundry, length, has_z...等等

# ### 3) Where does each bird start and end its journey? (Part 1)
#
# Now, we're ready to look more closely at each bird's path.  Run the next code cell to create two GeoDataFrames:
# - `path_gdf` contains LineString objects that show the path of each bird.  It uses the `LineString()` method to create a LineString object from a list of Point objects.
# - `start_gdf` contains the starting points for each bird.

# +
# GeoDataFrame showing path for each bird
path_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: LineString(x)).reset_index()
path_gdf = gpd.GeoDataFrame(path_df, geometry=path_df.geometry)
path_gdf.crs = {'init' :'epsg:4326'}

# GeoDataFrame showing starting point for each bird
start_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[0]).reset_index()
start_gdf = gpd.GeoDataFrame(start_df, geometry=start_df.geometry)
start_gdf.crs = {'init' :'epsg:4326'}

# Show first five rows of GeoDataFrame
start_gdf.head()
# -

# Use the next code cell to create a GeoDataFrame `end_gdf` containing the final location of each bird.  
# - The format should be identical to that of `start_gdf`, with two columns ("tag-local-identifier" and "geometry"), where the "geometry" column contains Point objects.
# - Set the CRS of `end_gdf` to `{'init': 'epsg:4326'}`.

# +
# Your code here
end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init' :'epsg:4326'}

# Check your answer
q_3.check()
# -

# Lines below will give you a hint or solution code
q_3.hint()
#q_3.solution()

# ### 4) Where does each bird start and end its journey? (Part 2)
#
# Use the GeoDataFrames from the question above (`path_gdf`, `start_gdf`, and `end_gdf`) to visualize the paths of all birds on a single map.  You may also want to use the `americas` GeoDataFrame.

# +
# display(len(start_df),
#        len(path_df),
#        len(end_df),
#        len(start_gdf),
#        len(path_gdf),
#        len(end_gdf))

# +
from matplotlib import pyplot as plt

# Your code here
# map
# Your code here
# world
ax = americas.plot(figsize=(8,8), color='whitesmoke', linestyle=':', edgecolor='black')
# start
start_gdf.plot(markersize=30, label='start', c='blue', ax=ax)
# end
end_gdf.plot(markersize=30, label='end', c='red', ax=ax)
# path
path_gdf.plot(label='path', color='orange',linestyle='-',linewidth=1,ax=ax)
# legend
plt.legend()
# Uncomment to see a hint
q_4.hint()


# Uncomment to see a hint
#q_4.hint()

# +
# Get credit for your work after you have created a map
q_4.check()

# Uncomment to see our solution (your code may look different!)
q_4.solution()
# -

# ### 5) Where are the protected areas in South America? (Part 1)
#
# It looks like all of the birds end up somewhere in South America.  But are they going to protected areas?
#
# In the next code cell, you'll create a GeoDataFrame `protected_areas` containing the locations of all of the protected areas in South America.  The corresponding shapefile is located at filepath `protected_filepath`.

# +
# Path of the shapefile to load
protected_filepath = "../input/geospatial-learn-course-data/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp"

# Your code here
protected_areas = gpd.read_file(protected_filepath)

# Check your answer
q_5.check()

# +
# Lines below will give you a hint or solution code
#q_5.hint()
#q_5.solution()
# -

# ### 6) Where are the protected areas in South America? (Part 2)
#
# Create a plot that uses the `protected_areas` GeoDataFrame to show the locations of the protected areas in South America.  (_You'll notice that some protected areas are on land, while others are in marine waters._)

# +
# Country boundaries in South America
south_america = americas.loc[americas['continent']=='South America']

# Your code here: plot protected areas in South America
south_america.to_crs(epsg=4326).plot()

# Uncomment to see a hint
#q_6.hint()

# +
# Get credit for your work after you have created a map
q_6.check()

# Uncomment to see our solution (your code may look different!)
#q_6.solution()
# -

# ### 7) What percentage of South America is protected?
#
# You're interested in determining what percentage of South America is protected, so that you know how much of South America is suitable for the birds.  
#
# As a first step, you calculate the total area of all protected lands in South America (not including marine area).  To do this, you use the "REP_AREA" and "REP_M_AREA" columns, which contain the total area and total marine area, respectively, in square kilometers.
#
# Run the code cell below without changes.

display(protected_areas.head(),
       protected_areas.columns)

P_Area = sum(protected_areas['REP_AREA']-protected_areas['REP_M_AREA'])
print("South America has {} square kilometers of protected areas.".format(P_Area))

# Then, to finish the calculation, you'll use the `south_america` GeoDataFrame.  

south_america.head()

# Calculate the total area of South America by following these steps:
# - Calculate the area of each country using the `area` attribute of each polygon (with EPSG 3035 as the CRS), and add up the results.  The calculated area will be in units of square meters.
# - Convert your answer to have units of square kilometeters.

# 根據特定國家，有特定的編碼方式來符合政府規範，這裡在南美洲使用3035, 台灣的話，可以參考[台灣常用的 EPSG代碼](http://gis.rchss.sinica.edu.tw/qgis/?p=2823)

# Your code here: Calculate the total area of South America (in square kilometers)
totalArea = sum(south_america.to_crs(epsg=3035).area) / (10^6)
print(totalArea)
# print(P_Area / totalArea)
# Check your answer
q_7.check()

# Lines below will give you a hint or solution code
q_7.hint()
#q_7.solution()

# Run the code cell below to calculate the percentage of South America that is protected.

# What percentage of South America is protected?
percentage_protected = P_Area/totalArea
print('Approximately {}% of South America is protected.'.format(round(percentage_protected*100, 2)))

# ### 8) Where are the birds in South America?
#
# So, are the birds in protected areas?  
#
# Create a plot that shows for all birds, all of the locations where they were discovered in South America.  Also plot the locations of all protected areas in South America.
#
# To exclude protected areas that are purely marine areas (with no land component), you can use the "MARINE" column (and plot only the rows in `protected_areas[protected_areas['MARINE']!='2']`, instead of every row in the `protected_areas` GeoDataFrame).

ax = americas.plot(figsize=(8,8), color='whitesmoke', linestyle=':', edgecolor='black')
# start
start_gdf.plot(markersize=30, label='start', c='blue', ax=ax)
# end
end_gdf.plot(markersize=30, label='end', c='red', ax=ax)
# path
path_gdf.plot(label='path', color='orange',linestyle='-',linewidth=1,ax=ax)
# legend
plt.legend()

# +
# birds
# -

# prepare data
land_protected_areas = protected_areas[protected_areas['MARINE'] != '2']
birds_south = birds[birds.geometry.y < 0] # south side for all birds
# map
PROJECTION_CODE = 4326
ax = south_america.to_crs(epsg=PROJECTION_CODE).plot(figsize=(8,8), color='whitesmoke', 
                                                     linestyle=':', edgecolor='black')
# land_protected_area zorder for coverd by bird points
land_protected_areas.to_crs(epsg=PROJECTION_CODE).plot(ax=ax, color='blue', alpha=.3,
                                                       label='protected area',zorder=1)
# all the birds
birds_south.to_crs(epsg=PROJECTION_CODE).plot(ax=ax, markersize=15, color='red',
                                              label='birds',zorder=2)
plt.legend()

# +
# Your code here
____

# Uncomment to see a hint
q_8.hint()

# +
# Get credit for your work after you have created a map
q_8.check()

# Uncomment to see our solution (your code may look different!)
q_8.solution()
# -

# # Keep going
#
# Create stunning **[interactive maps](https://www.kaggle.com/alexisbcook/interactive-maps)** with your geospatial data.

# ---
# **[Geospatial Analysis Home Page](https://www.kaggle.com/learn/geospatial-analysis)**
#
#
#
#
#
# *Have questions or comments? Visit the [Learn Discussion forum](https://www.kaggle.com/learn-forum) to chat with other Learners.*
