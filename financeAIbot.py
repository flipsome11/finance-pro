from neuralintents import BasicAssistant
import matplotlib.pyplot as plt 
import pandas as pd 
import pandas_datareader as web 
import mplfinance as mpf 
import yfinance as yf
import pickle
import sys
import datetime as dt

# This is a common pattern for saving and loading data structures in Python.
# 'portfolio.pkl' in binary read mode ('rb'). The with statement is used to ensure that the file is properly closed after reading.
# pickle.load(f): This function reads the serialized data from the file f and reconstructs the original Python object. In this case, it's loading the content of the file into the portfolio variable.
# The combination of these two code snippets allows you to persistently store the state of a portfolio object in a file and later retrieve it. This is useful for saving and loading data between program executions.
with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

# with open('portfolio.pkl', 'wb') as f:: Similar to the reading part, this line opens the file named 'portfolio.pkl' in binary write mode ('wb'). The with statement ensures that the file is properly closed after writing.
# pickle.dump(portfolio, f): This function serializes the portfolio object and writes it to the file f. It essentially saves the current state of the portfolio to the file, making it possible to load it later using pickle.load.
def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

# The function starts by taking user input for the stock ticker and the number of shares to add.
# ticker = input("Which Stock do you want to add: "): This line prompts the user with a message and waits for input. The entered value is stored in the variable ticker.
# amount = input("How many shares do you want to add: "): Similarly, this line prompts the user for the number of shares and stores the input in the variable amount.
# if ticker in portfolio.keys():: This line checks if the entered stock ticker (ticker) already exists in the portfolio dictionary. The portfolio variable is assumed to be a dictionary containing stock tickers as keys and the corresponding number of shares as values.
# If the ticker exists in the portfolio, the number of shares is increased by the entered amount.
# portfolio[ticker] += int(amount): This line increments the existing number of shares for the specified ticker by converting the input amount to an integer.
# If the ticker doesn't exist, a new entry is created in the portfolio with the entered amount of shares.
# else: portfolio[ticker] = int(amount): This line adds a new entry to the portfolio dictionary with the entered ticker as the key and the entered amount as the value.
# save_portfolio(): After modifying the portfolio, the save_portfolio function is called to persistently save the updated portfolio to a file. 
# This ensures that the changes made by adding shares are stored and can be retrieved in subsequent program executions.
def add_portfolio():
    ticker = input("Which Stock do you want to add: ")
    amount = input("How many shares do you want to add: ")

    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()


# In Python, portfolio.keys() is a method call on a dictionary object (portfolio). It returns a view of all the keys in the dictionary.
#  The returned object is a view object that displays a list of all the keys in the dictionary.
# portfolio is assumed to be a dictionary where each key represents a stock ticker, and the corresponding value represents the number of shares owned for that stock.
# if ticker in portfolio.keys(): checks if the user-inputted stock ticker (ticker) is present in the keys of the portfolio dictionary.

def remove_portfolio():
    ticker = input("Which stock do you want to sell:")
    amount = input("How many shares do you want to sell: ")

    # If the stock symbol is found in the portfolio, it further checks if the specified amount of shares to sell (amount) is less than or equal to the number of shares currently owned for that stock.
    # If there are sufficient shares, it deducts the specified amount from the existing shares in the portfolio.
    # After updating the portfolio, the save_portfolio function is called to save the changes.
    # 
    if ticker in portfolio.keys():
        if amount <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            save_portfolio()
        else:
            print("You don't have enough shares!")
    else:
        print(f"You don't own any shares of {ticker}")

def show_portfolio():
    print("Your portfolio:")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")

# The function starts by initializing a variable sum to 0. This variable will be used to accumulate the total worth of the portfolio.
# The function then iterates over each stock ticker in the keys of the portfolio dictionary.
# Inside the loop, it uses web.DataReader from the pandas_datareader library to fetch historical stock data for the current ticker from Yahoo Finance.
# This assumes that web refers to the pandas_datareader module, and it is fetching historical stock data for the specified ticker.
# The code then extracts the last closing price of the stock from the fetched data. It assumes that the stock data is organized as a pandas DataFrame, and it retrieves the last closing price using .iloc[-1].
# .iloc is used to index and select specific rows and columns from a DataFrame.
# This line assumes that the closing prices are available in a column named 'Close' in the fetched data.
# The closing price for the current stock (price) is added to the sum variable. This step is repeated for each stock in the portfolio, effectively accumulating the total worth of the portfolio.
# After iterating through all stocks in the portfolio, the function prints the total worth of the portfolio in USD.
def portfolio_worth():
    sum = 0
    for ticker in portfolio.keys():
        data = web.DataReader(ticker, 'yahoo')
        price = data['Close'].iloc[-1]
        sum += price

    print(f"Your portfolio is worth {sum} USD")

