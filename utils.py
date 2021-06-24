import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def concat(fields, fd):
    return fd[fields].T.values

def only(name, value, df):
     return df[df[name] == value].drop(columns=[name])

def pool(name, df):
     return df[df['pool'] == name].drop(columns=["pool"])

def mode(name, df):
     return df[df['mode'] == name].drop(columns=['mode'])

def access(name, df):
     return df[df['access'] == name].drop(columns=['access'])

def rw_ratio(ratio, df):
    if type(ratio) == str:
        if   ratio == 'wo' : v = 0
        elif ratio == 'rww': v = 33
        elif ratio == 'rw' : v = 50
        elif ratio == 'rrw': v = 66
        elif ratio == 'ro' : v = 100
        else: raise Exception('Unknown ratio "{}"'.format(ratio))
    else:
        v = ratio
    return df[df['rw_ratio'] == v].drop(columns=["rw_ratio"])

def ws(v, df):
    return df[df['ws'] == v].drop(columns=['ws'])

def threads(i, df):
    return df[df['threads'] == i].drop(columns=['threads'])

def pattern(name, df):
    return df[df['pattern'] == name].drop(columns=['pattern'])

def merge_ratios(fd, ratios=['ro','rrw', 'rw', 'rww', 'wo']):
    m = fd["threads"].drop_duplicates()
    for n in ratios:
        t = rw_ratio(n, fd).rename(columns={'ltc':n,'ltc_d':n+'_d'})
        m = pd.merge(m, t)
    return m

