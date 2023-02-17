# import all necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import os
from dateutil.parser import parse
import pandas as pd
from datetime import datetime
import logging
import schedule

# URL of the website to scrape
url = "https://www.gov.uk/government/statistics/oil-and-oil-products-section-3-energy-trends"



# create a directory named "downloads"
directory = "downloads"
if not os.path.exists(directory):
    os.makedirs(directory)

# Retrieve the link to the file and store it in "file_url"
response = requests.get(url)
soup = bs(response.content, "html.parser", from_encoding="UTF-8")
file_url = soup.select_one('a[aria-describedby="attachment-7159263-accessibility-help"]')['href']
file_path = directory + '/' + file_url.split('/')[-1]

# Set up the logger to keep track of the program
logger = logging.getLogger("petrioneos")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs_petrioneos.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Function to check if there is new data available
def check_for_new_data(previous_df):
    logger.info('Checking for new data...')
    print('Checking for new data...')
    download_file()
    current_df = pd.read_excel(file_path,
                               sheet_name='Quarter',
                               index_col=4,
                               header=4)
    if previous_df.equals(current_df):
        logger.info('Data is up-to-date.')
        print('Data is up-to-date.')
        return False
    else:
        logger.info('New data found.')
        print('New data found.')
        return True

# Function to download the file from the link
def download_file():
    response = requests.get(file_url)
    with open(file_path, "wb") as energy_file:
        energy_file.write(response.content)
    logger.info(f'Downloaded file: {file_path}')
    print(f'Downloaded file: {file_path}')

# Function to check if a date string is valid
def is_valid_date(date_string):
    try:
        parse(date_string)
        return True
    except ValueError:
        logger.error(f"Error trying to parse {date_string} to datetime")
        return False    

# Main function to run the program
def main():

    # Set the task to run every 24 hours
    schedule.every(24).hours.do(check_for_new_data)
    download_file()

    # Read the excel file into a pandas dataframe
    df = pd.read_excel(file_path, sheet_name="Quarter", index_col=4, header=4)
    
    # Perform basic data profiling and save to a CSV file
    num_rows, num_cols = df.shape
    min_per_col = df.min()
    max_per_col = df.max()
    mean_per_col = df.mean()
    median_per_col = df.median()
    total_missing_values = df.isnull().sum().sum()
    dict_profilling = {"num_rows": num_rows, "num_cols": num_cols, "min_per_col": min_per_col, \
                       "max_per_col": max_per_col, "mean_per_col": mean_per_col, "median_per_col": median_per_col, \
                       "total_missing_values": total_missing_values}
    df.fillna("")
    df_profiling = pd.DataFrame(dict_profilling)
    df_profiling.to_csv(file_path.split("/")[-1][:-5] + "_data_profiling.csv")
    
    # Check if the dataframe contains date type columns and convert them to datetime objects
    if (df.select_dtypes(include=['datetime']).columns.size > 0):
        logger.info('DataFrame contains date type column')
        print('DataFrame contains date type column')
        for i, j in df.iterrows():
            for data in j:
                str_data = str(data)
                if is_valid_date(str_data):
                    if len(str_data) == 10:
                        df.at[i][j] = datetime.strptime(str_data, "%Y-%m-%d")
                    elif len(str_data) == 17:
                        df.at[i][j] = datetime.strptime(str_data, '%Y-%m-%d %H-%M-%S')
    else:
        logger.info('DataFrame does not contain date type column')
        print('DataFrame does not contain date type column')
    
    # Create a dictionary to store consistency checks
    dict_data_consistency = {}
    dict_data_consistency["new_data"] = check_for_new_data(df)
    dict_data_consistency["correct_time_format"] = "sorted"
    dict_data_consistency["num_missing_values"] = total_missing_values
    dict_data_consistency["new_columns"] = check_for_new_data(df)
    dict_data_consistency["missing_columns"] = check_for_new_data(df)

    # Create a dataframe to store consistency check results
    df_data_consistency = pd.DataFrame(dict_data_consistency.items())
    df_data_consistency.to_csv(file_path.split("/")[-1][:-5] + "_data_consistency.csv")
    
if __name__ == '__main__':
    main()
