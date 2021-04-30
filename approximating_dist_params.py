import pymc3 as pm


def plot_traces(trcs, varnames=None):
    '''Plot traces with overlaid means and values'''

    nrows = len(trcs.varnames)
    if varnames is not None:
        nrows = len(varnames)

    ax = pm.traceplot(trcs, var_names=varnames, figsize=(12, nrows*1.4),
                      lines=tuple([(k, {}, v['mean'])
                                   for k, v in pm.summary(trcs, varnames=varnames).iterrows()]))

    for i, mn in enumerate(pm.summary(trcs, varnames=varnames)['mean']):
        ax[i, 0].annotate('{:.2f}'.format(mn), xy=(mn, 0), xycoords='data',
                          xytext=(5, 10), textcoords='offset points', rotation=90,
                          va='bottom', fontsize='large', color='#AA0022')
                          
                          
with pm.Model() as model:
    mu = pm.Uniform('mu', lower=0, upper=1)
    sigma = pm.Uniform('sigma', lower=0, upper=2)
    
    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=np.random.normal(0.2, 1.1, 10000))    

    trace = pm.sample(1000, tune=1000, cores=2)# Produce normally distributed samples
    
    
# Produce normally distributed samples
np.random.seed(1618)
size = 5000
mu = 23
sigma = 7
samples = np.random.normal(mu, sigma, size)

# Set censoring limits
high = 28
low = 0

# Censor samples
censored = samples[(samples > low) & (samples < high)]


# Visualize uncensored and censored data
_, axarr = plt.subplots(ncols=2, figsize=[16, 4], sharex=True, sharey=True)
for i, data in enumerate([samples, censored]):
    sns.distplot(data, ax=axarr[i])
axarr[0].set_title('Uncensored')
axarr[1].set_title('Censored')
plt.show()
    
    
# Produce normally distributed samples
np.random.seed(1618)
size = 5000
mu = 23
sigma = 7
samples = np.random.normal(mu, sigma, size)

# Set censoring limits
high = 28
low = 0

# Censor samples
censored = samples[(samples > low) & (samples < high)]


# Visualize uncensored and censored data
_, axarr = plt.subplots(ncols=2, figsize=[16, 4], sharex=True, sharey=True)
for i, data in enumerate([samples, censored]):
    sns.distplot(data, ax=axarr[i])
axarr[0].set_title('Uncensored')
axarr[1].set_title('Censored')
plt.show()



# Uncensored model
with pm.Model() as uncensored_model:
    mu = pm.Normal('mu', mu=0., sigma=(high - low) / 2.)
    sigma = pm.HalfNormal('sigma', sigma=(high - low) / 2.)
    observed = pm.Normal('observed', mu=mu, sigma=sigma, observed=samples)
    trace = pm.sample(1000, tune=1000, cores=2)
    
    
pm.traceplot(trace)





# CENSORED MODEL
# Import the log cdf and log complementary cdf of the normal Distribution from PyMC3
from pymc3.distributions.dist_math import normal_lcdf, normal_lccdf

# Helper functions for unimputed censored model
def left_censored_likelihood(mu, sigma, n_left_censored, lower_bound):
    ''' Likelihood of left-censored data. '''
    return n_left_censored * normal_lcdf(mu, sigma, lower_bound)


def right_censored_likelihood(mu, sigma, n_right_censored, upper_bound):
    ''' Likelihood of right-censored data. '''
    return n_right_censored * normal_lccdf(mu, sigma, upper_bound)
    
    
# Unimputed censored model
n_right_censored = len(samples[samples >= high])
n_left_censored = len(samples[samples <= low])
n_observed = len(samples) - n_right_censored - n_left_censored

with pm.Model() as unimputed_censored_model:
    mu = pm.Normal('mu', mu=0., sigma=(high - low) / 2.)
    sigma = pm.HalfNormal('sigma', sigma=(high - low) / 2.)

    observed = pm.Normal(
        'observed',
        mu=mu,
        sigma=sigma,
        observed=censored,
    )

    right_censored = pm.Potential(
        'right_censored',
        right_censored_likelihood(mu, sigma, n_right_censored, high)
    )
    trace = pm.sample(1000, tune=1000, cores=2)
    
    
pm.traceplot(trace)
