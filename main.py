import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QLabel, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QPen
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QPieSeries, QBarSeries
from PyQt5.QtCore import Qt
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import datetime


path = os.getcwd() + '/venv/'

client_id = 0
name = ""
currency_name = ""
currency_rate = 0.
currency_id = 0
buy = 0.
sell = 0.
amount = 0.
new_operation_id = 0
date = datetime.datetime.now().strftime('%d-%m-%Y')
url = 'https://www.cbr-xml-daily.ru/daily_json.js'
full_page = requests.get(url)
soup = BeautifulSoup(full_page.content, 'html.parser')
site_json = json.loads(soup.text)['Valute']
# print(text)
tags = ['CharCode', 'Name', 'Nominal', 'Value']
values = []
for i in site_json:
    new = []
    for tag in tags:
        new.append(site_json[i][tag])
    values.append([new])



class TitleWindow(QWidget):
    def __init__(self):
        super(TitleWindow, self).__init__()
        loadUi(path+"title.ui", self)
        self.pushButton.clicked.connect(self.gotoLogin)


    def gotoLogin(self):
        login = LoginWindow()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)



class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi(path+'login.ui', self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.loginFunction)

    def loginFunction(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if len(login)==0 or len(password)==0:
            self.warning.setText('Пожалуйста заполните все поля')
        else:
            conn = sqlite3.connect(path+'Leskov.db')
            cur = conn.cursor()
            query = "SELECT client_id, password FROM Logins WHERE login =\'"+login+"\'"
            cur.execute(query)
            log = cur.fetchone()
            global client_id
            client_id = log[0]
            result_pass = log[1]
            if result_pass == password:
                print('Successfully logged in')
                self.warning.setText('')
                print(client_id)
                mainWindow = Cabinet()
                widget.addWidget(mainWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.warning.setText('Неверные логин и пароль')



class Cabinet(QWidget):
    def __init__(self):
        super(Cabinet, self).__init__()
        loadUi(path+"main.ui", self)
        self.loadName()
        self.pushButton.clicked.connect(self.gotoBalance)
        self.pushButton_2.clicked.connect(self.gotoHistory)
        self.pushButton_3.clicked.connect(self.gotoRates)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def loadName(self):
        conn = sqlite3.connect(path+'Leskov.db')
        cur = conn.cursor()
        global client_id
        query = 'SELECT name FROM Clients WHERE client_id = '+str(client_id)
        cur.execute(query)
        global name
        name = cur.fetchone()[0]
        self.label_2.setText(name)


    def gotoBalance(self):
        balance = BalanceWindow()
        widget.addWidget(balance)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoHistory(self):
        history = HistoryWindow()
        widget.addWidget(history)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoRates(self):
        rates = RatesWindow()
        widget.addWidget(rates)
        widget.setCurrentIndex(widget.currentIndex()+1)




class BalanceWindow(QWidget):
    def __init__(self):
        super(BalanceWindow, self).__init__()
        loadUi(path+"balance.ui", self)
        global name
        self.label_2.setText(name)
        self.loadBalance()
        self.pushButton.clicked.connect(self.gotoCabinet)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadBalance(self):
        conn = sqlite3.connect(path+'Leskov.db')
        cur = conn.cursor()
        global client_id
        print('Balance for client ' + str(client_id))
        sqlquery = "SELECT currency_name, balance FROM Currencies, Balances WHERE Balances.currency_id=Currencies.currency_id AND Balances.client_id = "+str(client_id)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 250)
        #self.tableWidget.setHorizontalHeaderLabels(['Наименование валюты', 'Баланс'])
        self.tableWidget.setRowCount(10)
        tablerow = 0
        for row in cur.execute(sqlquery):
            print(row)
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            tablerow+=1

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class HistoryWindow(QWidget):
    def __init__(self):
        super(HistoryWindow, self).__init__()
        loadUi(path+"history.ui", self)
        global name
        self.label_2.setText(name)
        self.loadHistory()
        self.pushButton.clicked.connect(self.gotoCabinet)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def loadHistory(self):
        conn = sqlite3.connect(path+'Leskov.db')
        cur = conn.cursor()
        global client_id
        print('History for client ' + str(client_id))
        sqlquery = "SELECT oper_id, currency_name, change FROM Currencies, Operations WHERE Operations.currency_id=Currencies.currency_id AND Operations.client_id = " + str(client_id) +" ORDER BY oper_id DESC"
        self.tableWidget.setHorizontalHeaderLabels(['Наименование валюты', 'Изменение баланса'])
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setRowCount(10)
        tablerow = 0
        for row in cur.execute(sqlquery):
            print(row)
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            if row[2]>0:
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem("+"+str(row[2])))
            else:
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[2])))
            tablerow += 1


    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class RatesWindow(QWidget):
    def __init__(self):
        super(RatesWindow, self).__init__()
        loadUi(path+"rates.ui", self)
        global name
        self.label_2.setText(name)
        self.loadRates()
        self.pushButton.clicked.connect(self.gotoCabinet)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadRates(self):
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 450)
        self.tableWidget.setRowCount(34)
        tablerow = 0
        global values
        for row in values:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(values[tablerow][0][0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(values[tablerow][0][1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(values[tablerow][0][2])))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(values[tablerow][0][3])))
            tablerow+=1

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class OperationsWindow(QWidget):
    def __init__(self):
        super(OperationsWindow, self).__init__()
        loadUi(path+"operations.ui", self)
        self.pushButton.clicked.connect(self.gotoBuy)
        self.pushButton_2.clicked.connect(self.gotoSell)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_6.clicked.connect(self.gotoOptions)
        self.label_2.setText(name)

    def gotoSell(self):
        sell = SellWindow()
        widget.addWidget(sell)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoBuy(self):
        buy = BuyWindow()
        widget.addWidget(buy)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class OptionsWindow(QWidget):
    def __init__(self):
        super(OptionsWindow, self).__init__()
        loadUi(path+"options.ui", self)
        self.pushButton.clicked.connect(self.gotoCharts)
        self.pushButton_2.clicked.connect(self.gotoTitle)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.label_2.setText(name)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTitle(self):
        title = TitleWindow()
        widget.addWidget(title)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCharts(self):
        charts = Chart1Window()
        widget.addWidget(charts)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class Chart1Window(QWidget):
    def __init__(self):
        super(Chart1Window, self).__init__()
        loadUi(path+"charts.ui", self)
        self.loadChart1()
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)
        self.pushButton_7.clicked.connect(self.gotoCharts2)
        self.label_2.setText(name)

    def loadChart1(self):
        series = QPieSeries()
        conn = sqlite3.connect(path + 'Leskov.db')
        cur = conn.cursor()
        global client_id
        print('Balance for client ' + str(client_id))
        sqlquery = "SELECT currency_name, balance FROM Currencies, Balances WHERE Balances.currency_id=Currencies.currency_id AND Balances.client_id = " + str(client_id)
        tablerow = 0
        for row in cur.execute(sqlquery):
            print(row)
            series.append(row[0],row[1])
            tablerow += 1
        my_slice = series.slices()[3]
        my_slice.setExploded(True)
        my_slice.setLabelVisible(True)
        my_slice.setPen(QPen(Qt.yellow, 4))
        my_slice.setBrush(Qt.yellow)
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Валюты на счетах")
        chart.setTheme(QChart.ChartThemeDark)
        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)

        self.frame.setLayout(vbox)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCharts2(self):
        charts2 = Chart2Window()
        widget.addWidget(charts2)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class Chart2Window(QWidget):
    def __init__(self):
        super(Chart2Window, self).__init__()
        loadUi(path + "charts.ui", self)
        self.loadChart2()
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)
        self.pushButton_7.clicked.connect(self.gotoCharts1)
        self.label_2.setText(name)

    def loadChart2(self):
        num = 0
        global values
        categories = []
        chart = QChart()
        for i in values:
            series = QBarSeries()
            set = QBarSet(values[num][0][0])
            categories.append(values[num][0][0])
            set << values[num][0][3]
            series.append(set)
            chart.addSeries(series)
            num += 1

        chart.setTitle("Курсы валют на сегодня")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)

        self.frame.setLayout(vbox)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCharts1(self):
        charts1 = Chart1Window()
        widget.addWidget(charts1)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class BuyWindow(QWidget):
    def __init__(self):
        super(BuyWindow, self).__init__()
        loadUi(path+"buy.ui", self)
        self.getList()
        self.pushButton.clicked.connect(self.gotoOperations)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)
        self.listWidget.itemClicked.connect(self.itemClickedEvent)
        self.lineEdit.textChanged.connect(self.buyChange)
        self.pushButton_2.clicked.connect(self.BuyCurrency)
        self.label_2.setText(name)

    def BuyCurrency(self):
        global buy, amount
        buy = float(self.lineEdit.text())
        global currency_rate
        amount = buy * currency_rate
        conn = sqlite3.connect(path+'Leskov.db')
        cur = conn.cursor()
        global client_id, currency_name, currency_id
        sqlquery = 'SELECT currency_id, currency_name FROM Currencies WHERE currency_name = "'+currency_name+'"'
        cur.execute(sqlquery)
        try:
            # if currency already exists in table Currencies
            currency_id = cur.fetchone()[0]
            minus = 'UPDATE Balances SET balance = balance-'+str(amount)+' WHERE currency_id = 1 AND client_id='+str(client_id)
            cur.execute(minus)
            conn.commit()
            balance = 'SELECT currency_id FROM Balances WHERE client_id = '+str(client_id)+' AND currency_id = '+str(currency_id)
            cur.execute(balance)
            try:
                # if client already has selected currency
                exists = cur.fetchone()[0]
                plus = 'UPDATE Balances SET balance = balance+'+str(buy)+' WHERE currency_id='+str(exists)+' AND client_id='+str(client_id)
                cur.execute(plus)
                conn.commit()
                print('Balance updated')
            except:
                # if selected client does NOT have this currency yet
                new_balance_id_query = 'SELECT balance_id FROM Balances ORDER BY balance_id DESC'
                cur.execute(new_balance_id_query)
                new_balance_id = cur.fetchone()[0]
                add_new_balance = 'INSERT INTO Balances (balance_id,client_id,currency_id,balance) VALUES ('+str(new_balance_id+1)+','+str(client_id)+','+str(currency_id)+','+str(buy)+')'
                cur.execute(add_new_balance)
                conn.commit()
                print('created new balance for client')
        except:
            # if currency is new
            idquery = 'SELECT currency_id FROM Currencies ORDER BY currency_id DESC'
            cur.execute(idquery)
            last_id = cur.fetchone()[0]
            addquery = 'INSERT INTO Currencies (currency_id, currency_name) VALUES ('+str(last_id+1)+',"'+currency_name+'")'
            cur.execute(addquery)
            conn.commit()
            print('currency added')

        #insert operations
        new_operation_id_query = 'SELECT oper_id FROM Operations ORDER BY oper_id DESC'
        cur.execute(new_operation_id_query)
        global new_operation_id
        new_operation_id = cur.fetchone()[0]
        add_operation_minus = 'INSERT INTO Operations (oper_id,client_id,currency_id,change) VALUES ('+str(new_operation_id+1)+','+str(client_id)+',1,'+str(-amount)+')'
        cur.execute(add_operation_minus)
        conn.commit()
        add_operation_plus = 'INSERT INTO Operations (oper_id,client_id,currency_id,change) VALUES ('+str(new_operation_id+2)+','+str(client_id)+','+str(currency_id)+','+str(buy)+')'
        cur.execute(add_operation_plus)
        conn.commit()

        #create document
        doc = DocBuy()
        widget.addWidget(doc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def getList(self):
        global values
        row = 0
        for i in values:
            self.listWidget.addItem(values[row][0][1])
            row+=1

    def itemClickedEvent(self, item):
        global currency_name, currency_rate
        currency_name = item.text()
        print(currency_name)
        index = 0
        for i in values:
            if values[index][0][1] == currency_name:
                currency_rate = round(values[index][0][3] * 1.02, 2)
                self.rate.setText("Курс покупки валюты: " + str(currency_rate))
                self.buyname.setText(currency_name + ', сумма')
                self.rub.setText('Российский рубль')
            index+=1
        self.buyChange()


    def buyChange(self):
        global buy
        if self.lineEdit.text() == '':
            print('edit line is empty')
            self.rub.setText('Российский рубль')
        else:
            buy = float(self.lineEdit.text())
            global currency_rate
            self.rub.setText(str(buy*currency_rate)+' руб.')



class DocBuy(QWidget):
    def __init__(self):
        super(DocBuy, self).__init__()
        label = QLabel(self)
        pixmap = QPixmap(path+'ПокупкаJPG.jpg')
        label.setPixmap(pixmap)
        widget.setFixedHeight(1098)
        widget.setFixedWidth(777)
        loadUi(path+"doc_buy.ui", self)
        self.pushButton.clicked.connect(self.gotoCabinet)
        global new_operation_id, date, currency_id, buy, amount, currency_rate, client_id
        self.operation.setText(str(new_operation_id))
        self.date.setText(date)
        self.date_2.setText(date)
        self.curr_code.setText(str(currency_id))
        self.curr_sum.setText(str(buy))
        self.rub_sum.setText(str(amount))
        self.rate.setText(str(currency_rate))
        self.curr_sum_2.setText(str(sell))
        self.rub_sum_2.setText(str(amount))
        self.rate_2.setText(str(currency_rate))
        self.balance_num.setText('0000' + str(client_id))
        self.balance_num_2.setText('0000' + str(client_id + 1))


    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.setFixedHeight(600)
        widget.setFixedWidth(1000)
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class SellWindow(QWidget):
    def __init__(self):
        super(SellWindow, self).__init__()
        loadUi(path+"sell.ui", self)
        self.getList()
        self.label_2.setText(name)
        self.pushButton.clicked.connect(self.gotoOperations)
        self.pushButton_4.clicked.connect(self.gotoCabinet)
        self.pushButton_5.clicked.connect(self.gotoOperations)
        self.pushButton_6.clicked.connect(self.gotoOptions)
        self.listWidget.itemClicked.connect(self.itemClickedEvent)
        self.lineEdit.textChanged.connect(self.sellChange)
        self.pushButton_2.clicked.connect(self.SellCurrency)

    def SellCurrency(self):
        global sell, amount
        sell = float(self.lineEdit.text())
        global currency_rate, currency_id
        amount = sell * currency_rate
        conn = sqlite3.connect(path+'Leskov.db')
        cur = conn.cursor()
        global client_id, currency_name
        sqlquery = 'SELECT currency_id, currency_name FROM Currencies WHERE currency_name = "'+currency_name+'"'
        cur.execute(sqlquery)
        try:
            # if currency already exists in table Currencies
            currency_id = cur.fetchone()[0]
            minus = 'UPDATE Balances SET balance = balance+'+str(amount)+' WHERE currency_id = 1 AND client_id='+str(client_id)
            cur.execute(minus)
            conn.commit()
            balance = 'SELECT currency_id FROM Balances WHERE client_id = '+str(client_id)+' AND currency_id = '+str(currency_id)
            cur.execute(balance)
            try:
                # if client already has selected currency
                exists = cur.fetchone()[0]
                plus = 'UPDATE Balances SET balance = balance-'+str(sell)+' WHERE currency_id='+str(exists)+' AND client_id='+str(client_id)
                cur.execute(plus)
                conn.commit()
                print('Balance updated')
            except:
                # if selected client does NOT have this currency yet
                new_balance_id_query = 'SELECT balance_id FROM Balances ORDER BY balance_id DESC'
                cur.execute(new_balance_id_query)
                new_balance_id = cur.fetchone()[0]
                add_new_balance = 'INSERT INTO Balances (balance_id,client_id,currency_id,balance) VALUES ('+str(new_balance_id+1)+','+str(client_id)+','+str(currency_id)+','+str(-sell)+')'
                cur.execute(add_new_balance)
                conn.commit()
                print('created new balance for client')
        except:
            # if currency is new
            idquery = 'SELECT currency_id FROM Currencies ORDER BY currency_id DESC'
            cur.execute(idquery)
            last_id = cur.fetchone()[0]
            addquery = 'INSERT INTO Currencies (currency_id, currency_name) VALUES ('+str(last_id+1)+',"'+currency_name+'")'
            cur.execute(addquery)
            conn.commit()
            print('currency added')

        #insert operations
        new_operation_id_query = 'SELECT oper_id FROM Operations ORDER BY oper_id DESC'
        cur.execute(new_operation_id_query)
        global new_operation_id
        new_operation_id = cur.fetchone()[0]
        add_operation_minus = 'INSERT INTO Operations (oper_id,client_id,currency_id,change) VALUES ('+str(new_operation_id+1)+','+str(client_id)+',1,'+str(amount)+')'
        cur.execute(add_operation_minus)
        conn.commit()
        add_operation_plus = 'INSERT INTO Operations (oper_id,client_id,currency_id,change) VALUES ('+str(new_operation_id+2)+','+str(client_id)+','+str(currency_id)+','+str(-sell)+')'
        cur.execute(add_operation_plus)
        conn.commit()

        # create document
        doc = DocSell()
        widget.addWidget(doc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sellChange(self):
        global sell
        if self.lineEdit.text() == '':
            print('edit line is empty')
            self.rub.setText('Российский рубль')
        else:
            sell = float(self.lineEdit.text())
            global currency_rate
            self.rub.setText(str(sell*currency_rate)+' руб.')

    def itemClickedEvent(self, item):
        global currency_name, currency_rate
        currency_name = item.text()
        print(currency_name)
        index = 0
        for i in values:
            if values[index][0][1] == currency_name:
                currency_rate = round(values[index][0][3] * .98, 2)
                self.rate.setText("Курс продажи валюты: " + str(currency_rate))
                self.buyname.setText(currency_name + ', сумма')
                self.rub.setText('Российский рубль')
            index+=1
        self.sellChange()

    def gotoOptions(self):
        options = OptionsWindow()
        widget.addWidget(options)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoOperations(self):
        operations = OperationsWindow()
        widget.addWidget(operations)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def getList(self):
        global values
        row = 0
        for i in values:
            self.listWidget.addItem(values[row][0][1])
            row += 1


class DocSell(QWidget):
    def __init__(self):
        super(DocSell, self).__init__()
        label = QLabel(self)
        pixmap = QPixmap(path+'ПродажаJPG.jpg')
        label.setPixmap(pixmap)
        widget.setFixedHeight(1098)
        widget.setFixedWidth(777)
        loadUi(path+"doc_sell.ui", self)
        global new_operation_id, date, currency_id, sell, amount, currency_rate, client_id
        self.operation.setText(str(new_operation_id))
        self.date.setText(date)
        self.curr_code.setText(str(currency_id))
        self.curr_sum.setText(str(sell))
        self.rub_sum.setText(str(amount))
        self.rate.setText(str(currency_rate))
        self.balance_num.setText('0000'+str(client_id))
        self.balance_num_2.setText('0000' + str(client_id+1))
        self.pushButton.clicked.connect(self.gotoCabinet)

    def gotoCabinet(self):
        cabinet = Cabinet()
        widget.setFixedHeight(600)
        widget.setFixedWidth(1000)
        widget.addWidget(cabinet)
        widget.setCurrentIndex(widget.currentIndex() + 1)



# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    title = TitleWindow()
    widget.addWidget(title)
    widget.setFixedHeight(600)
    widget.setFixedWidth(1000)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print('exiting')