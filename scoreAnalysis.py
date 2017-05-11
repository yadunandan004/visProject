#here we have to interpret movie gross based on quality
import numpy as np
import pandas as pd
import preprocessing
def RankvProfit(df1):
	#we try to estimate the average 
	#Class indicated by rank column
	res={}
	# print df1[df1['budget'] == 0]
	group=df1.groupby(['rank'])
	grossgrp=group['gross'].sum()
	budgetgrp=group['budget'].sum()
	for i in range(1,5):
		# print len(group.ix[i])
		gross=grossgrp.ix[i]
		budget=budgetgrp.ix[i]
		res[i]=int(gross-budget)
	return res
def BudgetvsProfit(df1):
	#we try to estimate the relationship budget and gross
	res={}
	group=df1.groupby(['class'])
	grossgrp=group['gross'].sum()
	budgetgrp=group['budget'].sum()
	for i in range(1,5):
		# print len(group.ix[i])
		gross=grossgrp.ix[i]
		budget=budgetgrp.ix[i]
		res[i]=int(gross-budget)
	return res
df1=preprocessing.prepData()
print BudgetvsProfit(df1)