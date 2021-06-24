from utils import *

import matplotlib.pyplot as plt

data = pd.read_csv('mem100.csv', delimiter = ",")#.drop([136])

cmap = { 'wo' : 'red', 'ro' : 'blue', 'rw': 'green' }
#Mem100 Mem80 Mem75 Mem60 Mem50 MemMix
def plot_by_mode(n, p, a):
    df = mode(n, pattern(p, access(a, data))).sort_values('ws')

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('{}/{} {}'.format(n, p ,a))

    for ratio in ['ro', 'rw', 'wo']:
        d = rw_ratio(ratio, df)[['ws','ltc','ltc_d']]
        ax.plot(d['ws']/1000, d['ltc'], label=ratio, color=cmap[ratio])
        ax.plot(d['ws']/1000, d['ltc_d'], linestyle=':', color=cmap[ratio], label="Δ")

    ax.legend(loc='upper left')
    ax.set_xlabel('Working set (GB)')
    ax.set_ylabel('Latency (ns)')
    ax.set_ylim([0, 300])
    ax.set_xlim([32, 70])
    return df

for n in ['MemMixApp50', 'MemOnly50']:#, 'MemMix50'  'Mem75', 'Mem60', 'Mem50', 'Mem24']:
    df = plot_by_mode(n, 'uniform', 'touch')
