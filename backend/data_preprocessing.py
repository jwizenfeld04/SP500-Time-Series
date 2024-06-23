import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = 'data'
PREPROCESSED_DIR = 'preprocessed_data'

# List all CSV files in the data directory
stock_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]


def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    return df


def preprocess_data(df):
    # Check for and remove duplicates
    df = df[~df.index.duplicated(keep='first')]

    df = df.astype({
        'Open': 'float64',
        'High': 'float64',
        'Low': 'float64',
        'Close': 'float64',
        'Adj Close': 'float64',
        'Volume': 'int64'
    })

    # Feature Engineering
    df['Daily Return'] = df['Adj Close'].pct_change()
    df['Volume Change'] = df['Volume'].pct_change()

    df = df.dropna()

    return df


def main():
    if not os.path.exists(PREPROCESSED_DIR):
        os.makedirs(PREPROCESSED_DIR)

    for file in stock_files:
        symbol = file.split('.')[0]
        file_path = os.path.join(DATA_DIR, file)
        df = load_data(file_path)
        df_preprocessed = preprocess_data(df)

        # Save the preprocessed data
        preprocessed_file_path = os.path.join(
            PREPROCESSED_DIR, f'{symbol}.csv')
        df_preprocessed.to_csv(preprocessed_file_path)
        print(
            f"Preprocessed data for {symbol} saved to {preprocessed_file_path}")


if __name__ == '__main__':
    main()
