import pandas as pd

def extract_columns(file1, cols1, file2, cols2, output_file):
    """
    Extract specific columns from two text files and save them to a new text file.

    Parameters:
    file1 (str): Path to the first input text file.
    cols1 (list): List of column names or indices to extract from the first file.
    file2 (str): Path to the second input text file.
    cols2 (list): List of column names or indices to extract from the second file.
    output_file (str): Path to save the output text file.
    """
    data1 = pd.read_csv(file1, sep=",", header=0)
    extracted1 = data1[cols1]

    data2 = pd.read_csv(file2, sep=",", header=0)
    extracted2 = data2[cols2]

    combined = pd.concat([extracted1, extracted2], axis=1)

    combined.to_csv(output_file, sep=",", index=False)

file1 = "data/timevsvelocity.txt"
cols1 = ["time", "longitude", "latitude"]
file2 = "data/timevsconnectivitymodified.txt"
cols2 = ["connectivity"]
output_file = "data/timevsconnectivityfinal.txt"

extract_columns(file1, cols1, file2, cols2, output_file)
