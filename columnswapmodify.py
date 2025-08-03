import pandas as pd
import re

def is_percentage(value):
    """
    Check if the value is a percentage like '67%'.
    """
    return bool(re.fullmatch(r"\d+%", str(value).strip()))

def is_signal_strength(value):
    """
    Check if the value is a signal strength like '21 (-71 dBm)'.
    """
    return bool(re.fullmatch(r"\d+\s\(-\d+\sdBm\)", str(value).strip()))

def fix_swapped_columns(input_file, output_file, percentage_col, signal_col, sep=","):
    """
    Fix swapped data between percentage and signal strength columns.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to save the corrected file.
        percentage_col (int): Index of the percentage column (0-based).
        signal_col (int): Index of the signal strength column (0-based).
        sep (str): Separator in the file (default is comma).
    """

    print("Reading input file...")
    df = pd.read_csv(input_file, sep=sep, header=None, engine='python')

    for index, row in df.iterrows():
        percentage_value = row[percentage_col]
        signal_value = row[signal_col]

        if is_signal_strength(percentage_value) and is_percentage(signal_value):
            # Swap the values
            df.at[index, percentage_col], df.at[index, signal_col] = signal_value, percentage_value

    print(f"Row {index}: Percentage Column = '{percentage_value}', Signal Column = '{signal_value}'")

    print("Saving corrected file...")
    df.to_csv(output_file, sep=sep, index=False, header=False)
    print(f"File saved to {output_file}")

input_file = "data/timevsconnectivity.txt"    # Path to the input file
output_file = "data/document.txt"   # Path to save the corrected file
percentage_col = 10                 # Index of the percentage column (adjust as needed)
signal_col = 9                      # Index of the signal strength column
separator = ","                  # Separator in the file (comma-separated)

fix_swapped_columns(input_file, output_file, percentage_col, signal_col, separator)
