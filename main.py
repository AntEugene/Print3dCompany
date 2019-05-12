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
        Login = self.lineEdit_Login.text()
        self.dialog = MainWindow(Login) # Create a class object and call it at the end to show the MainWindow
        Password = self.lineEdit_Password.text()
        db = QSqlDatabase.addDatabase("QPSQL") #before use it, install PyQt5, QPSQL
        db.setHostName('localhost')
        db.setPort(5432)
        db.setDatabaseName('print3dcompany')
        db.setUserName(Login)
        #db.setUserName('engineer')
        #db.setPassword(Password)
        db.setPassword('12345')
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
        self.comboBox.activated.connect(self.allUsersWindow)
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
        self.allUsersWindow()
        self.tableWidget.insertRow(self.tableWidget.rowCount())


    def getTableColumns(self, tableName):
        """
        Get column names from the table.
        """
        queryColumns = QSqlQuery()
        getTableColumnsList = list()
        queryColumns.exec("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name=\'" + tableName + "\';") 
        while(queryColumns.next()):
            getTableColumnsList.append(queryColumns.value(0))
        return getTableColumnsList


    def saveInDB(self):
        '''
        Saves the filled row in the database
        '''
        # Select the right table
        if (self.tableName == "clients"):
            self.clientsSave(self.filledData())
        elif (self.tableName == "orders" or self.tableName == "materials" or self.tableName == "printers"):
            self.defaultTableSave(self.filledData())
        elif (self.tableName == "models_3d"):
            self.models_3dSave(self.filledData())
        elif (self.tableName == "tasks"):
            self.tasksSave()

    def filledData(self):
        rowPositionCopy = self.tableWidget.rowCount() - 1
        numberOfColumns = len(self.tableColumnsList)
        insertInDB = list()
        # Save data in list
        for i in range(numberOfColumns):
            tableItem = self.tableWidget.item(rowPositionCopy, i)
            insertInDB.append(tableItem.text())
        return insertInDB

    def clientsSave(self, insertInDB):
        columns = self.getTableColumns(self.tableName)
        columns.pop(0)
        columns = [str(i) + ", " for i in columns]
        columns[-1] = columns[-1][:-2] # Delete the last comma and space
        querySaveDB = QSqlQuery()
        # Formats the lines in the list and send them to the server
        FormatStr = ["\'" + str(i) + "\'," for i in insertInDB]
        FormatStr[-1] = FormatStr[-1][:-1] # Delete the last comma
        querySaveDB.exec("INSERT INTO " + self.tableName + "(" + "".join(map(str, columns)) + ") VALUES(" + "".join(map(str, FormatStr)) + ");")


    def tasksSave(self):
        # Can't be saved in DB
        errorWin = QMessageBox()
        errorWin.setIcon(QMessageBox.Critical)
        errorWin.setWindowTitle("Ошибка записи в базу данных")
        errorWin.setInformativeText("Вы не можете изменить эту таблицу")
        errorWin.exec_()


    def defaultTableSave(self, insertInDB):
        querySaveDB = QSqlQuery()
        # Formats the lines in the list and send them to the server
        FormatStr = ["\'" + str(i) + "\'," for i in insertInDB]
        FormatStr[-1] = FormatStr[-1][:-1] # Delete the last comma
        querySaveDB.exec("INSERT INTO " + self.tableName + " VALUES(" + "".join(map(str, FormatStr)) + ");")


    def models_3dSave(self, insertInDB):
        columns = self.getTableColumns(self.tableName)
        columns.pop(0)
        columns = [str(i) + ", " for i in columns]
        columns[-1] = columns[-1][:-2] # Delete the last comma and space
        querySaveDB = QSqlQuery()
        # Formats the lines in the list and send them to the server
        FormatStr = ["\'" + str(i) + "\'," for i in insertInDB]
        FormatStr[-1] = FormatStr[-1][:-1] # Delete the last comma
        querySaveDB.exec("INSERT INTO " + self.tableName + "(" + "".join(map(str, columns)) + ") VALUES(" + "".join(map(str, FormatStr)) + ");")


    def allUsersWindow(self):
        """
        This function shows the table selected in the "comboBox"
        """
        self.tableName = str(self.comboBox.currentText()) # Get the russian name of the table
        tableList = ["Клиенты", "Заказы", "3D модели", "Материалы", "Принтеры", "Задания"] # All tables
        replaceList = ["clients", "orders", "models_3d", "materials", "printers", "tasks"] # Replace tableList on this List
        self.tableName = replaceList[tableList.index(self.tableName)] # 

        # List with headers for every table
        clientsHeaderList = ["Имя", "Фамилия", "Отчество", "Номер телефона", "Эл. почта"]
        ordersHeaderList = ["Номер заказа", "Номер клиента", "Статус заказа", "Адрес доставки", "Дата формирования", "Примечание"]
        models_3dHeaderList = ["Название модели", "Путь к фалйу модели", "Размер модели"]
        materialsHeaderList = ["Материал", "Цвет", "Плотность", "Остаток", "Цена за кг"]
        printersHeaderList = ["Номер принтера", "Название принтера", "Область печати"]
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

        # Select the right table u must
        if (self.tableName == "clients"):
            self.clientsShowFunc(query)
        elif (self.tableName == "orders" or self.tableName == "materials" or self.tableName == "printers"):
            self.defaultShowFunc(query)
        elif (self.tableName == "models_3d"):
            self.models_3dShowFunc(query)
        elif (self.tableName == "tasks"):
            self.tasksShowFunc(query)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.show()

    def defaultShowFunc(self, query):
        numberOfColumns = len(self.tableColumnsList)
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)
            for i in range(numberOfColumns):
                self.tableWidget.setItem(self.rowPosition, i, QtWidgets.QTableWidgetItem(str(query.value(i))))
            

    def tasksShowFunc(self, query):
        numberOfColumns = len(self.tableColumnsList)
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)

            for i in range(numberOfColumns):
                self.tableWidget.setItem(self.rowPosition, i, QtWidgets.QTableWidgetItem(str(query.value(i+2))))
            

    def models_3dShowFunc(self, query):
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)

            self.tableWidget.setItem(self.rowPosition, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
            self.tableWidget.setItem(self.rowPosition, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
            self.tableWidget.setItem(self.rowPosition, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))


    def clientsShowFunc(self, query):
        # Show the answer in table
        numberOfColumns = len(self.tableColumnsList)
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)

            for i in range(0, numberOfColumns):
                self.tableWidget.setItem(self.rowPosition, i, QtWidgets.QTableWidgetItem(str(query.value(i+1))))

        

def main():
    app = QtWidgets.QApplication(sys.argv)
    showAuthWin = Authorization()
    showAuthWin.show()
    app.exec_()

if __name__ == "__main__":
    main()