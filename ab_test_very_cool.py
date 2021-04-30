## Просто кустарное определение размера группы
import scipy.stats as st
k = 1.2
N = 32400
CONFIG = {'platform':'uni', 'q':st.norm.ppf(0.90)}


arpu_std =  cr_arpu[cr_arpu['platform']==CONFIG['platform']]['price_usd'].std()
vals = [['static_ARPU', cr_arpu[cr_arpu['platform']==CONFIG['platform']]['price_usd'].mean()]]


for name, val in vals:

    if val + CONFIG['q']*arpu_std/N**0.5 < (val*k) - CONFIG['q']*arpu_std/N**0.5:
        is_success = True
    else:
        is_success = False
    print(name, is_success, 'a=',  val,  'b=',  val*k , 'diff=', (Q1*arpu_std/N**0.5))
    
    
    
## Хиквадрат
for i in static_ab_stat_ARPU['platform'].unique():
    tmp_dat = static_ab_stat_ARPU[static_ab_stat_ARPU['platform']==i]
    obs = np.array([
                [                 
                 int(tmp_dat[tmp_dat['test_group']=='test_A']['uid']) - int(tmp_dat[tmp_dat['test_group']=='test_A']['payers']),
                 int(tmp_dat[tmp_dat['test_group']=='test_A']['payers']),
                ],
                [
                 int(tmp_dat[tmp_dat['test_group']=='test_G']['uid']) - int(tmp_dat[tmp_dat['test_group']=='test_G']['payers']),
                 int(tmp_dat[tmp_dat['test_group']=='test_G']['payers'])
                ]])
    chi2, p, dof, expected = scipy.stats.chi2_contingency(obs)
    print(i ,obs, p)
