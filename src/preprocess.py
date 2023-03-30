import pandas

df = pandas.read_csv('./data/data.csv')
df = df[['x','y']]
df.to_csv('./data/clean.csv', index=False)