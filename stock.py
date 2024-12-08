import requests

# Your Alpha Vantage API Key (replace with your own key)
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

# Portfolio dictionary to manage stock holdings
portfolio = {}

def fetch_stock_price(symbol):
    """
    Fetch the latest stock price for the given symbol using the Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the latest price if data is valid
    if "Time Series (1min)" in data:
        latest_time = next(iter(data["Time Series (1min)"]))
        price = float(data["Time Series (1min)"][latest_time]["1. open"])
        return price
    else:
        print(f"Error: Unable to fetch stock data for {symbol}.")
        return None

def add_stock(symbol, quantity):
    """
    Add a stock to the portfolio.
    """
    price = fetch_stock_price(symbol)
    if price is not None:
        portfolio[symbol] = {
            "quantity": quantity,
            "price": price
        }
        print(f"Added {symbol} to your portfolio with {quantity} shares at ${price:.2f}.")
    else:
        print(f"Failed to add {symbol}. Check the stock symbol and try again.")

def remove_stock(symbol):
    """
    Remove a stock from the portfolio.
    """
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from your portfolio.")
    else:
        print(f"{symbol} is not in your portfolio.")

def view_portfolio():
    """
    View the current portfolio with stock details and total value.
    """
    if not portfolio:
        print("Your portfolio is empty.")
        return

    total_value = 0
    print("\nYour Portfolio:")
    print(f"{'Symbol':<10} {'Quantity':<10} {'Price':<10} {'Value':<10}")
    print("-" * 40)
    for symbol, data in portfolio.items():
        value = data["quantity"] * data["price"]
        total_value += value
        print(f"{symbol:<10} {data['quantity']:<10} ${data['price']:<10.2f} ${value:<10.2f}")

    print(f"\nTotal Portfolio Value: ${total_value:.2f}\n")

def main():
    """
    Main program loop for the stock portfolio tracker.
    """
    print("Welcome to the Stock Portfolio Tracker!")
    while True:
        print("\nOptions:")
        print("1. Add a stock")
        print("2. Remove a stock")
        print("3. View portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").upper()
            quantity = int(input("Enter the quantity of shares: "))
            add_stock(symbol, quantity)
        elif choice == "2":
            symbol = input("Enter the stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            view_portfolio()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
