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
        Password = self.lineEdit_Password.text()
        db = QSqlDatabase.addDatabase("QPSQL") #before use it, install PyQt5, QPSQL
        db.setHostName('localhost')
        db.setPort(5432)
        db.setDatabaseName('print3dcompany')
        db.setUserName(self.lineEdit_Login.text())
        db.setPassword(Password)
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
            print("Connected!")
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

    def addFunc(self):
        self.tableWidget.setRowCount(0)
        tableName = self.lineEdit_TableName.text().lower() # Get the name of the table
        if (self.checkTableAccess(tableName, self.WhoIsIt)):
            self.getTableColumns(tableName)
            self.showTable(tableName)
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.rowPosition = self.tableWidget.rowCount() - 1

    def saveInDB(self, rowPosition, tableName):
        tableName = self.lineEdit_TableName.text().lower() # Get the name of the table
        numberOfColumns = len(self.tableColumnsList)
        insertInDB = list()
        for i in range(numberOfColumns):
            tableItem = self.tableWidget.item(rowPosition, i)
            insertInDB.append(tableItem.text())
        print (insertInDB)


    def checkTableAccess(self, tableName, userName):
        """
        Check permissions for each user.
        """
        if (userName == "manager"):
            managerAccess = ["clients", "orders"]
            if (tableName in managerAccess):
                return True
            else:
                errorWin = QMessageBox()
                errorWin.setIcon(QMessageBox.Critical)
                errorWin.setWindowTitle("Ошибка доступа")
                errorWin.setInformativeText("Нет доступа к запрошенной таблице.\nИли имя таблицы введено некорректно!")
                errorWin.exec_()
                return False
        elif (userName == "engineer"):
            engineerAccess = ["models_3d", "materials", "printers", "tasks"]
            if (tableName in engineerAccess):
                return True
            else:
                errorWin = QMessageBox()
                errorWin.setIcon(QMessageBox.Critical)
                errorWin.setWindowTitle("Ошибка доступа")
                errorWin.setInformativeText("Нет доступа к запрошенной таблице.\nИли имя таблицы введено некорректно!")
                errorWin.exec_()
                return False


    def getTableColumns(self, tableName):
        """
        Get column names from the table.
        """
        queryColumns = QSqlQuery()
        self.tableColumnsList = list()
        queryColumns.exec("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name=\'" + tableName + "\';") 
        while(queryColumns.next()):
            self.tableColumnsList.append(queryColumns.value(0))


    def allUsersWindow(self):
        tableName = self.lineEdit_TableName.text().lower() # Get the name of the table
        if (self.checkTableAccess(tableName, self.WhoIsIt)):
            self.getTableColumns(tableName)
            self.showTable(tableName)


    def showTable(self, tableName):
        self.tableWidget.setRowCount(0)
        query = QSqlQuery()
        query.exec("SELECT * FROM " + tableName + ";")
        numberOfColumns = len(self.tableColumnsList)
        self.tableWidget.setShowGrid(True) # User friendly interface
        self.tableWidget.setColumnCount(numberOfColumns)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(self.tableColumnsList)
        # Show the answer in table
        while(query.next()):
            self.rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowPosition)
            for i in range(0, numberOfColumns):
                self.tableWidget.setItem(self.rowPosition, i, QtWidgets.QTableWidgetItem(str(query.value(i))))
        
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.show()



def main():
    app = QtWidgets.QApplication(sys.argv)
    showAuthWin = Authorization()
    showAuthWin.show()
    app.exec_()

if __name__ == "__main__":
    main()