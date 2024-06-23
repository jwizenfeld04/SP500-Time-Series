import os
import pickle
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

DATA_DIR = 'data'


def save_sp500_tickers():
    resp = requests.get(
        'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def fetch_and_save_stock_data(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=10*365)
                  ).strftime('%Y-%m-%d')
    df = yf.download(symbol, start=start_date, end=end_date)
    if not df.empty:
        file_path = os.path.join(DATA_DIR, f'{symbol}.csv')
        df.to_csv(file_path)
        print(f"Saved data for {symbol} to {file_path}")
    else:
        print(f"No data found for {symbol}")


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    tickers = save_sp500_tickers()
    for symbol in tickers:
        print(f"Fetching data for {symbol}...")
        fetch_and_save_stock_data(symbol)


if __name__ == '__main__':
    main()
