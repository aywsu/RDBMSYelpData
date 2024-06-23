"""
Group Name: ZA
Members: Zachary Werle, Aviv Yaaran
Code adapted from https://gist.github.com/arslanay/d61b1636d563e18f2680e39803f12282 with the help of instructional videos
provided in the Project Resource Videos Page on Canvas.
"""
import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QLabel
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap

qtCreatorFile = "App.ui" # Enter file here.
user = 'postgres'
password = '451'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.businessInput.textChanged.connect(self.businessSearch)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.updateZipcodeStats)
        self.ui.stateList.currentTextChanged.connect(self.updateTopCategoryTable)
        self.ui.cityList.itemSelectionChanged.connect(self.updateTopCategoryTable)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.updateTopCategoryTable)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.updatePopularBusinessTable)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.updateSucessfulBusinessTable)
        self.ui.categoryList.itemSelectionChanged.connect(self.updatePopularBusinessTable)

        
                

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("host='localhost' port='5432' dbname='ms2' user='" + user + "' password='" + password + "'")
            print(conn)
        except:
            print('Unable to connect to database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result
    
    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = 'SELECT DISTINCT state FROM business ORDER BY state;'
        try:
            result = self.executeQuery(sql_str)
            for row in result:
                self.ui.stateList.addItem(row[0])
        except:
            print('Load State List Query Failed')
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        if self.ui.stateList.currentIndex() >= 0:
            self.ui.cityList.clear()
            self.ui.zipCodeList.clear()
            self.ui.categoryList.clear()
            state = self.ui.stateList.currentText()
            sql_str = 'SELECT DISTINCT city FROM business WHERE state=\'' + state + '\' ORDER BY city;'
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.cityList.addItem(row[0])
            except:
                print('Load City List Query Failed')
            
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = 'SELECT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE state=\'' + state + '\' ORDER BY name;'
            try:
                result = self.executeQuery(sql_str)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'State', 'Zipcode', 'Stars', 'Review Count', 'Average Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(7, 200)
                self.ui.businessTable.setColumnWidth(8, 200)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Load Business Table Query Failed')

    def cityChanged(self):    
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0:
            self.ui.zipCodeList.clear()
            self.ui.categoryList.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = 'SELECT DISTINCT zipcode FROM business WHERE state=\'' + state + '\' AND city=\'' + city + '\' ORDER BY zipcode;'
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.zipCodeList.addItem(str(row[0]))
            except:
                print('Load ZIP Code List Query Failed')

            try:
                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)
                sql_str = 'SELECT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE city=\'' + city + '\' AND state=\'' + state + '\' ORDER BY name;'
                result = self.executeQuery(sql_str)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'State', 'Zipcode', 'Stars', 'Review Count', 'Average Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(7, 200)
                self.ui.businessTable.setColumnWidth(8, 200)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Load Business Table Query Failed')


    def zipcodeChanged(self):    
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
            self.ui.categoryList.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            sql_str = 'SELECT DISTINCT category FROM categories WHERE business_id IN (SELECT DISTINCT business_id FROM business WHERE state=\'' + state + '\' AND city=\'' + city + '\' AND zipcode=\'' + zipcode + '\') ORDER BY category;'
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.categoryList.addItem(row[0])
            except:
                print('Load Category List Query Failed')

            try:
                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE state=\'' + state + '\' AND city=\'' + city + '\' AND zipcode=\'' + zipcode + '\' ORDER BY name;'
                result = self.executeQuery(sql_str)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'State', 'Zipcode', 'Stars', 'Review Count', 'Average Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(7, 200)
                self.ui.businessTable.setColumnWidth(8, 200)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Load Business Table Query Failed')

    def categoryChanged(self):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0 and len(self.ui.categoryList.selectedItems()) > 0:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()
            try:
                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE business_id IN (SELECT business_id FROM categories WHERE business_id IN (SELECT business_id FROM business WHERE city=\'' + city + '\' AND state=\'' + state + '\' AND zipcode=\'' + zipcode + '\') AND category=\'' + category + '\') ORDER BY name;'
                result = self.executeQuery(sql_str)
                self.ui.businessTable.setColumnCount(len(result[0]))
                self.ui.businessTable.setRowCount(len(result))
                self.ui.businessTable.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'State', 'Zipcode', 'Stars', 'Review Count', 'Average Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(7, 200)
                self.ui.businessTable.setColumnWidth(8, 200)
                currentRowCount = 0
                for row in result:
                    for colCount in range(0, len(result[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Load Business Table Query Failed')

    def businessSearch(self):
        if self.ui.businessInput.text() != '':
            name = self.ui.businessInput.text()
            if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0 and len(self.ui.categoryList.selectedItems()) > 0:
                state = self.ui.stateList.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                zipcode = self.ui.zipCodeList.selectedItems()[0].text()
                category = self.ui.categoryList.selectedItems()[0].text()
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE business_id IN (SELECT business_id FROM categories WHERE business_id IN (SELECT business_id FROM business WHERE city=\'' + city + '\' AND state=\'' + state + '\' AND zipcode=\'' + zipcode + '\') AND category=\'' + category + '\') AND name LIKE \'%' + name + '%\' ORDER BY name;'
            elif self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
                state = self.ui.stateList.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                zipcode = self.ui.zipCodeList.selectedItems()[0].text()
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE state=\'' + state + '\' AND city=\'' + city + '\' AND zipcode=\'' + zipcode + '\' AND name LIKE \'%' + name + '%\' ORDER BY name;'
            elif self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0:
                state = self.ui.stateList.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE city=\'' + city + '\' AND state=\'' + state + '\' AND name LIKE \'%' + name + '%\' ORDER BY name;'
            elif self.ui.stateList.currentIndex() >= 0:
                state = self.ui.stateList.currentText()
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE state=\'' + state + '\' AND name LIKE \'%' + name + '%\' ORDER BY name;'
            else:
                sql_str = 'SELECT DISTINCT name,address,city,state,zipcode,stars,reviewcount,reviewrating,numcheckins FROM business WHERE name LIKE \'%' + name + '%\' ORDER BY name;'
            try:
                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)
                result = self.executeQuery(sql_str)
                if len(result) > 0:
                    self.ui.businessTable.setColumnCount(len(result[0]))
                    self.ui.businessTable.setRowCount(len(result))
                    self.ui.businessTable.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'State', 'Zipcode', 'Stars', 'Review Count', 'Average Rating', 'Number of Checkins'])
                    self.ui.businessTable.resizeColumnsToContents()
                    self.ui.businessTable.setColumnWidth(0, 300)
                    self.ui.businessTable.setColumnWidth(1, 300)
                    self.ui.businessTable.setColumnWidth(2, 100)
                    self.ui.businessTable.setColumnWidth(7, 200)
                    self.ui.businessTable.setColumnWidth(8, 200)
                    currentRowCount = 0
                    for row in result:
                        for colCount in range(0, len(result[0])):
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
            except:
                print('Load Business Table Query Failed')


    def updateZipcodeStats(self):

        if len(self.ui.zipCodeList.selectedItems()) <= 0:
            for i in reversed(range(self.ui.topCategoryTable.rowCount())):
                self.ui.topCategoryTable.removeRow(i)
            self.ui.numBusinessesLabel.setText('')
            self.ui.totalPop.setText('')
            self.ui.avgIncome.setText('')
        #display number of businesses
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            # self.ui.zipCodeList.clear()
            try:
                sql_str = 'SELECT COUNT(*) AS business_count FROM business WHERE zipcode=\'' + zipcode + '\''
                result = self.executeQuery(sql_str)
                business_count = result[0][0]
                self.ui.numBusinessesLabel.setText(str(business_count))
            except Exception as e:
                print('Loading Number of Businesses Failed:', e)


            if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
                zipcode = self.ui.zipCodeList.selectedItems()[0].text()
                # self.ui.zipCodeList.clear()
                try:
                    sql_str = 'SELECT totalpopulation FROM zipcodedata WHERE zipcode = \''+zipcode+'\''
                    result = self.executeQuery(sql_str)
                    totalPop = result[0][0]
                    self.ui.totalPop.setText(str(totalPop))
                except Exception as e:
                    print('Loading Number of Businesses Failed:', e)


            if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
                zipcode = self.ui.zipCodeList.selectedItems()[0].text()
                # self.ui.zipCodeList.clear()
                try:
                    sql_str = 'SELECT avgincome FROM zipcodedata WHERE zipcode = \''+zipcode+'\''
                    result = self.executeQuery(sql_str)
                    totalPop = result[0][0]
                    self.ui.avgIncome.setText(str(totalPop))
                except Exception as e:
                    print('Loading Number of Businesses Failed:', e)



        
        

        

    def updateTopCategoryTable(self):

        if len(self.ui.zipCodeList.selectedItems()) > 0:
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            #category = self.ui.categoryList.selectedItems()[0].text()            # self.ui.zipCodeList.clear()
            try:
                sql_str = 'SELECT COUNT(business_id),category FROM categories WHERE business_id IN (SELECT business_id FROM business WHERE zipcode=\''+zipcode+'\') GROUP BY category ORDER BY COUNT(business_id) DESC;'
                result = self.executeQuery(sql_str)
                
            except Exception as e:
                print('Loading Top Categories Failed:', e)

            try:
                for i in reversed(range(self.ui.topCategoryTable.rowCount())):
                    self.ui.topCategoryTable.removeRow(i)
                result = self.executeQuery(sql_str)
                if len(result) > 0:
                    self.ui.topCategoryTable.setColumnCount(len(result[0]))
                    self.ui.topCategoryTable.setRowCount(len(result))
                    self.ui.topCategoryTable.setHorizontalHeaderLabels(['# of Businesses','Categories'])
                    self.ui.topCategoryTable.resizeColumnsToContents()
                    self.ui.topCategoryTable.setColumnWidth(0, 150)
                    self.ui.topCategoryTable.setColumnWidth(1, 150)
               
                    currentRowCount = 0
                    for row in result:
                        for colCount in range(0, len(result[0])):
                            self.ui.topCategoryTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
            except Exception as e:
                print('Loading Top Categories Failed:', e)
            
        
    
    def updatePopularBusinessTable(self):
        if len(self.ui.categoryList.selectedItems()) <= 0:
            for i in reversed(range(self.ui.popularBusinessTable.rowCount())):
                    self.ui.popularBusinessTable.removeRow(i)
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0 and len(self.ui.categoryList.selectedItems()) > 0:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()
            try:
                for i in reversed(range(self.ui.popularBusinessTable.rowCount())):
                    self.ui.popularBusinessTable.removeRow(i)
                sql_str = 'SELECT name,numCheckins,reviewCount FROM business WHERE business_id IN ' + \
                          '(SELECT business_id FROM categories WHERE category=\'' + category + '\') AND city=\'' + city + '\' AND state=\'' + state + '\' AND zipcode=\'' + zipcode + '\' AND numCheckins >= (SELECT AVG(numCheckins) AS avgNumCheckins FROM business WHERE business_id IN ' + \
                          '(SELECT business_id FROM categories WHERE category=\'' + category + '\') AND city=\'' + city + '\' AND state=\'' + state + '\' AND zipcode=\'' + zipcode + '\') ORDER BY numCheckins DESC;'
                result = self.executeQuery(sql_str)
                if len(result) > 0:
                    self.ui.popularBusinessTable.setColumnCount(len(result[0]))
                    self.ui.popularBusinessTable.setRowCount(len(result))
                    self.ui.popularBusinessTable.setHorizontalHeaderLabels(['Name', 'Number of Checkins', 'Review Count'])
                    self.ui.popularBusinessTable.resizeColumnsToContents()
                    self.ui.popularBusinessTable.setColumnWidth(0, 250)
                    self.ui.popularBusinessTable.setColumnWidth(1, 250)
                    self.ui.popularBusinessTable.setColumnWidth(2, 50)
                    currentRowCount = 0
                    for row in result:
                        for colCount in range(0, len(result[0])):
                            self.ui.popularBusinessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
            except:
                print('Load Popular Business Table Query Failed')

    def updateSucessfulBusinessTable(self):
         if len(self.ui.zipCodeList.selectedItems()) <= 0:
            for i in reversed(range(self.ui.successfulBusinessTable.rowCount())):
                    self.ui.successfulBusinessTable.removeRow(i)
         if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipCodeList.selectedItems()) > 0:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipCodeList.selectedItems()[0].text()
            try:
                for i in reversed(range(self.ui.successfulBusinessTable.rowCount())):
                    self.ui.successfulBusinessTable.removeRow(i)
                sql_str = 'SELECT name,reviewrating,reviewcount FROM business WHERE reviewrating > 3.5 AND city=\'' + city + '\' AND state=\'' + state + '\' AND zipcode=' + zipcode + ' ORDER BY reviewrating DESC;'
                result = self.executeQuery(sql_str)
                if len(result) > 0:
                    self.ui.successfulBusinessTable.setColumnCount(len(result[0]))
                    self.ui.successfulBusinessTable.setRowCount(len(result))
                    self.ui.successfulBusinessTable.setHorizontalHeaderLabels(['Name', 'Average Rating', 'Review Count'])
                    self.ui.successfulBusinessTable.resizeColumnsToContents()
                    self.ui.successfulBusinessTable.setColumnWidth(0, 250)
                    self.ui.successfulBusinessTable.setColumnWidth(1, 250)
                    self.ui.successfulBusinessTable.setColumnWidth(2, 50)
                    currentRowCount = 0
                    for row in result:
                        for colCount in range(0, len(result[0])):
                            self.ui.successfulBusinessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
            except:
                print('Load Successful Business Table Query Failed')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())