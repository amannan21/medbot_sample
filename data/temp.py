import pandas as pd
import numpy as np

disease_symptom_dict = {}
input_file_name = 'data/dataset.csv'

def readData(inpit_file_name):

    data_df = pd.read_csv(input_file_name)

    return data_df

def createDiseaseSymptomDict(data_df):

    disease_symptom_dict = {}

    for iter, row in data_df.iterrows():

        symptom_list = []

        for col_name in data_df.columns:

            if(row[col_name] == 1):
                symptom_list.append(col_name)

        disease_symptom_dict[row['Name']] = symptom_list    

    return disease_symptom_dict

def findTopMatches(n, data, disease_symptom_dict):

    return []

if(__name__ == '__main__'):

    data_df = readData(inpit_file_name = input_file_name)
    disease_symptom_dict = createDiseaseSymptomDict(data_df = data_df)

    print(disease_symptom_dict)