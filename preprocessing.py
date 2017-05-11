import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random
import math
import operator
import json
from sklearn.decomposition import PCA
from pymongo import MongoClient
client=MongoClient()
client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_test']
posts=db.posts
# post_data={
# 	'id':'test123',
# 	'test':'this is just a test phrase'
# }
# result=posts.insert_one(post_data)
# print('One post: {0}'.format(result.inserted_id)) 
# #trying to answer the question what makes a movie good?


# bills_post = posts.find_one({'id': 'test123'})
# print(bills_post)
#print(df1)
# def createCSV(data_frame,filename):
#     data_frame.columns=["director_name","num_critic_for_reviews","duration","director_facebook_likes","actor_2_name","actor_1_facebook_likes","gross","genres","actor_1_name","movie_title","num_voted_users","cast_total_facebook_likes","plot_keywords","num_user_for_reviews","language","country","content_rating","budget","title_year","actor_2_facebook_likes","imdb_score","movie_facebook_likes"]
#     fileName=filename+".csv"
#     data_frame.to_csv(fileName,sep=',')

# def parseGenres(df1):
# 	idx=1
# 	res=[]
# 	di={}
# 	# di={'Action':1,'Adventure':2,'Sci-Fi':3,'Romance':4,'Comedy':5,'Horror':6,'Drama':7,'Thriller':8,'Documentary':9}
# 	allg=list(df1['genres'])
# 	#print len(df1)
# 	for i in range(len(allg)):
# 		s=allg[i]
# 		g=s.split('|')
# 		num=0
# 		for j in range(len(g)):
# 			key=g[j]
# 			if di.has_key(key):

# 				# num=num*10+di[key]
# 			else:
# 				di[key]=idx
# 				idx+=1
# 				# num=num*10		
# 		res.append(num)
# 	print "total genres:"+str(idx)
# 	df1.drop(['genres'],1)
# 	df1['genres']=res
# 	#print di.keys()
# 	return df1


def rankMovies(df): #ranking movies based on imdb score
	df['rank']=np.ones(len(df))
	qt=df['imdb_score'].quantile([0.25,0.5,0.75]).values
	df.loc[df['imdb_score']>qt[2],'rank']=4
	df.loc[(df['imdb_score']<=qt[2]) &(df['imdb_score']>qt[1]),'rank']=3
	df.loc[(df['imdb_score']<=qt[1]) &(df['imdb_score']>qt[0]),'rank']=2
	return df
def classMovies(df): #ranking movies based on budget score
	df['class']=np.ones(len(df))
	qt=df['budget'].quantile([0.25,0.5,0.75]).values
	df.loc[df['budget']>qt[2],'class']=4
	df.loc[(df['budget']<=qt[2]) &(df['budget']>qt[1]),'class']=3
	df.loc[(df['budget']<=qt[1]) &(df['budget']>qt[0]),'class']=2
	return df

def sampling(df,fraction):	#sampling based on imdb scores
	cl_rows=[]
	qt=df1['imdb_score'].quantile([0.25,0.5,0.75]).values #creating quantiles of scores	
	cl_rows.append(df.ix[random.sample(df[df['rank']==1].index,(int)(len(df[df['rank']==1])*fraction))])	#ramdom samples from quantile group
	cl_rows.append(df.ix[random.sample(df[df['rank']==2].index,(int)(len(df[df['rank']==2])*fraction))])
	cl_rows.append(df.ix[random.sample(df[df['rank']==3].index,(int)(len(df[df['rank']==3])*fraction))])
	cl_rows.append(df.ix[random.sample(df[df['rank']==4].index,(int)(len(df[df['rank']==4])*fraction))])
	sdf=pd.concat(cl_rows)
	return sdf  
def dimReduction(df):
	std=StandardScaler().fit_transform(df)
	mean_vec = np.mean(std, axis=0)
	cov_mat = (std - mean_vec).T.dot((std - mean_vec))/(std.shape[0]-1)
	cov_mat = np.cov(std.T)
	eig_vals, eig_vecs = np.linalg.eig(cov_mat)
	eig_vals=sorted(eig_vals, reverse=True)
	#print eig_vals
	comp=0
	for vr in eig_vals:
		if(vr>1):
			comp+=1
	pca=PCA( n_components=comp)	
	return {'pca':pca,'eigen_values':eig_vals,'data':pd.DataFrame(pca.fit_transform(df)),'n_indim':comp}

