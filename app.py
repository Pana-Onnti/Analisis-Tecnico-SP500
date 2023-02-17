import os , csv
from flask import Flask , request
from flask import render_template
from patterns import patterns
import yfinance as yf 
import pandas as pd
import talib 


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    pattern=request.args.get('pattern',None)
    stocks={}


    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]]={'company':row[1]}
            
    print(stocks)
    if pattern :
       datafiles = os.listdir('datasets/daily')
       for filename in datafiles:
        df = pd.read_csv('datasets/daily/{}'.format(filename))
        patter_function= getattr(talib,pattern)

        symbol = filename.split('.')[0]
        
        try:
            result = patter_function(df['Open'],df['High'],df['Low'],df['Close'])
            last = result.tail(1).values[0]
            if last > 0:
                stocks[symbol][pattern]='Bullish'
            elif last <0 :
                stocks[symbol][pattern]='Bearish'
            else:
                stocks[symbol][pattern]=None
        except:
            pass


    return render_template('index.html',patterns=patterns,stocks=stocks, current_pattern=pattern)



@app.route("/snapshot")
def snapshot(): 
    with open('datasets/companies.csv') as f:
        companies= f.read().splitlines()
        for company in companies:
           symbol= company.split(',')[0]
           print(symbol)
           df = yf.download(symbol,start="2020-01-01", end="2022-09-09")
           df.to_csv('datasets/daily/{}.csv'.format(symbol))







if __name__ == "__main__":
    app.run(debug=True)
