#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use pandas dataframes to retrieve data from YahooFinance and process into
matrix form using numpy
"""

import pandas as pd
import numpy as np
import yfinance as yf
from user import *
from prints import *


def get_prices(begin,end,tickers):
    """
    input string dates, then list of string tickers
    scrapes yahoo finance
    returns a df of prices
    """
    df= pd.DataFrame() #initialize empty DF, iterate each ticker's data in
    for ticker in tickers:
        Data = yf.Ticker(ticker)
        tickerDf = Data.history(period='1d', start=begin, end=end)
        df[ticker]=tickerDf['Close']
    if df.isnull().values.any():  # if any stock prices aren't available:
        Tickers_with_missing_values = df.columns[df.isna().any()].tolist() # find those with missing values
        first_date = df.dropna().iloc[:1].index[0].strftime("%Y-%m-%d %H:%M")[:-6] # beginning date all tickers values available
        last_date = df.dropna().iloc[-1:].index[-1].strftime("%Y-%m-%d %H:%M")[:-6]
        print_missing_tickers(Tickers_with_missing_values,first_date,last_date) # print which were missing and when all are listed
        # user decides whether to begin analysis when all tickers' values are listed
        # or remove tickers with any missing values
        s_or_r = skip_or_remove()
        if s_or_r == 'skip':
            df=df.dropna(axis=0) #removes all rows with nan values
            begin = first_date# change starting date
            end = last_date
        else:
            df = df.dropna(axis=1) #removes all columns with nan values
            # remvoe tickers with missing values from list:
            [tickers.remove(Tickers_with_missing_values[i]) for i in range(len(Tickers_with_missing_values))]
    return df,tickers,begin,end
    

def get_returns(prices):
    """
    Input dataframe of adj close prices
    returns a df of returns
    """
    returns = prices.pct_change()
    return returns


def returns_to_np(prices):
    """
    Input a dataframe of  prices
    returns an array of returns
    """
    df = prices.pct_change()
    array=np.zeros(len(df))
    for i in range(len(df)):
        array[i]=df.iloc[i]
    return array


def take_mean_of_returns(returns):
    """
    Input dataframe of returns
    returns a df
    """
    return returns.mean()


def np_take_mean_of_returns(returns):
    """
    input dataframe of returns, takes mean
    returns a matrix of means
    """
    df = take_mean_of_returns(returns)
    array=np.zeros(len(df))
    for i in range(len(df)):
        array[i]=df.iloc[i]
    return array


def get_std(returns):
    """
    input df of returns
    returns df of sample standard deviations
    """
    return returns.std()


def std_to_np(returns):
    """
    input df of returns 
    returns array of sample standard deviations
    """
    std=get_std(returns)
    return np.array(std)


def get_var(returns):
    """
    input a df of returns
    returns a df of variances
    """
    var=returns.var()
    return var


def var_to_np(returns):
    """
    input df of returns
    return array of variances
    """
    var=get_var(returns)
    array=np.zeros(len(var))
    for x in range(len(var)):
        array[x]=var[x]
    return array


def get_covar(returns):
    """
    input dataframe of returns
    returns df of covar
    """
    df = returns.cov()
    return df 


def covar_to_np(returns):
    """
    input dataframe of returns
    returns matrix of covar
    """
    df = returns.cov()
    array=np.zeros((len(df),len(df.iloc[0])))
    for i in range(len(df)):
        for j in range(len(df.iloc[0])):
            array[i][j]=df.iloc[i][j]
    return array


def get_corrmat():
    # initial ui
    start1,end1,tickers = get_portfolio_parameters()
    prices=get_prices(start1,end1,tickers)
    returns=get_returns(prices)
    return returns.corr()
    
    