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
            if trial_1.iloc[index+j, 1] != "-":
                temp.append(trial_1.iloc[index+j, 1]) # x value
            else:
                temp.append(0)
        for j in range(20):
            if trial_1.iloc[index+j, 2] != "-":
                temp.append(trial_1.iloc[index+j, 1]) # y value
            else:
                temp.append(0)
        for j in range(20):
            if trial_1.iloc[index+j, 3] != "-":
                temp.append(trial_1.iloc[index+j, 1]) # z value
            else:
                temp.append(0)
        temp.append(0) # label as no fall
        data.append(temp)
        index += 10
    return data

def fall(temp, start,end):
    if end == None:
        end =len(temp)
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
fall(temp, 15, None)
data = data + temp

file_name = "raw_data/IMU_trial6_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 4,None)
data = data + temp

file_name = "raw_data/IMU_trial7_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 1, None)
data = data + temp

file_name = "raw_data/IMU_trial8_Brian_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial9_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp,7, 18)
fall(temp, 23, None)
data = data + temp

file_name = "raw_data/IMU_trial10_Brian_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 7, 18)
data = data + temp

file_name = "raw_data/IMU_trial1_JA_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

# file_name = "raw_data/IMU_trial2_JA_no_fall.xlsx"
# temp = read_no_fall(file_name)
# data = data + temp

file_name = "raw_data/IMU_trial3_JA_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 15, 19)
data = data + temp

file_name = "raw_data/IMU_trial1_NG_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial2_NG_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp
fall(temp, 6, 23)

file_name = "raw_data/IMU_trial3_NG_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 4, 13)
fall(temp, 15, 22)
data = data + temp

file_name = "raw_data/IMU_trial1_AH_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 5, 8)
fall(temp, 12, 22)
data = data + temp

file_name = "raw_data/IMU_trial2_AH_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial3_AH_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial4_AH_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 7, 17)
data = data + temp

file_name = "raw_data/IMU_trial5_AH_fall.xlsx"
temp = read_no_fall(file_name)
fall(temp, 9, 15)
data = data + temp

file_name = "raw_data/IMU_trial1_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial2_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

file_name = "raw_data/IMU_trial3_no_fall.xlsx"
temp = read_no_fall(file_name)
data = data + temp

## convert to df after reading all data
df = pd.DataFrame(data)
df.to_csv('data_df.csv')    

