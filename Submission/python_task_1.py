import pandas as pd

def generate_car_matrix(df):
  matrix= df.pivot(index='id_1', columns='id_2', value='cars')
  matrix= matrix.fillna(0)
  for i in matrix.columns:
    matrix.at[i, i]= 0
  return matrix

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
print(generate_car_matrix(df))


def get_type_count(df):
  df['car_type']= df.cut(df['cars'], bins=[-float(inf), 15, 25, float(inf)], labels=['low', 'medium', 'high'])
  counts= df['car_type'].value_counts().to_dict()
  counts= dict(sorted(counts.item()))

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
print(get_type_count(df)) 


def get_bus_indexes(df):
  mean= df['bus'].mean()
  indexes= df[df['bus'] > 2 * mean].index.tolist()
  indexes.sort()
  return indexes

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
print(get_bus_indexes(df))


def filter_routes(df):
  avg= df.groupby('truck')['route'].mean()
  #routes= avg[avg > 7].index.tolist()
  routes= avg[avg > 7].tolist()
  routes.sort()
  return(filter_routes(df))

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
print(filter_routes(df))


def multiply_matrix(matrix):
  new_df= matrix.copy()
  new_df= new_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
  new_df= new_df.round(1)
  return new_df

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
print(multiply_matrix(matrix))


def time_check(df):
  
  







