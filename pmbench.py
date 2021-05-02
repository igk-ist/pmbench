# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def concat(fields, fd):
    return fd[fields].T.values

def pool(name, df):
     return df[df['pool'] == name].drop(columns=["pool"])

def rw_ratio(ratio, df):
     return df[df['rw_ratio'] == ratio].drop(columns=["rw_ratio"])

def ws(v, df):
    return df[df['ws'] == v].drop(columns=['ws'])

def threads(i, df):
    return df[df['threads'] == i].drop(columns=['threads'])

def merge_ratios(fd, ratios=[
            (100, 'ro'),
            (66, 'rrw'),
            (50, 'rw'),
            (33, 'rww'),
            (0, 'wo')]):
    m = fd["threads"]#.drop_duplicates()
    for r, n in ratios:
        t = rw_ratio(r, fd).rename(columns={'ltc':n,'ltc_d':n+'_d'})
        m = pd.merge(m, t)
    return m

def plot_ratios(fd, axs):
    fd = merge_ratios(fd)
    fd.plot(
        ax=axs,
        x='threads',
        ylabel='latency (ns)',
        y=['ro','rrw','rw','rww','wo'],
        yerr=concat(['ro_d','rrw_d','rw_d','rww_d','wo_d'], fd))


# %%
data = pd.read_csv('pmbench.csv', delimiter = ",")
data

# %%
apps = data[
    (data["offset"] == "uniform") &
    (data['pattern'] == "random") &
    (data['mode'] == "App") &
    True].drop(columns=["offset","pattern","mode","sz","ws","date"])

apps_fsdax = pool('fsdax', apps)
apps_ram_l = pool('ram_l', apps)
apps_ram_r = pool('ram_r', apps)
apps_pm_r  = pool('pm_r',  apps)
apps_pm_l  = pool('pm_l',  apps)

# %%
fig = plt.figure(figsize=(20,15))
for v, n, i in [
        (apps_pm_l, "Apps PM local", 1),
        (apps_fsdax, "Apps fsdax (local)", 2),
        (apps_pm_r, "Apps PM rmote", 3),
        (apps_ram_l, "Apps RAM local", 4),
        (apps_ram_r, "Apps RAM remote", 6)]:
    ax = fig.add_subplot(2, 3, i)
    ax.set_title(n)
    plot_ratios(v, ax)

# %%

mem100 = data[
    (data['mode'] == 'Mem100') &
    True].drop(columns = [
        'date',
        'pool',
        'offset',
        'pattern',
        'mode',
        'sz',
        ]).sort_values(["threads","ws"])

def plot_mem_by_thread():
    df = merge_ratios(ws(128, mem100))
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Mem100: access latency by thread number')
    df.plot(x = 'threads',
            y = ['ro', 'rw', 'wo'],
            yerr=concat(['ro_d', 'rw_d', 'wo_d'], df),
            ylabel = 'latency (ns)',
            ax = ax)

plot_mem_by_thread()

# %%

def plot_mem_latency_by_ws(n, ax):
    threads(n, merge_ratios(mem100)).plot(ax = ax, x='ws', y=['ro','rw','wo'])

#def main():
#    fig = plt.figure()
#    for n, i in [(1, 1), (2, 2), (4, 3), (8, 4)]:
#        ax = fig.add_subplot(2,2,i)
#        plot_mem_latency_by_ws(n, ax)

threads(1, rw_ratio(0, mem100)).plot(x='ws', y='ltc')

#d = rw_ratio(0, mem100)
#
#fig = plt.figure()
#ax = fig.add_subplot()
#cb = ax.scatter(d['ws'], d['ltc'] , c=d['threads'])
#plt.colorbar(cb)
#
#def plot_thread(n, df):
#    v = threads(n, df)
#    ax.plot(v['ws'], v['ltc'], c=cb.to_rgba(n))

a = ws(32768, rw_ratio(0, mem100)).plot(x='threads', y='ltc', yerr='ltc_d')
a.set_xticks([2,4,6,8,10,16,32])

#plot_ratios(mem100)
