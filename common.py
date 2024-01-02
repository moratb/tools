pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

def flatten_columns(df):
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

## to start of week
df['dt_s'] = df['created_at'] - df['created_at'].apply(lambda x:dt.timedelta(x.weekday()))

## to start of month
df['dt_s'] = df['created_at'].apply(lambda x : x.replace(day=1))

## tsfix
for col in ['fsub_ts','create_ts','sub_ts','cancel_ts','end_ts']:
    df[col] = pd.to_datetime(df[col]).apply(lambda x:x.replace(tzinfo=None))
