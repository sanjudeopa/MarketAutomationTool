import os
import pandas as pd


# Function to process a single sheet
def process_sheet(excel_file, sheet_name):
    ''' '''

    df = excel_file.parse(sheet_name)
    if all(col in df.columns for col in ['Date', 'Open', 'High', 'Low', 'Close']):
        # TODO create a map from configSheet.
        df['stock_name'] = sheet_name
        return df[['stock_name', 'Date', 'Open', 'High', 'Low', 'Close']].tail(3)
    
    return None


# Function to compile all sheets into one DataFrame
def compile_stock_data(file_path):
    ''' 
    Input file has 200 sheets named as <NSE:STOCKCODE>
    '''

    data_frames = []
    excel_file = pd.ExcelFile(file_path, engine='openpyxl')
    for sheet in excel_file.sheet_names:
        if not sheet.startswith('NSE'):
            continue
        stock_df = process_sheet(excel_file, sheet)
        if stock_df is not None:
            data_frames.append(stock_df)

    return pd.concat(data_frames, ignore_index=True)


# Usage
def main():
    ''' main calling function '''

    input_name = "../data/Nifty200Weekly.xlsx"
    nifty_data = compile_stock_data(input_name)
    print(nifty_data)


if __name__ == '__main__':
    main()

