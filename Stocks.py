import requests
from PyQt5.QtWidgets import (QLineEdit,QPushButton)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_KEY = "d9uk089r01qs9cmd5bagd9uk089r01qs9cmd5bb0"

def searchbar(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter stock ticker...")

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_stock)

def search_stock(ticker):
    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": ticker,
        "token": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Check if ticker is invalid
    if data["c"] == 0 and data["h"] == 0 and data["l"] == 0:
        return None, None

    price = data["c"]
    change = data["d"]
    percent = data["dp"]

    stock_info = (
        f"Price: ${price:.2f} | "
        f"Change: ${change:.2f} | "
        f"Percent: {percent:.2f}%"
    )

    return data, stock_info

#creating the graph
class Graph(FigureCanvas):

    def __init__(self, data):

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        super().__init__(self.figure)

        self.plot_stock(data)


    def plot_stock(self, data):

        labels = [
            "Previous Close",
            "Open",
            "Low",
            "High",
            "Current"
        ]

        prices = [
            data["pc"],
            data["o"],
            data["l"],
            data["h"],
            data["c"]
        ]

        self.axes.clear()

        self.axes.plot(labels, prices, marker="o")

        self.axes.set_title("Stock")
        self.axes.set_ylabel("Price ($)")

        self.figure.tight_layout()

        self.draw()
