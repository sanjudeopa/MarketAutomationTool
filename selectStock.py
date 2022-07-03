import sys, os
import pandas
import argparse

class selectStocks():
    ''' Stock Selection Strategies'''

    STOCK_PRICE_LIMIT = 1000

    @staticmethod
    def is_float(num):
        ''' To check if value can be converted to fload '''
        try:
            float(num)
        except ValueError:
            return False
        return True

    def preopen_market_based_select(self, per_change, file_path):
        ''' first stratergy 
            1. Dowload the csv file from NSE. 
            2. based on the pre open market data, and 
               GAP UP/DOWN movement in NIFTY50
            3. Select Stocks
                if price < 1000 and the move similarly. 
            TODO :  automate the download and finding the % change in NIFTY50.
            TODO : latest.csv filename to actual file name format.
            
        '''
        filename = os.path.join(file_path, 'latest.csv')
        assert os.path.exists(filename), f"File {s} is missing!!".format(filename)
        df = pandas.read_csv(filename, header=None)

        stock_l = []
        lower_limit = per_change - 0.10
        upper_limit = per_change + 0.10
        column_l = list(df.columns)[:6]
        data  = df.iloc[1:, column_l]
        for idx, row in data.iterrows():
            if (self.is_float(row[column_l[-2]]) and \
                (float(row[column_l[-2]]) > lower_limit)  and \
                (float(row[column_l[-2]]) < upper_limit) and \
                (float(row[column_l[1]].replace(',', '')) < self.STOCK_PRICE_LIMIT)):
                stock_l.append(list(row))

        return stock_l

    def get_stocks(self, change, file_path):
        '''
        Interface routine. 
        TODO : make it generic as you go.
        '''
        return self.preopen_market_based_select(change, file_path)


def parseInput():
    '''
        Parser
    '''
    home_path = "/home/sanju/Music/stockMarket"
    parser = argparse.ArgumentParser(description='Stock Selection Tool')
    parser.add_argument('--path',type=str, nargs="+", default=home_path, help='path to the preopen market data')
    parser.add_argument('--change', type=float, nargs="+", default=0.30, help='% change in NIFTY50 before market')
    args = parser.parse_args()
    return args.change[0], args.path

def run():
    change_nifty50, csv_path = parseInput()
    todays_stock_l = selectStocks().get_stocks(float(change_nifty50), csv_path)
    if not len(todays_stock_l):
        print("No Stock To select today!! Try something else.") 
    else:
        for stock in todays_stock_l:
            print("".join(f"{s:10} "for s in stock))

if __name__ == "__main__":
    sys.exit(run())
