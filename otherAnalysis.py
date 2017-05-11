import numpy as np
import pandas as pd
import preprocessing

def createDirGross(df1):
	gross={}
	dircat= df1.groupby(['rank'])['director_name'].value_counts()
	for i in range(1,5):
		counts=dircat.ix[i]
		names=dircat.ix[i].keys()
		for i in range(len(counts)):
			if(counts[i]>=2):		
				
				gross[names[i]]=counts[i] 
	print gross
		# print dircat.keys()
def createDirImdb(df1):
	gross={}
	dircat= df1.groupby(['director_name']) 
	print dircat['imdb_score'].mean().to_dict()

def createDirScore(df1):
	dircat= df1.groupby(['rank'])['director_name'].value_counts()
	direc = df1['director_name'].value_counts()
	dnames=direc.keys()
	# print dircat.ix[4]['Steven Spielberg']
	dirdi={}
	for i in range(1,5):
		counts=dircat.ix[i]
		names=dircat.ix[i].keys()
		for j in range(len(counts)):
			if dirdi.has_key(names[j]) is False:
				dirdi[names[j]]=0
				dirdi[names[j]]+=counts[j]*math.pow(i,i)
				

	df1['director_score']=1
	# print df1['director_name'][0]
	# for i in range(len(dnames)):
	# 	# if direc.ix[i]<=2:
	# 		dirdi[dnames[i]]=float(dirdi[dnames[i]])/direc.ix[i]

	i=0
	for name in df1['director_name']:
	 	if dirdi.has_key(name):
	 		df1.loc[i,'director_score']=dirdi[name]
	 	i+=1
 	print df1.ix[df1["rank"]==4,"direc"]
 	return df1

df1=preprocessing.prepData()
# print list(df1)
createDirGross(df1)