# Two variables, sum_now and sum_then, are initialized to 0. These variables will be used to accumulate the total worth of the portfolio at the current date and the specified starting date, respectively.
# The code then attempts to fetch the historical stock data for each ticker in the portfolio and compare the closing prices between the current date and the specified starting date.
def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYYY-MM-DD): ")

    sum_now = 0
    sum_then = 0

    # For each stock in the portfolio, it fetches the current closing price (price_now) from the latest available data and the closing price on the specified starting date (price_then).
    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then

        # Using the accumulated values of sum_now and sum_then, it calculates both the relative gains (as a percentage) and absolute gains in USD.
        # Relative Gains are calculated as the percentage change between the portfolio worth on the current date and the specified starting date.
        # Absolute Gains are the difference in portfolio worth between the two dates.
        print(f"Relative Gains: {((sum_now - sum_then)/ sum_then) * 100}% ")
        print(f"Absolute Gains: {sum_now - sum_then} USD")

       

    except IndexError:
        print("There was no trading on this day! ")


def plot_chart():
    ticker = input("Choose a ticker symbol: ")
    starting_string = input("Choose a starting date (DD/MM/YYYY): ")

    # plt.style.use('dark_background') sets the plotting style to use a dark background. This is a customization for the appearance of the plot.
    
    plt.style.use('dark_background')

    # # start = dt.datetime.strptime(starting_string, "%d/%m/%Y") parses the user-provided starting date string into a datetime object (start). The %d/%m/%Y format string indicates the expected format of the date string.
    # end = dt.datetime.now() sets the end date to the current date and time.
    
    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    # data = yf.download(ticker, start, end) uses the yfinance library (yf) to download historical stock data for the specified ticker symbol (ticker) within the given date range.
    data = yf.download(ticker, start , end)
    
    # The code then defines colors for the candlestick chart using mplfinance (mpf). make_marketcolors is used to set colors for different market scenarios (up, down, wick, edge, volume).
    colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    mpf.plot(data, type='candle', style=mpf_style, volume=True)
    
    
# The bye() function is defined, and when called, it prints "Goodbye" and then exits the Python interpreter using sys.exit(0).
def bye():
    print("Goodbye")
    sys.exit(0)


# An instance of the BasicAssistant class is created with the following parameters:
# 'intents.json': The file path to a JSON file containing intents and their associated actions.
# method_mappings: A dictionary that maps intent names to corresponding functions.
# The method_mappings dictionary associates specific intents (like 'plot_chart', 'add_portfolio', etc.) with corresponding Python functions.
assistant = BasicAssistant('intents.json', method_mappings={
    'plot_chart' : plot_chart,
    'add_portfolio' : add_portfolio,
    'remove_portfolio' : remove_portfolio,
    'show_portfolio' : show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains' : portfolio_gains,   
    'bye' : bye
})

# assistant.load_model() is called, presumably to load any pre-trained model or configurations associated with the BasicAssistant instance
assistant.load_model()

# done is set to False. This variable is likely used to control a loop, allowing the assistant to handle user inputs repeatedly until the user decides to exit.
done = False

# This sets up a while loop that continues as long as the variable done is False. The loop will repeatedly prompt the user for input.
# Inside the loop, it uses input("Enter a message: ") to prompt the user to enter a message. The entered message is stored in the variable message.
# It checks if the entered message is equal to "STOP." If so, it sets done to True, which will exit the loop.
# If the user input is not "STOP," it calls assistant.process_input(message) to process the user's input using the defined intents and associated functions. The result is then printed to the console.
while not done:
    message = input("Enter a message: ")
    if message == "STOP":
        done = True
    else:
        print(assistant.process_input(message))

