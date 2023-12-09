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
