import pandas as pd

def calculate_distance_matrix(df):
    unique_ids = sorted(set(data['id_start'].unique()) | set(data['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    distance_matrix = distance_matrix.fillna(0)

    for _, row in data.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[id_start, id_end] = distance
        distance_matrix.at[id_end, id_start] = distance  

    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, j] == 0 and i != j:
                    if distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix

df = pd.read_csv(r'C:\/Users\Acer\Desktop\ML\Untitled Folder 1\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv')
resulting_matrix = calculate_distance_matrix('dataset-3.csv')
print(resulting_matrix)
  
  
def unroll_distance_matrix(distance_matrix):
    unrolled_dataframe = (distance_matrix.stack()
                          .reset_index()
                          .rename(columns={'level_0': 'id_start', 'level_1': 'id_end', 0: 'distance'})
                          .query('id_start != id_end'))

    return unrolled_dataframe

unrolled_dataframe = unroll_distance_matrix(resulting_matrix)
print(unrolled_dataframe)


def find_ids_within_ten_percentage_threshold(df, ref_value):
    ref_df= result_df[result_df['id_start']==ref_value]
    avg_dist= result_df['distance'].mean()
    threshold= 0.1 * avg_dist
    within_threshold= result_df[(result_df['distance'] >= (avg_dist - threshold)) & 
                                (result_df['distance'] <= (avg_dist + threshold))]
    return within_threshold

df= unrolled_dataframe
ref_value= 1001400
results_id= find_ids_within_ten_percentage_threshold(df, ref_value)
print(results_id)


def calculate_toll_rate(df):
    new_df= df.copy()
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        new_df[vehicle_type] = new_df['distance'] * rate_coefficient
    return new_df

df= unrolled_dataframe
toll_rate_df = calculate_toll_rate(df)
print(toll_rate_df)









