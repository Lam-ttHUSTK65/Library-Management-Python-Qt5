import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUiType
import mysql.connector as con
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from xlrd import *
from xlsxwriter import *
import datetime
import pyqtgraph as pg
from PyQt5.QtWidgets import *

ui, _ = loadUiType('lib_ui.ui')
uii, _ = loadUiType('login.ui')

class MainAppUser(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False)
        self.button_trigger()
        self.Email_Access = "user1@gmail.com"
        self.book_data = []

        self.Show_User_Info()
        self.Show_Loan()
        self.Show_Fine()
        self.Show_Book()


    def button_trigger(self):
        self.butt_u.clicked.connect(self.open_loan)
        self.butt_u_2.clicked.connect(self.open_find)
        self.butt_u_3.clicked.connect(self.open_fine)
        self.butt_u_4.clicked.connect(self.open_pass)
        self.butt_u_5.clicked.connect(self.open_theme)

        self.butt_t.clicked.connect(self.theme_dark)
        self.butt_t_2.clicked.connect(self.theme_light)
        self.butt_t_3.clicked.connect(self.theme_blue)
        self.butt_t_4.clicked.connect(self.theme_pink)

        self.pushButton_6.clicked.connect(self.Search_Book)
        self.pushButton_8.clicked.connect(self.Change_password)



    def button_choose(self, now_button):
        for each in [self.butt_u, self.butt_u_2, self.butt_u_3, self.butt_u_4, self.butt_u_5]:
            each.setStyleSheet('''
                QPushButton {text-align: left; background-color: rgb(255,255,127); color: rgb(0,0,0);}
                QPushButton:hover {background-color: rgb(170,170,255);}''')
        now_button.setStyleSheet('text-align: left; background-color: rgb(170,170,255); color: rgb(0,0,0);')

    ###################################################################################
    ########################################OPEN#######################################
    def open_loan(self):
        self.tabWidget.setCurrentIndex(0)
        self.button_choose(self.butt_u)

    def open_find(self):
        self.tabWidget.setCurrentIndex(1)
        self.button_choose(self.butt_u_2)

    def open_fine(self):
        self.tabWidget.setCurrentIndex(2)
        self.button_choose(self.butt_u_3)

    def open_pass(self):
        self.tabWidget.setCurrentIndex(3)
        self.button_choose(self.butt_u_4)

    def open_theme(self):
        self.tabWidget.setCurrentIndex(4)
        self.button_choose(self.butt_u_5)


    ###################################################################################
    #######################################THEME#######################################
    def theme_dark(self):
        self.setStyleSheet('background-color: rgb(0,0,0); color: rgb(255,255,255);')

    def theme_light(self):
        self.setStyleSheet('')

    def theme_blue(self):
        self.setStyleSheet('''
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(63, 66, 172, 255), stop:1 rgba(207, 255, 255, 255));''')

    def theme_pink(self):
        self.setStyleSheet('''
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(255, 134, 255, 234), stop:1 rgba(255, 255, 255, 255));''')

    ###################################################################################
    #######################################SHOW########################################

    def Show_User_Info(self):
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()
        cursor.execute("select * from user where email = %s", (self.Email_Access,))
        result = cursor.fetchone()
        if result:
            self.label_u_5.setText(result[1])  # Hiển thị tên người dùng
            self.label_u_6.setText(str(result[0]))  # Hiển thị ID
            self.label_u_7.setText(result[2])  # Hiển thị địa chỉ email
            self.label_u_8.setText(str(result[5]))  # Hiển thị số nợ

    def Show_Fine(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()
        user_email = self.label_u_7.text()

        self.cur.execute('''
                            SELECT loan.ID, copyBook.ID, book.Title, loan.Loan_date, loan.Due_date, loan.Return_date, loan.Fine, loan.Reason, loan.Status
                            FROM loan
                            JOIN user ON loan.User_ID = user.ID
                            JOIN copyBook ON loan.CopyBook_ID = copyBook.ID
                            JOIN book ON copyBook.Book_ID = book.ID
                            JOIN category ON book.Category_ID = category.ID
                            JOIN publisher ON book.Publisher_ID = publisher.ID
                            WHERE user.Email = %s AND loan.fine != 0
                            ORDER BY loan.ID DESC;
                        ''', (user_email,))

        data = self.cur.fetchall()

        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 8:
                    if item == 0:
                        item = "Not Paid Yet"
                    elif item == 1:
                        item = "Paid"
                    else:
                        item = "Unknown"
                self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

        if self.tableWidget_3.item(self.tableWidget_3.rowCount() - 1, 0) is None:
            self.tableWidget_3.removeRow(self.tableWidget_3.rowCount() - 1)

    def Show_Loan(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()
        user_email = self.label_u_7.text()

        self.cur.execute('''
                            SELECT loan.ID, book.Title, copyBook.ID, category.Name, publisher.Name, loan.Loan_date, loan.Due_date, loan.Status
                            FROM loan
                            JOIN user ON loan.User_ID = user.ID
                            JOIN copyBook ON loan.CopyBook_ID = copyBook.ID
                            JOIN book ON copyBook.Book_ID = book.ID
                            JOIN category ON book.Category_ID = category.ID
                            JOIN publisher ON book.Publisher_ID = publisher.ID
                            WHERE user.Email = %s
                            ORDER BY loan.ID DESC;
                        ''', (user_email,))

        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 7:
                    if item == 0:
                        item = "Borrowing"
                    elif item == 1:
                        item = "Returned"
                    else:
                        item = "Unknown"
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

        if self.tableWidget.item(self.tableWidget.rowCount() - 1, 0) is None:
            self.tableWidget.removeRow(self.tableWidget.rowCount() - 1)

    def Show_Book(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT
                                 book.Title as Book_Title,
                                 book.ISBN,
                                 book.Description as Book_Description,
                                 category.Name as Book_Category,
                                 GROUP_CONCAT(DISTINCT author.Name SEPARATOR ', ') as Book_Author,
                                 publisher.Name as Book_Publisher,
                                 COUNT(DISTINCT CASE WHEN copyBook.Available = 1 THEN copyBook.ID END) as Available
                             FROM
                                 book
                                 JOIN writing ON book.ID = writing.Book_ID
                                 JOIN author ON author.ID = writing.Author_ID
                                 JOIN category ON book.Category_ID = category.ID
                                 JOIN publisher ON book.Publisher_ID = publisher.ID
                                 LEFT JOIN copyBook ON book.ID = copyBook.Book_ID
                             GROUP BY
                                 book.ID;
                             ''')

        self.book_data = self.cur.fetchall()  # Lưu dữ liệu vào biến instance

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row, form in enumerate(self.book_data):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
        if self.tableWidget_2.item(self.tableWidget_2.rowCount() - 1, 0) is None:
            self.tableWidget_2.removeRow(self.tableWidget_2.rowCount() - 1)
        self.db.close()

    ###################################################################################
    #####################################FUNCTION BOTTON###############################
    def Search_Book(self):
        search_criteria = self.comboBox.currentText()
        search_text = self.lineEdit.text()

        # Xử lý logic tìm kiếm và lọc dữ liệu
        # Tìm kiếm theo tiêu chí
        search_results = []
        for row in self.book_data:
            if search_criteria == 'Tên sách' and search_text.lower() in row[0].lower():
                search_results.append(row)
                # Tìm kiếm theo tác giả
            elif search_criteria == 'Tác giả':
                for author in row[4].split(', '):
                    if search_text.lower() in author.lower():
                        search_results.append(row)
                        break  # Chỉ cần sách có ít nhất 1 tác giả thỏa mãn điều kiện là được

            elif search_criteria == 'Thể loại' and search_text.lower() in row[3].lower():
                search_results.append(row)
            elif search_criteria == 'Nhà xuất bản' and search_text.lower() in row[5].lower():
                search_results.append(row)

        # Hiển thị kết quả tìm kiếm trên tableWidget_2
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row, form in enumerate(search_results):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
        if self.tableWidget_2.item(self.tableWidget_2.rowCount() - 1, 0) is None:
            self.tableWidget_2.removeRow(self.tableWidget_2.rowCount() - 1)
        # Nếu không nhập thông tin tìm kiếm thì hiển thị lại toàn bộ dữ liệu
        if not search_text:
            self.Show_Book()

    def Change_password(self):
        current_password = self.lineEdit_2.text()
        new_password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()
        user_email = self.label_u_7.text()

        if current_password == "" or new_password == "" or confirm_password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        # Truy vấn database dùng email để lấy mật khẩu hiện tại
        self.db = con.connect(host='localhost', user='root', password='1234', db='20-2')
        self.cur = self.db.cursor()
        self.cur.execute("SELECT password FROM user WHERE email=%s", (user_email,))
        current_password_db = self.cur.fetchone()[0]  # Lấy phần tử đầu tiên của tuple

        if current_password != current_password_db:
            QMessageBox.warning(self, "Thông báo", "Mật khẩu hiện tại không chính xác.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Thông báo", "Mật khẩu mới không trùng khớp.")
            return

        if new_password == current_password:
            QMessageBox.warning(self, "Thông báo", "Mật khẩu mới không được giống mật khẩu hiện tại.")
            return

        # Cập nhật mật khẩu mới vào cơ sở dữ liệu
        self.cur.execute("UPDATE user SET password=%s WHERE email=%s", (new_password, user_email))
        self.db.commit()

        QMessageBox.information(self, "Thông báo", "Cập nhật mật khẩu thành công.")
def main():
    app = QApplication(sys.argv)
    window = MainAppUser()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()