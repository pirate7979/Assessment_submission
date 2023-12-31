import pandas as pd

#1
def calculate_distance_matrix(df):
    data = df

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
print('resulting_matrix_df:')
resulting_matrix_df = calculate_distance_matrix(df)
print(resulting_matrix_df)
  

#2
def unroll_distance_matrix(distance_matrix):
    unrolled_dataframe = (distance_matrix.stack()
                          .reset_index()
                          .rename(columns={'level_0': 'id_start', 'level_1': 'id_end', 0: 'distance'})
                          .query('id_start != id_end'))

    return unrolled_dataframe

unrolled_dataframe = unroll_distance_matrix(resulting_matrix)
print('unrolled_dataframe:')
print(unrolled_dataframe)


#3
def find_ids_within_ten_percentage_threshold(df, ref_value):
    ref_df= result_df[result_df['id_start']==ref_value]
    avg_dist= result_df['distance'].mean()
    threshold= 0.1 * avg_dist
    within_threshold= result_df[(result_df['distance'] >= (avg_dist - threshold)) & 
                                (result_df['distance'] <= (avg_dist + threshold))]
    return within_threshold

df= unrolled_dataframe
ref_value= 1001400
results_id_df= find_ids_within_ten_percentage_threshold(df, ref_value)
print('results_id:')
print(results_id_df)


#4
def calculate_toll_rate(df):
    new_df= df.copy()
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        new_df[vehicle_type] = new_df['distance'] * rate_coefficient
    return new_df

df= unrolled_dataframe
toll_df = calculate_toll_rate(df)
print('roll_df:')
print(toll_df)


#5
def calculate_time_based_toll_rates(df):
    nw_df= df.copy()
    time_ranges_weekdays = [(datetime.time(0, 0, 0), datetime.time(10, 0, 0)),
                            (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
                            (datetime.time(18, 0, 0), datetime.time(23, 59, 59))]

    time_ranges_weekends = [(datetime.time(0, 0, 0), datetime.time(23, 59, 59))]

    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7

    
    nw_df['start_day'] = nw_df['timestamp'].dt.strftime('%A')
    nw_df['start_time'] = nw_df['timestamp'].dt.time
    nw_df['end_day'] = nw_df['end_timestamp'].dt.strftime('%A')
    nw_df['end_time'] = nw_df['end_timestamp'].dt.time

    for idx, (start, end) in enumerate(time_ranges_weekdays):
        mask = (nw_df['start_time'] >= start) & (nw_df['start_time'] <= end) & (nw_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        nw_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factors_weekdays[idx]

    for start, end in time_ranges_weekends:
        mask = (nw_df['start_time'] >= start) & (nw_df['start_time'] <= end) & (nw_df['start_day'].isin(['Saturday', 'Sunday']))
        nw_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor_weekends
    return nw_df

df= results_id
toll_rate_df = calculate_time_based_toll_rates(df)
print('toll_rate_df:')
print(toll_rate_df)
