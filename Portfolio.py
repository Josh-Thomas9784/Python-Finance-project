from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget
from Stocks import search_stock

portfolio_list = []

class Portfolio(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.update_portfolio()

    def initUI(self):
        # Title
        self.title = QLabel("Your Portfolio")

        # List of stocks
        self.stock_list = QListWidget()

        #Total Stock value
        self.total_label = QLabel("Portfolio Value: $0.00")

        # Home button
        self.home_button = QPushButton("Go back to Home page")

        # Layout
        mainLayout = QVBoxLayout()
        
        mainLayout.addWidget(self.title)
        mainLayout.addWidget(self.stock_list)
        mainLayout.addWidget(self.total_label)
        mainLayout.addWidget(self.home_button)

        self.setLayout(mainLayout)

    def update_portfolio(self):

        self.stock_list.clear()

        total = 0

        for ticker in portfolio_list:

            data, _ = search_stock(ticker)

            if data is not None:

                price = data["c"]
                total += price

                self.stock_list.addItem(
                    f"{ticker} — ${price:.2f}"
                )

        self.total_label.setText(
            f"Portfolio Value: ${total:.2f}"
        )