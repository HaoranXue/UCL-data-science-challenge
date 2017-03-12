import pandas as pd
import collections
import numpy as np
import os,sys,time


class ReadData():

    def __init__(self):
        self.name_list = ['Commodity', 'Currency', 'Economic_Indicator', 'Equity', 'Index','Precious_Metal']
        self.location = '../data'
        self.data_pack = collections.defaultdict()
        self.read_data()
        self.ticker_name = []
        self.read_ticker()

    def read_ticker(self):
        for i in self.name_list:
            print(i,'master')
            dummy = pd.read_csv(self.location + '/' + str(i) + '_Master' +  '.csv')
            self.ticker_name.append(list(dummy.Ticker))

    def read_data(self):
        for i in self.name_list:
            print(i)
            self.data_pack[i] = pd.read_csv(self.location + '/' + str(i) + '_mod' +  '.csv')

    def get_data(self):
        print("")
        return self.data_pack

    def get_name_list(self):
        return self.name_list

    def get_ticker_name(self):
        return self.ticker_name


def first():
    data = ReadData()
    name_list = data.get_name_list()
    data_pack = data.get_data()
    print('first')
    for i in range(len(name_list)):
        print('\r' + str(i) + '/' + str(len(name_list)),end='')
        data_pack[name_list[i]]['Date'] = pd.to_datetime(data_pack[name_list[i]].Date)
        data_pack[name_list[i]]['Date'] = data_pack[name_list[i]]['Date'].dt.strftime('%Y%m%d')

        try:
            new_data_frame = data_pack[name_list[i]][['Date', 'Ticker', 'Close']]
        except:
            new_data_frame = data_pack[name_list[i]][['Date', 'Ticker', 'Value']]
            new_data_frame.columns = ['Date', 'Ticker', 'Close']

        new_data_frame.to_csv('../data/' + name_list[i] + '_mod'+'.csv',index=False)


def second():
    data = ReadData()
    name_list = data.get_name_list()
    data_pack = data.get_data()
    ticker_name = data.get_ticker_name()

    print('second')
    count = 0
    for i in range(len(name_list)):
        for j in range(len(ticker_name[i])):
            print('\r' + str(i) + '/' + str(len(name_list)) + '\t' + str(j) + '/' + str(len(ticker_name[i])), end='')
            try:
                if count == 0:
                    df_a = data_pack[name_list[i]].loc[data_pack[name_list[i]]['Ticker'] == ticker_name[i][j]]
                    df_a = df_a[['Date','Close']]
                    df_a.columns = ['Date',ticker_name[i][j]]
                    merged = df_a
                else:
                    df_a = data_pack[name_list[i]].loc[data_pack[name_list[i]]['Ticker'] == ticker_name[i][j]]
                    df_a = df_a[['Date','Close']]
                    df_a.columns = ['Date',ticker_name[i][j]]
                    merged = pd.merge(merged,df_a, on='Date', how='outer')
            except:
                print(name_list[i],name_list[i][j])
            count += 1

    print(merged)
    merged.to_csv('../data/' +'merged_8.csv', index=False)


def third():
    print('third')
    location = '../data'

    df = pd.read_csv(location + '/' + 'merged_8.csv')

    print(df)
    df = df.sort_values(by='Date', ascending=[True])
    print(df)
    df.to_csv('../data/' + 'merged_9.csv', index=False)


def main():
    first()
    second()
    third()


if __name__ == '__main__':
    main()





















