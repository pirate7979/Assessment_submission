import pandas as pd

#1
def generate_car_matrix(df):
    matrix= df.pivot(index='id_1', columns='id_2', values='car')
    matrix= matrix.fillna(0)
    for i in matrix.columns:
        matrix.at[i, i]= 0
    return matrix

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
matrix_df= generate_car_matrix(df)
print('generate_car_matrix:')
print(matrix_df)


#2
def get_type_count(df):
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['high', 'medium', 'low'])
    counts = df['car_type'].value_counts().to_dict()
    sorted_counts = dict(sorted(counts.items()))
    return sorted_counts

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')   
print('get_type_count:')
print(get_type_count(df)) 


#3
def get_bus_indexes(df):
    mean= df['bus'].mean()
    indexes= df[df['bus'] > 2 * mean].index.tolist()
    indexes.sort()
    return indexes

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
index_df= get_bus_indexes(df)
print('get_bus_indexes:')
print(index_df)


#4
def filter_routes(df):
    avg= df.groupby('route')['truck'].mean()
    routes= avg[avg > 7].index.tolist()
    #routes= avg[avg > 7].tolist()
    routes.sort()
    return routes

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
route_df= filter_routes(df)
print('filter_routes:')
print(route_df)


#5
def multiply_matrix(df):
    new_df= df.copy()
    new_df= new_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    new_df= new_df.round(1)
    return new_df

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-1.csv')
multi_matrix_df= multiply_matrix(df)
print('multiply_matrix:')
print(multi_matrix_df)


#6
def time_check(df1):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df1['startDay'] = pd.Categorical(df1['startDay'], categories=day_order, ordered=True)
    df1['endDay'] = pd.Categorical(df1['endDay'], categories=day_order, ordered=True)

    df1['timestamp'] = pd.to_datetime(df1['startDay'].astype(str) + ' ' + df1['startTime'], errors='coerce')
    df1['end_timestamp'] = pd.to_datetime(df1['endDay'].astype(str) + ' ' + df1['endTime'], errors='coerce')

    problematic_rows = df[pd.to_datetime(df1['startDay'].astype(str) + ' ' + df1['startTime'], errors='coerce').isnull() |
                          pd.to_datetime(df1['endDay'].astype(str) + ' ' + df1['endTime'], errors='coerce').isnull()]

    if not problematic_rows.empty:
        print("Problematic rows:")
        print(problematic_rows)
        return pd.Series()

    time_check_result = (df1.groupby(['id', 'id_2'])
                         .apply(lambda x: (not x['timestamp'].empty) and
                                          (x['timestamp'].min().floor('D') == x['timestamp'].max().floor('D')) and
                                          (x['timestamp'].dt.dayofweek.nunique() == 7))
                         .reset_index(drop=True))

    return time_check_result

df1 = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-2.csv')
time_check_result = time_check(df1)
print(time_check_result)
