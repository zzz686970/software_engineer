## groupby and count
```py
df.groupby(['col1', 'col2'])['col3'].count()

df.groupby(['col1', 'col2']).size()
```



```py
## pd.__version__ >= 1.1
## faster performance

df.value_counts(['col1', 'col2'])

```

## check data types
```py
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

is_string_dtype(df['A'])


## select certain dtype
df.select_dtypes(include=['float64']).apply(func1)

df.select_dtypes(exclude=['string', 'object']).apply(func2)


df['A'].dtype 

isinstance(df['A'], np.int64)

df.select_dtypes('number')


```


## combine two columns

```py
## way 1
df['col_new'] = df['col1'] + df['col2']

df['col_new'] = df[['col1', 'col2']].agg('-'.join, axis = 1)

## small dataset
[''.join(i) for i in zip(df['year'].map(str), df['quarter'])]

df.year.str.cat(df.quarter)

## large dataset
df['year'].astype(str) + df['quarter']



In [107]: %timeit df['Year'].astype(str) + df['quarter']
10 loops, best of 3: 131 ms per loop

In [106]: %timeit df['Year'].map(str) + df['quarter']
10 loops, best of 3: 161 ms per loop

In [108]: %timeit df.Year.str.cat(df.quarter)
10 loops, best of 3: 189 ms per loop

In [109]: %timeit df.loc[:, ['Year','quarter']].astype(str).sum(axis=1)
1 loop, best of 3: 567 ms per loop

In [110]: %timeit df[['Year','quarter']].astype(str).sum(axis=1)
1 loop, best of 3: 584 ms per loop

In [111]: %timeit df[['Year','quarter']].apply(lambda x : '{}{}'.format(x[0],x[1]), axis=1)
1 loop, best of 3: 24.7 s per loop

```

## drop value
```py
import perfplot, numexpr

def bi1(df):
    return df[df['R1'].values != 1]

def bi2(df):
    return df[df['R1'] != 1]

def drop1(df):
    return df.drop(df[df["R1"] == 1].index)

def drop2(df):
    return df.drop(df.index[df["R1"] == 1])

def drop3(df):
    return df.drop(df.loc[df['R1'] == 1].index)

def drop4(df):
    return df.drop(np.where(df["R1"] == 1)[0])


def ne(x):
    x = x['R1'].values
    return x[numexpr.evaluate('(x != 1)')]

def q(x):
    return x.query('R1 != 1')

def ev(x):
    return x[x.eval('R1 != 1')]


def make_df(n):
    df = pd.DataFrame({'R1':np.random.randint(100, size=n)})
    return df

perfplot.show(
    setup=make_df,
    kernels=[bi1, bi2,drop1,drop2,drop3,drop4,ne,q,ev],
    n_range=[2**k for k in range(2, 25)],
    logx=True,
    logy=True,
    equality_check=False,
    xlabel='len(df)')    
```