def get_loadings(n,comp,df):
	i=0
	j=0
	sum=0
	temp=[]
	for var in comp:
		while (i<n):
			sum+=var[i]**2
			i+=1
		temp.append({'ssl':math.sqrt(sum),'var':j})
		j+=1
		sum=0
		i=0	
	temp.sort(key=operator.itemgetter('ssl'),reverse=True)
	print temp




def prepData():
	df=pd.read_csv("movie_metadata.csv",header=0)
	headers=["director_name","num_critic_for_reviews","duration","gross","genres","actor_1_name","movie_title","num_voted_users","plot_keywords","num_user_for_reviews","language","country","content_rating","budget","title_year","imdb_score"]
	crucialHeaders=["director_name","movie_title","gross","country","budget","imdb_score"]

	#There are around 800 "0"s in the "gross" attribute. This was either caused by (a) no gross number was found in certain movie page, or
	#(b) the response returned by scrapy http request returned nothing in short period of time.
	#So please make your own judgement when analyzing on this attribute.
	#There are around 908 directors whose "director_facebook_likes" attribute are 0. If somebody did analysis on "directory_facebook_like"
	#attribute, there could be some off, and say, the top10, or top50 directors could be inaccurate. 
	#Perhaps for some directors, facebook did not respond with reasonable result within short timespan (< 0.25 second) and returned "None"
	#in Python (translated to 0 in my code).

	#As of now, all 0 values from gross have been dropped
	#dropping unwanted columns, duplicates and null values (have not considered any facebook likes for removing null values)
	df1=df.drop(["movie_imdb_link","color","aspect_ratio","actor_3_facebook_likes","actor_3_name","facenumber_in_poster"],axis=1)
	df1=df1.drop_duplicates()
	#df1=df1.dropna(axis=0,subset=headers)   #if you want to drop all missing values, has ~3780 entries
	df1= df1.replace(0,'nan')
	df1=df1.dropna(axis=0,subset=crucialHeaders)   #drop missing values based on selected columns
	df1=df1[df1.country!="Official site"]

	#replacing same meaning values with one value
	df1=df1.replace("Not Rated","Unrated")
	df1=df1.replace("GP","PG")
	df1=df1.replace("M","PG")
	df1=df1[df1["country"]=="USA"]
	#converting categorical data to numerical (unsure what to do for genres,movie title, names and movie plot)
	x=list(df1.apply(set)["country"]) #budget and gross are adjusted already to US$
	for index,item in enumerate(x):
	    df1=df1.replace(item,index+1)
	    #print(item,index)

	y=list(df1.apply(set)["content_rating"])
	for index,item in enumerate(y):
	    df1=df1.replace(item,index+1)
	    #print(item,index)

	z=list(df1.apply(set)["language"])
	for index,item in enumerate(z):
	    df1=df1.replace(item,index+1)
	df1['language']=df1['language'].astype('category')
	df1['country']=df1['country'].astype('category')
	df1['genres']=df1['genres'].astype('category')
	df1['content_rating']=df1['content_rating'].astype('category')
	# df1 = parseGenres(df1)
	df1=rankMovies(df1)
	df1=classMovies(df1)
	df1=df1.dropna(axis=0,how='any')
	# ndf=df1.apply(pd.to_numeric,errors='coerce') #Each row among all columns will be ocnverted to numeric type names-> NAN issue with dates tho
	# ndf=ndf.drop(['title_year','director_name','actor_1_name','actor_2_name','genres','plot_keywords','movie_title','content_rating','director_facebook_likes','country','language'],1)
	# post_data={}
	# for col in list(df1):
	# 	post_data[col]=df1[col]
	# # print post_data['imdb_score']
	# return post_data
	return df1
	# ndf=ndf.dropna(axis=0,how='any')		
	#df1=createDirScore(df1)
	# createDirGross(df1)
	# return df1.to_json()
# prepData()
# post_data={
# 	'dataId':'moviedb1',
# 	'dataframe':prepData()
# }
# data = posts.find_one({'dataId': 'moviedb1'})
# # print data
# if(data is None):
# 	result=posts.insert_one(post_data)
# 	print('One post: {0}'.format(result.inserted_id)) 
# print prepData()

#sorted_x = sorted(dirdi.items(), key=operator.itemgetter(1))
#print sorted_x
# props= dimReduction(ndf)
# pca=props['pca']
# get_loadings(pca.n_components,pca.components_.tolist(),ndf)
# print list(ndf.columns.values)
# print props['n_indim']
#print len(sdf[sdf['country']=="Turkish"])


