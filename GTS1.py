import pandas as pd
import numpy as np
#remember to delete all the assistant columns!!!
def main():

    df = pd.read_csv('/Users/Wang/Downloads/PythonTest/sampleInput.csv')
    
    SymbolPosition(df)

    SymbolValue(df)

    SymbolBought(df)

    SymbolSold(df)

    ExchangeBought(df)

    ExchangeSold(df)

    TotalBought(df)

    TotalBoughtNotional(df)

    TotalSold(df)

    TotalSoldNotional(df)

    TotalValue(df)

  

    
#summary after process all data
    print('Shares Bought:', df['TotalBought'].iloc[-1],'\n')
    print ('Shares Sold:', df['TotalSold'].iloc[-1],'\n')
    print ('Notional Bought: $', format(df['TotalBoughtNotional'].iloc[-1],',.2f'),'\n',sep = '')
    print ('Notional Sold: $', format(df['TotalSoldNotional'].iloc[-1],',.2f'),'\n',sep = '')
    print ('Per Exchange Volume:','\n', PerEV(df),'\n')
    print ('Average Fill Size:', format(df['FillSize'].mean(),',.2f'),'\n')
    print ('Median Fill Size:',format(df['FillSize'].median(),',.2f'),'\n')
    print ('10 Most Active:','\n', MostActive(df))

    df = df.drop(['SignFillSize','SignFillSizeBought','SignFillSizeSold','SymbolFillSize'], axis = 1 )

    
#Round 'FillPrice','SymbolValue','TotalBoughtNotional','TotalSoldNotional','TotalValue'
    df[['FillPrice','SymbolValue','TotalBoughtNotional','TotalSoldNotional','TotalValue']] = df[['FillPrice','SymbolValue','TotalBoughtNotional','TotalSoldNotional','TotalValue']].apply(lambda x: pd.Series.round(x, 2))
    
    
#Save the data to out.csv
    df.to_csv('/Users/Wang/Downloads/PythonTest/out.csv')
    
#del df['SignFillSize']
def SymbolPosition(df):
    df['SignFillSize'] = df[['Side','FillSize']].apply(lambda x: x['FillSize'] if x['Side']=='b' else -x['FillSize'],axis = 1)
    df['SymbolPosition'] = df.groupby('Symbol')['SignFillSize'].cumsum()
    
def SymbolValue(df):
    df['SymbolValue'] = df[['SymbolPosition','FillPrice']].apply(lambda x: x['SymbolPosition']*x['FillPrice'], axis = 1)
#del df['SignFillSizeBought'] 
def SymbolBought(df):
    df['SignFillSizeBought'] = df[['Side','FillSize']].apply(lambda x: x['FillSize'] if x['Side']=='b' else 0,axis = 1)
    df['SymbolBought'] = df.groupby('Symbol')['SignFillSizeBought'].cumsum()
#del df['SignFillSizeSold']   
def SymbolSold(df):
    df['SignFillSizeSold'] = df[['Side','FillSize']].apply(lambda x: 0 if x['Side']=='b' else x['FillSize'],axis = 1)
    df['SymbolSold'] = df.groupby('Symbol')['SignFillSizeSold'].cumsum()


def ExchangeBought(df):
    df['ExchangeBought'] = df.groupby('FillExchange')['SignFillSizeBought'].cumsum()
    
    
def ExchangeSold(df):
    df['ExchangeSold'] = df.groupby('FillExchange')['SignFillSizeSold'].cumsum()

def TotalBought(df):
    df['TotalBought'] = df['SignFillSizeBought'].cumsum()

def TotalBoughtNotional(df):
    BoughtPrice = df['SignFillSizeBought']*df['FillPrice']
    df['TotalBoughtNotional'] = BoughtPrice.cumsum()

def TotalSold(df):
    df['TotalSold'] = df['SignFillSizeSold'].cumsum()

def TotalSoldNotional(df):
    SoldPrice = df['SignFillSizeSold']*df['FillPrice']
    df['TotalSoldNotional'] = SoldPrice.cumsum()
#From the sample out,it's more like TotalValue = SymbolValue,But the defination is NOT.
#So I imply the one follow by the Defination.
def TotalValue(df):
    df['TotalValue'] = df['SymbolValue'].cumsum()


def PerEV(df):
    return df[['ExchangeBought','ExchangeSold','FillExchange']].groupby('FillExchange').last().reset_index()
#del df['SymbolFillSize'] 
def MostActive(df):
    df['SymbolFillSize'] = df.groupby('Symbol')['FillSize'].cumsum()
    EachSymbol = df[['SymbolFillSize','Symbol']].groupby('Symbol').last()
    return EachSymbol.sort_values(by = 'SymbolFillSize', ascending=False).head(10).reset_index()

    
main()
