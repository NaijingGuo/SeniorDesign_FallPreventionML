'''
data processing - 
    last column is label, 0 for no fall, 1 for fall
    each instance last 2s, 1s overlap w/ previous instance
    20 x values, 20 y values, 20 z values

    label everything as no fall, then manually change it
'''

import pandas as pd
def read_no_fall(file_name):
    trial_1 = pd.read_excel(file_name)
    trial_1 = trial_1.iloc[:, :4] # get rid of note, leave time + data
    index = 0
    data = []
    while index < len(trial_1)-21: 
        temp = []
        for j in range(20):
            temp.append(trial_1.iloc[index+j, 1]) # x value
        for j in range(20):
            temp.append(trial_1.iloc[index+j, 2]) # y value
        for j in range(20):
            temp.append(trial_1.iloc[index+j, 3]) # z value
        temp.append(0) # label as no fall
        data.append(temp)
        index += 10
    return data

def fall(temp, start,end):
    for i in range(start, end):
        temp[i][-1] = 1
    return temp

data = []
file_name = "raw_data/IMU_trial1_Brian_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp
file_name = "raw_data/IMU_trial2_Brian_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp
file_name = "raw_data/IMU_trial3_Brian_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp
file_name = "raw_data/IMU_trial4_Brian_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp
file_name = "raw_data/IMU_trial5_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 2,9)
fall(temp, 15, 25)
data = data + temp
file_name = "raw_data/IMU_trial6_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 4,13)
data = data + temp
file_name = "raw_data/IMU_trial7_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 1,13)
data = data + temp

## convert to df after reading all data
df = pd.DataFrame(data)
df.to_csv('data_df.csv')    

