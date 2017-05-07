import numpy as np
import pandas as pd
import preprocessing
def createDirGross(df1):
	gross={}
	dircat= df1.groupby(['director_name']) 
	print dircat['gross'].mean().to_dict()

def createDirImdb(df1):
	gross={}
	dircat= df1.groupby(['director_name']) 
	print dircat['imdb_score'].mean().to_dict()

df1=preprocessing.prepData()
createDirGross(df1)