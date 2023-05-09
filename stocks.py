import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Use yfinance to extract Tesla stock data
tickerSymbol = 'TSLA'
tickerData = yf.Ticker(tickerSymbol)
tesla_data = tickerData.history(period='max')
tesla_data.reset_index(inplace=True)

# Use web scraping to extract Tesla revenue data
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
response = requests.get(url)
html_data = response.text
soup = BeautifulSoup(html_data, 'html.parser')
table = soup.find_all("tbody")[1]
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in table.find_all('tr'):
    col = row.find_all('td')
    date = col[0].text.strip()
    revenue = col[1].text.strip()
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Use yfinance to extract GameStop stock data
tickerSymbol = 'GME'
tickerData = yf.Ticker(tickerSymbol)
gme_data = tickerData.history(period='max')
gme_data.reset_index(inplace=True)

# Use web scraping to extract GameStop revenue data
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
response = requests.get(url)
html_data = response.text
soup = BeautifulSoup(html_data, 'html.parser')
table = soup.find_all("tbody")[1]
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in table.find_all('tr'):
    col = row.find_all('td')
    date = col[0].text.strip()
    revenue = col[1].text.strip()
    revenue = revenue.replace(',', '').replace('$', '')
    gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Plot the Tesla stock graph
def make_graph(data, revenue, stock_name):
    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(data['Date'], data['Close'], label='Stock Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(stock_name + ' Stock Price')
    ax2 = ax.twinx()
    ax2.plot(revenue['Date'], revenue['Revenue'], color='r', label='Revenue')
    ax2.set_ylabel('Revenue')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()

make_graph(tesla_data, tesla_revenue, 'Tesla')
