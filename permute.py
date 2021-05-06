import seaborn as sns
from mlxtend.evaluate import permutation_test

%%time
def perm_func(data, n0, n1):
    n = n1+n2
    idx_group0 = data.sample(n1).index
    idx_group1 = data.index ^ idx_group0
    mean_diff = data.iloc[idx_group1]['price_usd'].mean() - data.iloc[idx_group0]['price_usd'].mean()
    return mean_diff

for i in payments_users_table['platform'].unique():
    test_dat = payments_users_table[payments_users_table['platform']==i].groupby(['uid','test_group'])['price_usd'].sum().reset_index()
    n0,n1 = list(test_dat.groupby(['test_group'])['uid'].nunique().reset_index()['uid'])
    
    
    diffs = []
    for j in range(1000):
        diffs += [perm_func(test_dat, n0, n1)]
    group_means = test_dat.groupby('test_group')['price_usd'].mean().reset_index()
    real_diff = np.float64(group_means[group_means['test_group']==1]['price_usd']) - np.float64(group_means[group_means['test_group']==0]['price_usd'])
    plt.figure()
    sns.distplot(diffs)
    plt.axvline(real_diff, 0,5)
    print(i,'two-sided p_value: ', sum(list(map(abs,diffs))>=abs(real_diff))/len(diffs) )
  
  
  

agg_payments = payments_users_table.groupby(['uid','platform','test_group'])['price_usd'].sum().reset_index()
for i in agg_payments['platform'].unique():
    tmp_dat = agg_payments[agg_payments['platform']==i]
    p_value = permutation_test(tmp_dat[tmp_dat['test_group']==0]['price_usd'],
                               tmp_dat[tmp_dat['test_group']==1]['price_usd'],
                           method='approximate',
                           num_rounds=10000,
                           seed=0)
    print(i , p_value)
