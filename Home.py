#All the Imports

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,

    # Layouts
    QVBoxLayout,
    QHBoxLayout,

    # Inputs
    QLineEdit,
    QPushButton,

    # Display
    QLabel,

    # Other
    QMessageBox,
)

from PyQt5.QtCore import Qt

#Importing pages
from Stocks import * 
from Portfolio import *


class Home(QMainWindow):

    def __init__(self):
        super().__init__()

        self.settings()

        # Pages
        self.pages = QStackedWidget()

        self.home_page = QWidget()
        self.portfolio_page = Portfolio()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.portfolio_page)

        self.setCentralWidget(self.pages)

        self.initUI()

    def initUI(self):

        # Title
        self.title = QLabel("PyFinance")
        self.title.setObjectName("title")

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter stock ticker (Ex: AAPL)...")

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)

        # Stock information
        self.stock_box = QLabel("Search for a stock")

        # Portfolio button
        self.portfolio_button = QPushButton("See your Portfolio")
        self.portfolio_button.clicked.connect(self.show_portfolio)

        self.portfolio_page.home_button.clicked.connect(self.go_home)

        #add to portfolio
        self.add_button = QPushButton("Add to your Portfolio")
        self.add_button.clicked.connect(self.add_to_portfolio)

        # Graph
        # Temporary graph using AAPL
        data, stock_info = search_stock("AAPL")

        self.stock_box.setText(stock_info)

        self.graph = Graph(data)

        # Layout
        mainLayout = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(self.title)
        left.addWidget(self.search_bar)
        left.addWidget(self.search_button)
        left.addWidget(self.stock_box)
        left.addWidget(self.add_button)
        left.addWidget(self.portfolio_button)

        right = QVBoxLayout()
        right.addWidget(self.graph)

        mainLayout.addLayout(left)
        mainLayout.addLayout(right)

        self.home_page.setLayout(mainLayout)


    def settings(self):
        self.setWindowTitle("PyFinance")
        self.setGeometry(450, 150, 900, 800)

    def search(self):

        ticker = self.search_bar.text().upper()

        if not ticker:
            return ("Retry")

        data, stock_info = search_stock(ticker)

        # Update stock information
        self.stock_box.setText(stock_info)

        if data is None: 
            QMessageBox.warning(
                self,
                "Invalid Ticker",
                "Please enter a valid stock ticker symbol.")
            return
        
        # Update graph
        self.graph.plot_stock(data)


    def show_portfolio(self):
        self.pages.setCurrentWidget(self.portfolio_page)

    def go_home(self):
            self.pages.setCurrentWidget(self.home_page)

    def add_to_portfolio(self):
        ticker = self.search_bar.text().upper()

        if not ticker:
            QMessageBox.warning(
                self,
                "No Ticker",
                "Please search for a stock first."
            )
            return

        if ticker in portfolio_list:
            QMessageBox.warning(
                self,
                "Already Added",
                f"{ticker} is already in your portfolio."
            )
            return

        portfolio_list.append(ticker)

        self.portfolio_page.update_portfolio()

        QMessageBox.information(
            self,
            "Added",
            f"{ticker} was added to your portfolio!"
        )




if __name__ == "__main__":
    app = QApplication([])

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())


    main = Home()
    main.show()
    app.exec_()
