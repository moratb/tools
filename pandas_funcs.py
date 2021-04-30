users_reached_kop = rm_energy_outcome_fs.groupby('reg_date').agg({
                                                               'uid':'nunique',
                                                               'resource':'count',
                                                               'time_diff':['mean','median'],
                                                               'time_diff': {'mean':'mean',
                                                                             'q10': lambda x: x.quantile(0.1),
                                                                             'q25': lambda x: x.quantile(0.25),
                                                                             'q50': lambda x: x.quantile(0.50),
                                                                             'q75': lambda x: x.quantile(0.75),
                                                                             'q90': lambda x: x.quantile(0.90)}}).reset_index()


df.groupby('uid').filter(lambda x: x['test_group'].nunique() == 1).groupby('test_group')['uid'].nunique()
