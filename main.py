import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import AuthorizationWindow
import MainWindowDesign

class Authorization(QtWidgets.QMainWindow, AuthorizationWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Authorization, self).__init__(parent)
        self.setupUi(self)
        self.Auth_button.clicked.connect(self.AuthorizationFunc)
    
    def AuthorizationFunc(self):
        # Connect to database
        self.dialog = MainWindow(self.lineEdit_Login.text()) # Create a class object and call it at the end to show the MainWindow
        #self.dialog = MainWindow("manager")
        Password = self.lineEdit_Password.text()
        db = QSqlDatabase.addDatabase("QPSQL") #before use it, install PyQt5, QPSQL
        db.setHostName('localhost')
        db.setPort(5432)
        db.setDatabaseName('print3dcompany')
        db.setUserName(self.lineEdit_Login.text())
        #db.setUserName('manager')
        db.setPassword(Password)
        #db.setPassword('12345')
        connected = db.open()
        if (not connected):
            #Window with error
            errorWin = QMessageBox()
            errorWin.setIcon(QMessageBox.Critical)
            errorWin.setWindowTitle("Ошибка подключения к базе данных")
            errorWin.setInformativeText(str(db.lastError().text()))
            errorWin.exec_()
            raise Exception('Wrong password or login.')
        else:
            Authorization.hide(self)
            self.dialog.show() # Show MainWindow
            
            
class MainWindow(QtWidgets.QDialog, MainWindowDesign.Ui_Dialog):
    def __init__(self, Login, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Button_Show.clicked.connect(self.allUsersWindow)
        self.WhoIsIt = Login
        self.Button_Add.clicked.connect(self.addFunc)
        self.Button_Save.clicked.connect(self.saveInDB)
        if (self.WhoIsIt == "manager"):
            self.comboBox.clear()
            self.comboBox.addItems(["Клиенты", "Заказы"])
        elif (self.WhoIsIt == "engineer"):
            self.comboBox.clear()
            self.comboBox.addItems(["3D модели", "Материалы", "Принтеры", "Задания"])

    def addFunc(self):
        '''
        Adds a row to a table
        '''
        self.tableWidget.setRowCount(0)
        self.showTable()
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        rowPositionCopy = self.tableWidget.rowCount()
        self.tableWidget.setItem(rowPositionCopy-1, 0, QtWidgets.QTableWidgetItem(str(rowPositionCopy)))


    def saveInDB(self):
        '''
        Saves the filled row in the database
        '''
        rowPositionCopy = self.tableWidget.rowCount() - 1
        numberOfColumns = len(self.tableColumnsList)
        insertInDB = list()
        for i in range(numberOfColumns):
            tableItem = self.tableWidget.item(rowPositionCopy, i)
            insertInDB.append(tableItem.text())
        querySaveDB = QSqlQuery()
        FormatStr = ["\'" + str(i) + "\'," for i in insertInDB]
        FormatStr[-1] = FormatStr[-1][:-1]
        querySaveDB.exec("INSERT INTO " + self.tableName + " VALUES(" + "".join(map(str, FormatStr)) + ");")



    def allUsersWindow(self):
        self.tableName = str(self.comboBox.currentText()) # Get the russian name of the table
        tableList = ["Клиенты", "Заказы", "3D модели", "Материалы", "Принтеры", "Задания"] # All tables
        replaceList = ["clients", "orders", "models_3d", "materials", "printers", "tasks"] # Replace tableList on this List
        self.tableName = replaceList[tableList.index(self.tableName)] # 

        # List with headers for every table
        clientsHeaderList = ["Имя", "Фамилия", "Отчество", "Номер телефона", "Эл. почта"]
        ordersHeaderList = ["Номер заказа", "Статус заказа", "Адрес доставки", "Дата формирования", "Примечание"]
        models_3dHeaderList = ["Название модели", "Путь к фалйу модели", "Размер модели"]
        materialsHeaderList = ["Материал", "Цвет", "Плотность", "Остаток", "Цена за кг"]
        printersHeaderList = ["Название принтера", "Область печати"]
        tasksHeaderList = ["Номер заказа", "Тип материала", "Цвет", "Статус", "Тип заполнения", "Процент заполнения", "Номер модели"]
        # Dictionary with headers list
        headerDictionary = {"clients":clientsHeaderList, "orders":ordersHeaderList, "models_3d":models_3dHeaderList, "materials":materialsHeaderList, "printers":printersHeaderList, "tasks":tasksHeaderList}
        self.tableColumnsList = headerDictionary[self.tableName]

        # Query for ShowFunc
        query = QSqlQuery()
        query.exec("SELECT * FROM " + self.tableName + ";")
        self.tableWidget.setShowGrid(True) # User friendly interface
        numberOfColumns = len(self.tableColumnsList)
        self.tableWidget.setColumnCount(numberOfColumns)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(self.tableColumnsList)

        # Clear the table
        self.tableWidget.setRowCount(0)
        
        if (self.tableName == "clients"):
            self.clientsShowFunc(query)
        elif (self.tableName == "orders"):
            self.ordersShowFunc(query)


    def clientsShowFunc(self, query):
        numberOfColumns = len(self.tableColumnsList)
        # Show the answer in table
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)
            for i in range(0, numberOfColumns):
                self.tableWidget.setItem(self.rowPosition, i, QtWidgets.QTableWidgetItem(str(query.value(i+1))))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.show()

    def ordersShowFunc(self, query):
        # Show the answer in table
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)

            self.tableWidget.setItem(self.rowPosition, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
            self.tableWidget.setItem(self.rowPosition, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
            self.tableWidget.setItem(self.rowPosition, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))
            self.tableWidget.setItem(self.rowPosition, 3, QtWidgets.QTableWidgetItem(str(query.value(4))))
            self.tableWidget.setItem(self.rowPosition, 4, QtWidgets.QTableWidgetItem(str(query.value(5))))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.show()
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    showAuthWin = Authorization()
    showAuthWin.show()
    app.exec_()

if __name__ == "__main__":
    main()