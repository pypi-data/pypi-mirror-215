import sys 
import os
sys.path.append(os.path.abspath(os.getcwd()))
import ipyfilechooser
from termcolor import colored
import requests
from requests import get
from IPython.display import HTML, display, Markdown, clear_output
from ipydatagrid import DataGrid, TextRenderer, BarRenderer, Expr
import pandas
from pathlib import Path


df = pandas.DataFrame()  # Add this line to initialize the df variable

def upload_file(chooser):
    global df
    if chooser.selected:
        with open(chooser.selected, 'rb') as f:
            file_name = chooser.selected_filename
            file_ext = file_name.split('.')[-1]
            clear_output(wait=True)
            if file_ext == 'csv':
                df = pandas.read_csv(f)
            elif file_ext == 'xlsx':
                df = pandas.read_excel(f)
            elif file_ext == 'parquet':
                df = pandas.read_parquet(f)
            else:
                display(Markdown('__Invalid file format!__'))
                return df
            display(Markdown('File `{}` having __{} rows__ and __{} columns__ loaded.'.format(file_name, df.shape[0], df.shape[1])))
            display(DataGrid(df.head(50), auto_fit_columns=True, layout={"height": "250px"}))
    else:
        display(Markdown('__No file selected!__'))
    
    return df


def load_data_from_url():
    store_df = pandas.DataFrame()

    display(Markdown('### Loading data from URL'))
    display(Markdown('Enter your URL and press `Enter`.'))

    cell_name = 'load_from_url'

    # once the box appears after executing this cell, enter your URL and press 'Enter'
    enter_url = input('URL: ')

    if enter_url == '':
        print(colored('\nNO URL entered!', "red", attrs=['bold']),
              colored('Please run this cell again to enter the URL.', "red"))
    else:
        try:
            display(Markdown('<div><div class="loader"></div><h2> &nbsp; DOWNLOADING data from URL </h2></div>'))
            # send request to obtain the data from the URL
            response = requests.get(enter_url)
            clear_output()

            # CSV file name obtained from online
            file_name = enter_url.split('/')[-1]

            # file that will be created in your local when the data is pulled from the URL
            file_path = Path(os.path.join(os.getcwd(), 'src', 'datasets', file_name))

            # create the directories if they don't exist
            os.makedirs(file_path.parent, exist_ok=True)
            
            # parse the HTML content and extract tables
            tables = pandas.read_html(response.content)

            # assume the first table is the desired dataset
            if tables:
                store_df = tables[0]
                clear_output()
                display(Markdown('File `{}` having __{} rows__ and __{} columns__ loaded.'.format(file_name, store_df.shape[0], store_df.shape[1])))
                display(store_df.head(100).round(4))
            else:
                print(colored('\nNo tables found in the HTML file!', "red", attrs=['bold']))

        except Exception as err:
            clear_output()
            # display the error
            print(colored('\nERROR:', "red", attrs=['bold']), colored(err, 'grey'))

    return store_df

