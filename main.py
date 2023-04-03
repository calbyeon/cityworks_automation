import pandas as pd
from fuzzywuzzy import fuzz
from dateutil.parser import parse
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Load the two CSV files into dataframes
def load_files():
    print("Select the first CSV file you would like to compare.")
    file1 = filedialog.askopenfilename(title="Select CSV file 1", filetypes=[("CSV Files", "*.csv")])
    print("Select the second CSV file you would like to compare.")
    file2 = filedialog.askopenfilename(title="Select CSV file 2", filetypes=[("CSV Files", "*.csv")])
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Get columns to compare
    col1 = input("Enter the column in file 1 you would like to compare: ")
    col2 = input("Enter the column in file 2 you would like to compare: ")

    
    # Request user input for the columns to compare
    while True:
        try:
            parse(df1[col1].iloc[0])
            parse(df2[col2].iloc[0])
            break
        except ValueError:
            print("The columns you entered do not contain dates. Please enter columns that contain dates.")
            col1 = input("Enter the column in file 1 you would like to compare: ")
            col2 = input("Enter the column in file 2 you would like to compare: ")
        except KeyError:
            print("The column you entered does not exist in one or both files. Please enter columns that exist in both files.")
            col1 = input("Enter the column in file 1 you would like to compare: ")
            col2 = input("Enter the column in file 2 you would like to compare: ")
    
    return df1, df2, col1, col2

df1, df2, col1, col2 = load_files()

# Find the best match between the two rows
for index1, row1 in df1.iterrows():
    best_match_score = 0
    best_match_row = None

    # Find the best match with any row in df2
    for index2, row2 in df2.iterrows():
        score = fuzz.ratio(str(row1[col1]), str(row2[col2]))
        if score > best_match_score:
            best_match_score = score
            best_match_row = row2

    # Print out the contents of the best match
    if best_match_score > 0:
        print('Best match for row {} in file1.csv:'.format(index1))
        print('Project Name:', row1['Project Name'])
        print(col1 + ':', row1[col1])
        print('Best match in file2.csv:')
        print('Project Description:', best_match_row['Project Description'])
        print(col2 + ':', best_match_row[col2])
        if parse(row1[col1]) == parse(best_match_row[col2]):
            print('Values of {} and {} match.\n'.format(col1, col2))
        else:
            print('Values of {} and {} do not match.\n'.format(col1, col2))
            new_date_str = input('Enter the correct date for {} in the format "DD-Mon-YYYY": '.format(col1))

            # Convert the input to a datetime object
            new_date = parse(new_date_str)

            # Update the dates in both sheets
            df1.at[index1, col1] = new_date.strftime('%d-%b-%Y')
            df2.at[best_match_row.name, col2] = new_date.strftime('%d-%b-%Y')
            print('{} updated to: {}'.format(col1, new_date_str))
            
            if parse(row1[col1]) == parse(best_match_row[col2]):
                print('Values updated. Values of {} and {} now match.\n'.format(col1, col2))
            else:
                print('Values still do not match')
                break
    else:
        print('No match found for row {} in file1.csv.'.format(index1))
        
df1.to_csv('ExampleC3_updated.csv', index=False)
df2.to_csv('ExampleC3_AGOL_updated.csv', index=False)