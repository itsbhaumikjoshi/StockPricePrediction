from datetime import datetime

# Enter your API key here from Alpha Vantage:
YOUR_API_KEY = ''

# Enter a Demo Stock for the testing of kalman filter prediction
DEMO_STOCK = 'IBM'

# The time for opening and closing of stock market
# It should be in HH:MM:SS
OPEN_TIME = ''
CLOSE_TIME = ''

OPEN_TIME = datetime.strptime(OPEN_TIME, '%H:%M:%S')
CLOSE_TIME = datetime.strptime(CLOSE_TIME, '%H:%M:%S')

# Current Day
CURRENT_DAY = datetime.today().strftime('%A')

# Enter the symbol code for the stocks to look for
STOCKS = []