#!/usr/bin/env python


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

df = None

#Read in dataset
def read_dataset():
    global df
    df = pd.read_csv("atussum_1121-reduced.csv", index_col=False)
    return df

#Extract means from data set
def get_means():
    means = df.mean().to_frame().reset_index() # obtain mean values
    means.columns = ['Category', 'Mean']
    means = means[means['Category'].str.contains('t')] # drop everything except the category information
    means = means.sort_values(by=['Mean'], ascending = False) # sort in descending order of mean values, so that the greatest values are at the head of the data frame
    means = means.reset_index().drop('index', axis = 1)
    means['Cumulative'] = [sum(means['Mean'].to_list()[0:i+1]) for i in range(len(means))] # Create a new column for cumulative time spent

    stdlist=[]
    varlist=[]
    for i in df.columns:
       if('t' in i):
            stdlist.append(df[i].std())
            varlist.append(df[i].var())


    means['std'] = stdlist
    means['var'] = stdlist
    
    return means


#Generate and display heatmap of standard deviations
def get_heatmap():

    stddev = get_means()

    hc_map = pd.DataFrame()
    hc_bar = pd.DataFrame()

    hc_map['cat1'] = []
    hc_map['cat2'] = []
    hc_map['std'] = []

    hc_bar['cat'] = []
    hc_bar['perc'] = []

    for i in stddev.Category:
        mean_i = float(stddev[stddev["Category"] == i]['Mean'])
        std_i  = float(stddev[stddev["Category"] == i]['std'])
        var_i  = float(stddev[stddev["Category"] == i]['var'])
        
        hc_bar.loc[-1] = [i, mean_i]
        hc_bar.index = hc_bar.index+1
        for j in stddev.Category:
            mean_j = float(stddev[stddev["Category"] == j]['Mean'])
            std_j  = float(stddev[stddev["Category"] == j]['std'])
            var_j  = float(stddev[stddev["Category"] == j]['var'])
            
            std_avg = (std_i + std_j)/2
            
            #Calculate average standard deviation
            var_avg = math.sqrt((var_i + var_j)/2)
            
            total = mean_i + mean_j
            
            if(i == j):
                total = mean_i
                
            p_i = (mean_i / (total))
            p_j = (mean_j / (total))
            
            p_std = var_avg 

            hc_map.loc[-1] = [i, j, p_std]
            hc_map.index = hc_map.index+1

    hc_map
    hc_map = hc_map.pivot("cat1", "cat2", "std")

    sns.set(font_scale=1.1)
    plt.figure()
    hm = sns.heatmap(data=hc_map, cmap="crest", annot=True, square=False)
    hm.set(xlabel="", ylabel="")

    hm.xaxis.tick_top()
    plt.show()


#Print table of values used to hand draw node-link graph
def print_datagroups(df):

    #Filter columns out
    filt = df.columns.str.startswith('t')
    df = df.loc[:,filt]
    
    #Group layout for node link graph
    #A
    #6: t10, t09, t08, t16, t04, t15, t14, t50, t06, t13, t07
        #A
        #3: t10, t09, t08, t16, t04, t15

        #B
        #5: t14, t50, t06, t13, t07
            #A
            #4 t14, t50, t06, t13
                #A
                #2 t14, t50
                   #A
                   #1 t14

                   #B
                   #1 t50

                #B       
                #2 t06, t13
                    #A
                    #1 t06

                    #B
                    #1 t13
            #B
            #1 t07
    
    #B
    #4: t03, t11, t18, t02, 
        #A
        #2 t03, t11
            #A
            #1 t03

            #B
            #1 t11
        #B
        #2 t18, t02
            #A
            #1 t18

            #B
            #1 t02
    
    #C
    #3: t05, t12, t01
        #A
        #1 t05

        #B
        #1 t12

        #C
        #1 t01
    
    #Create new categories in dataset
    df['ALL'] = df['t10'] + df['t09'] + df['t08'] + df['t16'] + df['t04'] + df['t15'] + df['t14'] + df['t50'] + df['t06'] \
            + df['t13'] + df['t07'] + df['t03'] + df['t11'] + df['t18'] + df['t02'] + df['t05'] + df['t12'] + df['t01']

    df['A'] = df['t10'] + df['t09'] + df['t08'] + df['t16'] + df['t04'] + df['t15'] + df['t14'] + df['t50'] + df['t06'] + df['t13'] + df['t07']
    df['AA'] = df['t10'] + df['t09'] + df['t08'] + df['t16'] + df['t04'] + df['t15']
    df['AB'] = df['t14'] + df['t50'] + df['t06'] + df['t13'] + df['t07']

    df['B'] = df['t03'] + df['t11'] + df['t18'] + df['t02']
    df['BA'] = df['t03'] + df['t11']
    df['BB'] = df['t18'] + df['t02']

    df['C'] = df['t05'] + df['t12'] + df['t01']
    df['CA'] = df['t05'] 
    df['CB'] = df['t12']
    df['CC'] = df['t01']

    means = df.mean().to_frame().reset_index() # obtain mean values
    means.columns = ['Category', 'Mean']

    std = df.std().to_frame().reset_index() # obtain std dev values
    std.columns = ['Category', 'std']
    
    quantiles = (df.quantile([0.25, 0.5, 0.75, 0.99]).transpose().reset_index())
    quantiles.columns = ['Category', '0.25', '0.5', '0.75', '0.99']

    merged = means.merge(std, left_on='Category', right_on='Category')
    merged = merged.merge(quantiles, left_on='Category', right_on='Category')
    print(merged)


def get_barchart():

    stddev = get_means()
    
    hc_map = pd.DataFrame()
    hc_bar = pd.DataFrame()
    
    hc_map['cat1'] = []
    hc_map['cat2'] = []
    hc_map['std'] = []
    
    hc_bar['cat'] = []
    hc_bar['perc'] = []

    for i in stddev.Category:
        mean_i = float(stddev[stddev["Category"] == i]['Mean'])
        std_i  = float(stddev[stddev["Category"] == i]['std'])
        var_i  = float(stddev[stddev["Category"] == i]['var'])
        
        hc_bar.loc[-1] = [i, mean_i]
        hc_bar.index = hc_bar.index+1
        for j in stddev.Category:
            mean_j = float(stddev[stddev["Category"] == j]['Mean'])
            std_j  = float(stddev[stddev["Category"] == j]['std'])
            var_j  = float(stddev[stddev["Category"] == j]['var'])
            
            std_avg = (std_i + std_j)/2
    
            var_avg = math.sqrt((var_i + var_j)/2)
            
            total = mean_i + mean_j
            
            if(i == j):
                total = mean_i
                
            p_i = (mean_i / (total))
            p_j = (mean_j / (total))
            
            p_std = var_avg 
    
            
            hc_map.loc[-1] = [i, j, p_std]
            hc_map.index = hc_map.index+1


    sns.set(font_scale=1.1, rc={'axes.facecolor':'white'})
    plt.figure()
    plt.hlines(y=[1440, 1440/2, 1440/4], xmin=-100, xmax=100, color='k', linestyle='-')
    plt.ylim(0, 1440/2 + 10)
    sns.barplot(data=hc_bar, x='cat', y='perc', order=['t01', 't02', 't03', 't04', 't05', 't06', 't07', 't08', 't09', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't18', 't50'])
    plt.show()



if __name__ == "__main__":
    read_dataset()
    get_heatmap()
    get_barchart()
    
    print_datagroups(read_dataset())
