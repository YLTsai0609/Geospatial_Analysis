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
# [Kiva.org](https://www.kiva.org/) is an online crowdfunding platform extending financial services to poor people around the world. Kiva lenders have provided over $1 billion dollars in loans to over 2 million people.
#
# <center>
# <img src="https://i.imgur.com/2G8C53X.png" width="500"><br/>
# </center>
#
# Kiva reaches some of the most remote places in the world through their global network of "Field Partners". These partners are local organizations working in communities to vet borrowers, provide services, and administer loans.
#
# In this exercise, you'll investigate Kiva loans in the Philippines.  Can you identify regions that might be outside of Kiva's current network, in order to identify opportunities for recruiting new Field Partners?
#
# To get started, run the code cell below to set up our feedback system.

# +
import geopandas as gpd

from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex1 import *
# -

# ### 1) Get the data.
#
# Use the next cell to load the shapefile located at `loans_filepath` to create a GeoDataFrame `world_loans`.  

# * 地理資料約略有4種 : shapefile, GeoJSON, KML, GKPG
# * 最常遇到的會是 shapefile, 可以輕易的被geopandas.read_file()方法讀取
# * geopandas.geodataframe.GeoDataFrame繼承了pandas的dataframe，所以擁有所有dataframe的屬性及方法
# * 通常會多出一個欄位是描述地理屬性，這個例子中用經緯度表示 : 'geometry' column

# +
loans_filepath = "../input/geospatial-learn-course-data/kiva_loans/kiva_loans/kiva_loans.shp"

# Your code here: Load the data
world_loans = gpd.read_file(loans_filepath)

# Check your answer
q_1.check()

# Uncomment to view the first five rows of the data
display('(Rows, features)' ,
        world_loans.shape,
        'Missing values',
        world_loans.isnull().sum() / len(world_loans),
        'Dtypes',
        world_loans.info(),
        'Snap',
        world_loans.head())

# +
# Lines below will give you a hint or solution code
# q_1.hint()
#q_1.solution()
# -

# ### 2) Plot the data.
#
# Run the next code cell without changes to load a GeoDataFrame `world` containing country boundaries.

# This dataset is provided in GeoPandas
world_filepath = gpd.datasets.get_path('naturalearth_lowres')
world = gpd.read_file(world_filepath)
world.head()

# * geometry欄位中會對該資料的地理形狀做進一步的描述
# * 通常會有3種, Point(點), LineString(路徑), Polygon(多邊形)

# Use the `world` and `world_loans` GeoDataFrames to visualize Kiva loan locations across the world.

# Your code here
ax = world.plot(figsize=(20,20), color='whitesmoke', linestyle=':', edgecolor='black')
world_loans.plot(ax=ax, markersize=2)
# Uncomment to see a hint
# q_2.hint()

# +
# Get credit for your work after you have created a map
q_2.check()

# Uncomment to see our solution (your code may look different!)
q_2.solution()
# -

# ### 3) Select loans based in the Philippines.
#
# Next, you'll focus on loans that are based in the Philippines.  Use the next code cell to create a GeoDataFrame `PHL_loans` which contains all rows from `world_loans` with loans that are based in the Philippines.

# +
# Explore where the "Philippines" data in 
# cols = ['Field Part','sector','country']
# for c in cols : 
#     print(c)
#     print('-'*60)
#     print(world_loans[f'{c}'].value_counts())
# Got answer : 'country' 

# +
# Your code here
PHL_loans = world_loans.query('country == "Philippines"')

# Check your answer
q_3.check()

# +
# Lines below will give you a hint or solution code
#q_3.hint()
#q_3.solution()
# -

# ### 4) Understand loans in the Philippines.
#
# Run the next code cell without changes to load a GeoDataFrame `PHL` containing boundaries for all islands in the Philippines.

# Load a KML file containing island boundaries
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
PHL = gpd.read_file("../input/geospatial-learn-course-data/Philippines_AL258.kml", driver='KML')
PHL.head()

# Use the `PHL` and `PHL_loans` GeoDataFrames to visualize loans in the Philippines.

# Your code here
# our base map
ax = PHL.plot(figsize=(10, 10), color = 'none', edgecolor='gainsboro',
              zorder=3)
PHL_loans.plot(color='maroon',markersize=2, ax=ax)
# Uncomment to see a hint
#q_4.a.hint()

# +
# Get credit for your work after you have created a map
q_4.a.check()

# Uncomment to see our solution (your code may look different!)
# q_4.a.solution()
# -

# Can you identify any islands where it might be useful to recruit new Field Partners?  Do any islands currently look outside of Kiva's reach?
#
# You might find [this map](https://bit.ly/2U2G7x7) useful to answer the question.

# * 菲律賓中段的地方仍然有著較少的借貸，有更多資訊的情況下(例如我們在疊一張可以透露需求量的地圖)，我們就能夠回答這個問題

# View the solution
q_4.b.solution()

# # Keep going
#
# Continue to learn about **[coordinate reference systems](https://www.kaggle.com/alexisbcook/coordinate-reference-systems)**.

# ---
# **[Geospatial Analysis Home Page](https://www.kaggle.com/learn/geospatial-analysis)**
#
#
#
#
#
# *Have questions or comments? Visit the [Learn Discussion forum](https://www.kaggle.com/learn-forum) to chat with other Learners.*
