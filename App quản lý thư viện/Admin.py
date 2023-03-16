import random
import sys
import pandas as pd
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
import re
import datetime


def Create_box_Cate(comboBox):
    # Kết nối tới database
    db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()

    # Hiển thị dữ liệu lên comboBox
    for category in categories:
        comboBox.addItem(category[1])

    # Đóng kết nối tới database
    cursor.close()
    db.close()

def Create_box_Pub(comboBox):
    # Kết nối tới database
    db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM publisher")
    publishers = cursor.fetchall()

    # Hiển thị dữ liệu lên comboBox
    for publisher in publishers:
        comboBox.addItem(publisher[1])

    # Đóng kết nối tới database
    cursor.close()
    db.close()

uiii, _ = loadUiType('library2 - Copy.ui')

class MainApp(QMainWindow, uiii):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False)
        self.trigger_buttons()
        self.User_Email = ''

        self.Show_Info()
        self.Show_Loan()
        self.Show_Book()
        self.Show_Copybook()
        self.Show_User()
        self.Show_Publisher()
        self.Show_Category()
        self.Show_Author()



        Create_box_Cate(self.comboBox_9)
        Create_box_Pub(self.comboBox_10)


    def trigger_buttons(self):
        self.butt_a.clicked.connect(self.open_loan_tab)
        self.butt_a_2.clicked.connect(self.open_return_tab)
        self.butt_a_3.clicked.connect(self.open_book_tab)
        self.butt_a_4.clicked.connect(self.open_user_tab)
        self.butt_a_5.clicked.connect(self.open_other_tab)
        self.butt_a_6.clicked.connect(self.open_theme_tab)
        self.butt_th.clicked.connect(self.theme_dark)
        self.butt_th_2.clicked.connect(self.theme_light)
        self.butt_th_3.clicked.connect(self.theme_blue)
        self.butt_th_4.clicked.connect(self.theme_pink)

        self.pushButton_30.clicked.connect(self.Add_Loan_today)
        self.pushButton_34.clicked.connect(self.Search_Loan_Book)
        self.pushButton_36.clicked.connect(self.Change_fine_reason)
        self.pushButton_35.clicked.connect(self.Pay_fine)
        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_17.clicked.connect(self.Add_Copybook)
        self.pushButton_9.clicked.connect(self.Search_Book)
        self.pushButton_8.clicked.connect(self.Edit_Book)
        self.pushButton_10.clicked.connect(self.Delete_Book)
        self.pushButton_11.clicked.connect(self.Add_New_User)
        self.pushButton_12.clicked.connect(self.Search_User)
        self.pushButton_13.clicked.connect(self.Edit_User)
        self.pushButton_22.clicked.connect(self.Delete_User)
        self.pushButton_14.clicked.connect(self.Add_New_Category)
        self.pushButton_16.clicked.connect(self.Add_New_Publisher)
        self.pushButton_23.clicked.connect(self.Search_Author_Book)
        self.pushButton_24.clicked.connect(self.Refresh_Author)

        self.pushButton_29.clicked.connect(self.Export_today_loan)

    def buttons_choose(self, now_button):
        for each in [self.butt_a, self.butt_a_2, self.butt_a_3, self.butt_a_4, self.butt_a_5, self.butt_a_6]:
            each.setStyleSheet('''
                QPushButton {text-align: left; background-color: rgb(255,255,127); color: rgb(0,0,0);}
                QPushButton:hover {background-color: rgb(170,170,255);}''')
        now_button.setStyleSheet('text-align: left; background-color: rgb(170,170,255); color: rgb(0,0,0);')


    ###################################################################################
    ########################################OPEN#######################################
    def open_loan_tab(self):
        self.tabWidget.setCurrentIndex(0)
        self.buttons_choose(self.butt_a)
        self.Show_Loan()

    def open_return_tab(self):
        self.tabWidget.setCurrentIndex(1)
        self.buttons_choose(self.butt_a_2)


    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.buttons_choose(self.butt_a_3)
        self.Show_Copybook()
        self.Show_Book()


    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.buttons_choose(self.butt_a_4)
        self.Show_User()

    def open_other_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.buttons_choose(self.butt_a_5)
        self.Show_Publisher()
        self.Show_User()
        self.Show_Author()

    def open_theme_tab(self):
        self.tabWidget.setCurrentIndex(5)
        self.buttons_choose(self.butt_a_6)

    ###################################################################################
    #######################################THEME#######################################
    def theme_dark(self):
        self.setStyleSheet('background-color: rgb(0,0,0); color: rgb(255,255,255);')

    def theme_light(self):
        self.setStyleSheet('')

    def theme_blue(self):
        self.setStyleSheet('''
            background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, 
            stop:0 rgba(63, 66, 172, 255), stop:0.950249 rgba(238, 255, 255, 255));''')

    def theme_pink(self):
        self.setStyleSheet('''
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(255, 134, 255, 234), stop:1 rgba(255, 255, 255, 255));''')

    ###################################################################################
    #######################################SHOW########################################
    def Show_Info(self):
        db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
        cursor = db.cursor()
        cursor.execute("select * from user where email = 'admin@gmail.com'")
        result = cursor.fetchone()
        if result:
            self.label_u_5.setText(result[1])  # Hiển thị tên thủ thư
            self.label_u_6.setText(str(result[0]))  # Hiển thị ID
            self.label_u_7.setText(result[2])  # Hiển thị địa chỉ email

    def Show_Loan(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''
                            SELECT loan.ID, user.Name, book.Title, copyBook.ID, category.Name, publisher.Name, loan.Loan_date, loan.Due_date, loan.Status, loan.Fine, loan.Reason
                            FROM loan
                            JOIN user ON loan.User_ID = user.ID
                            JOIN copyBook ON loan.CopyBook_ID = copyBook.ID
                            JOIN book ON copyBook.Book_ID = book.ID
                            JOIN category ON book.Category_ID = category.ID
                            JOIN publisher ON book.Publisher_ID = publisher.ID
                            ORDER BY loan.ID DESC;
        ''')
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 8:
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

        self.db.close()

    def Show_Book(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT
                                book.Title as Book_Title,
                                book.ISBN,
                                book.Description as Book_Description,
                                category.Name as Book_Category,
                                GROUP_CONCAT(DISTINCT author.Name SEPARATOR ', ') as Book_Author,
                                publisher.Name as Book_Publisher,
                                COUNT(DISTINCT copyBook.ID) as Quantity,
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

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(self.book_data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        if self.tableWidget_5.item(self.tableWidget_5.rowCount() - 1, 0) is None:
            self.tableWidget_5.removeRow(self.tableWidget_5.rowCount() - 1)
        self.db.close()

    def Show_User(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db = '11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT 
                                user.ID, 
                                user.Name, 
                                user.Email, 
                                user.Debt, 
                                SUM(loan.Fine) AS TotalFine
                            FROM 
                                user
                                LEFT JOIN loan ON user.ID = loan.User_ID
                            WHERE 
                                user.Is_admin = 0
                            GROUP BY 
                                user.ID;
                        ''')

        self.book_data = self.cur.fetchall()  # Lưu dữ liệu vào biến instance

        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row, form in enumerate(self.book_data):
            for column, item in enumerate(form):
                self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        if self.tableWidget_6.item(self.tableWidget_6.rowCount() - 1, 0) is None:
            self.tableWidget_6.removeRow(self.tableWidget_6.rowCount() - 1)
        self.db.close()

    def Show_Category(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''
                SELECT category.Name, COUNT(DISTINCT book.ID) AS "Số lượng sách"
                FROM category
                LEFT JOIN book ON category.ID = book.Category_ID
                LEFT JOIN copyBook ON book.ID = copyBook.Book_ID
                GROUP BY category.ID
               ''')

        self.category_data = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(['Category', 'Number of book titles'])

        for row, form in enumerate(self.category_data):
            self.tableWidget_2.insertRow(row)
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))

        self.db.close()

    def Show_Publisher(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT publisher.Name, COUNT(DISTINCT book.ID) AS "Số lượng sách"
            FROM publisher
            LEFT JOIN book ON publisher.ID = book.Publisher_ID
            LEFT JOIN copyBook ON book.ID = copyBook.Book_ID
            GROUP BY publisher.ID
        ''')

        self.publisher_data = self.cur.fetchall()

        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(2)
        self.tableWidget_4.setHorizontalHeaderLabels(['Publisher', 'Number of book titles'])

        for row, form in enumerate(self.publisher_data):
            self.tableWidget_4.insertRow(row)
            for column, item in enumerate(form):
                self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))

        self.db.close()

    def Show_Author(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT author.Name, COUNT(DISTINCT book.ID) AS "Number of book titles"
            FROM author
            LEFT JOIN writing ON author.ID = writing.Author_ID
            LEFT JOIN book ON writing.Book_ID = book.ID
            GROUP BY author.ID
        ''')

        self.author_data = self.cur.fetchall()

        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(2)
        self.tableWidget_3.setHorizontalHeaderLabels(['Author', 'Number of book titles'])

        for row, form in enumerate(self.author_data):
            self.tableWidget_3.insertRow(row)
            for column, item in enumerate(form):
                self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))

        self.db.close()

    def Show_Copybook(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        self.cur.execute('''
                            SELECT
                                copyBook.ID as Copybook_ID,
                                book.Title,
                                book.ISBN,
                                CASE 
                                    WHEN copyBook.Available = 1 THEN 'Available' 
                                    ELSE 'Unavailable'
                                END AS Availability,
                                loan.ID as Loan_ID,
                                loan.User_ID,
                                user.Name
                            FROM
                                copyBook
                                JOIN book ON copyBook.Book_ID = book.ID
                                LEFT JOIN loan ON copyBook.ID = loan.CopyBook_ID AND loan.ID = (
                                    SELECT MAX(ID) FROM loan WHERE CopyBook_ID = copyBook.ID
                                )
                                LEFT JOIN user ON loan.User_ID = user.ID
                            ORDER BY
                                Copybook_ID;
                        ''')

        self.copybook_data = self.cur.fetchall()  # Lưu dữ liệu vào biến instance

        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)

        for row, form in enumerate(self.copybook_data):
            for column, item in enumerate(form):
                self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)

        if self.tableWidget_7.item(self.tableWidget_7.rowCount() - 1, 0) is None:
            self.tableWidget_7.removeRow(self.tableWidget_7.rowCount() - 1)

        self.db.close()

    ###################################################################################
    #####################################FUNCTION BOTTON###############################
    def Add_Loan_today(self):
        # Check if User_ID and Copies_ID are not empty
        user_id = self.lineEdit.text()
        copies_id = self.lineEdit_29.text()
        if not user_id or not copies_id:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter both User ID and Copies ID!")
            return

        # Connect to database
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        # Check if User exists
        self.cur.execute("SELECT ID FROM user WHERE ID=%s", (user_id,))
        user = self.cur.fetchone()
        if not user:
            QtWidgets.QMessageBox.warning(self, "User Not Found", "User with ID {} not found!".format(user_id))
            return

        # Check if Copybook_ID is valid and available
        self.cur.execute("SELECT Book_ID FROM copybook WHERE ID=%s AND Available = 1", (copies_id,))
        book_id = self.cur.fetchone()
        if not book_id:
            QtWidgets.QMessageBox.warning(self, "Copy Not Found",
                                          "CopyBook with ID {} not found or is not available!".format(copies_id))
            return

        # Get Book title for Book_Id
        self.cur.execute("SELECT Title FROM book WHERE ID=%s", (book_id[0],))
        book_title = self.cur.fetchone()[0]

        # Get loan period
        loan_period = self.comboBox_2.currentText()
        if loan_period == '1 month':
            due_date = datetime.date.today() + datetime.timedelta(days=30)
        elif loan_period == '3 months':
            due_date = datetime.date.today() + datetime.timedelta(days=90)
        else:
            return

        # Get next loan ID
        self.cur.execute("SELECT MAX(ID) FROM loan")
        result = self.cur.fetchone()[0]
        if result is None:
            loan_id = 1
        else:
            loan_id = result + 1

        # Insert new loan to loan table
        self.cur.execute("""
            INSERT INTO loan (ID, User_ID, CopyBook_ID, Loan_date, Due_date, Return_date, Status, Fine, Reason)
            VALUES (%s, %s, %s, %s, %s, %s, 0, 0.00, NULL)
        """, (loan_id, user_id, copies_id, datetime.date.today(), due_date, None))

        self.db.commit()

        # Update copybook table
        self.cur.execute("UPDATE copybook SET Available=0 WHERE ID=%s", (copies_id,))
        self.db.commit()

        # Close database connection
        self.db.close()

        # Update UI and show success message
        self.Show_Loan()
        QtWidgets.QMessageBox.information(self, "Success",
                                          f"{book_title} has been loaned to User with ID {user_id} successfully!")
        self.lineEdit.clear()
        self.lineEdit_29.clear()


    def Export_today_loan(self):
        # Connect to database and execute query
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cur = db.cursor()
        cur.execute("""
                    SELECT loan.ID, user.Name, book.Title, copyBook.ID, category.Name, publisher.Name, loan.Loan_date, loan.Due_date, loan.Status, loan.Fine, loan.Reason
                    FROM loan
                    JOIN user ON loan.User_ID = user.ID
                    JOIN copyBook ON loan.CopyBook_ID = copyBook.ID
                    JOIN book ON copyBook.Book_ID = book.ID
                    JOIN category ON book.Category_ID = category.ID
                    JOIN publisher ON book.Publisher_ID = publisher.ID
                    WHERE loan.Loan_date = %s
                    ORDER BY loan.Loan_date DESC;
        """, (datetime.date.today(),))

        # Create pandas dataframe from query result
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=["Loan ID", "User Name", "Book Title", "Copy ID", "Catagory", "Publisher", "Loan date", "Due date", "Status", "Fine", "Reason"])

        # Add new column based on "Status" column
        df["Loan Status"] = df.apply(lambda row: "Borrowing" if row["Status"] == 0 else "Returned", axis=1)

        # Drop "Status" column
        df = df.drop(columns=["Status"])

        # Export dataframe to Excel file
        filename = "today_loan_{}.xlsx".format(datetime.date.today())
        df.to_excel(filename, index=False)

        # Close database connection
        db.close()

    def Search_Loan_Book(self):
        user_id = self.lineEdit_36.text()
        self.User_Id = user_id

        if user_id == "":
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập User ID!")
        else:
            # Kiểm tra User có tồn tại không
            db = con.connect(host='localhost', user='root', password='1234', db='11-3')
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM user WHERE ID = '{user_id}'")
            result = cursor.fetchone()

            if result:
                # Kiểm tra User có phải là admin không
                if result[4] == 1:
                    QMessageBox.warning(self, "Cảnh báo", "User không tồn tại!")
                else:
                    # Hiển thị thông tin User
                    self.lineEdit_33.setText(result[2])  # Hiển thị User_email
                    self.lineEdit_36.setText(str(result[0]))  # Chuyển đổi ID sang kiểu chuỗi và hiển thị

                    # Hiển thị danh sách các sách đang mượn của User
                    cursor.execute(f'''
                                SELECT loan.ID, copybook.ID, book.Title, loan.Loan_date, loan.Due_date, loan.Return_date, loan.fine, loan.Reason, loan.Status
                                FROM loan 
                                JOIN copybook ON loan.CopyBook_ID = CopyBook.ID 
                                JOIN book ON copybook.Book_ID = book.ID 
                                WHERE loan.User_ID = '{user_id}'
                                ORDER BY loan.Status, loan.Due_date
                    ''')

                    data = cursor.fetchall()

                    self.tableWidget_10.setRowCount(0)
                    self.tableWidget_10.insertRow(0)

                    for row, form in enumerate(data):
                        for column, item in enumerate(form):
                            if column == 8:
                                if item == 0:
                                    item = "Borrowing"
                                elif item == 1:
                                    item = "Returned"
                                else:
                                    item = "Unknown"
                            self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                            column += 1

                        row_position = self.tableWidget_10.rowCount()
                        self.tableWidget_10.insertRow(row_position)

                    if self.tableWidget_10.item(self.tableWidget_10.rowCount() - 1, 0) is None:
                        self.tableWidget_10.removeRow(self.tableWidget_10.rowCount() - 1)

                    # Hiển thị thông tin số tiền phạt còn lại
                    cursor.execute(f'''SELECT SUM(fine)
                                    FROM loan
                                    JOIN copybook ON loan.CopyBook_ID = copyBook.ID
                                    JOIN user ON loan.User_ID = user.ID
                                    WHERE user.ID = '{user_id}' AND loan.Status = 0;''')
                    result = cursor.fetchone()
                    remaining_fine = result[0] if result[0] else 0
                    self.lineEdit_37.setText(str(remaining_fine))
            else:
                QMessageBox.warning(self, "Cảnh báo", "User không tồn tại!")

            db.close()

    def Change_fine_reason(self):
        loan_id = self.lineEdit_34.text()
        amount = self.lineEdit_35.text()
        reason = self.textEdit_3.toPlainText()

        # Kiểm tra loan_id có tồn tại trong bảng loan không
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()
        cursor.execute("SELECT User_ID FROM loan WHERE ID=%s", (loan_id,))
        result = cursor.fetchone()
        user_id = result[0]
        if not result:
            QMessageBox.warning(self, "Warning", "Invalid Loan ID. Please check again.")
            return

        # Kiểm tra email của user có khớp với email nhập vào hay không
        user_id = result[0]
        cursor.execute("SELECT Email FROM user WHERE ID=%s", (user_id,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "Warning", "Invalid User ID. Please check again.")
            return

        email = result[0]

        if email != self.lineEdit_33.text():
            QMessageBox.warning(self, "Warning", "Invalid Email. Please check again.")
            return

        # Xác nhận cập nhật
        reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to update the fine?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Cập nhật fine và reason vào database
            cursor.execute("UPDATE loan SET fine=%s, Reason=%s WHERE ID=%s", (amount, reason, loan_id))

            db.commit()

            # Hiển thị thông báo cập nhật thành công
            QMessageBox.information(self, "Success", "Fine has been updated successfully.")

            # Hiển thị thông tin số tiền phạt còn lại
            cursor.execute(f'''SELECT SUM(fine)
                            FROM loan
                            JOIN copybook ON loan.CopyBook_ID = copyBook.ID
                            JOIN user ON loan.User_ID = user.ID
                            WHERE user.ID = '{user_id}' AND loan.Status = 0;''')
            result = cursor.fetchone()
            remaining_fine = result[0] if result[0] else 0
            self.lineEdit_37.setText(str(remaining_fine))
            cursor.execute("UPDATE user SET Debt=%s WHERE ID=%s", (remaining_fine, user_id))
            db.commit()

            cursor.execute(f'''
                            SELECT loan.ID, copybook.ID, book.Title, loan.Loan_date, loan.Due_date, loan.Return_date, loan.fine, loan.Reason, loan.Status
                            FROM loan 
                            JOIN copybook ON loan.CopyBook_ID = CopyBook.ID 
                            JOIN book ON copybook.Book_ID = book.ID 
                            WHERE loan.User_ID = '{user_id}'
                            ORDER BY loan.Status, loan.Due_date
                            ''')
            data = cursor.fetchall()

            self.tableWidget_10.setRowCount(0)
            self.tableWidget_10.insertRow(0)

            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    if column == 8:
                        if item == 0:
                            item = "Borrowing"
                        elif item == 1:
                            item = "Returned"
                        else:
                            item = "Unknown"
                    self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_10.rowCount()
                self.tableWidget_10.insertRow(row_position)

            if self.tableWidget_10.item(self.tableWidget_10.rowCount() - 1, 0) is None:
                self.tableWidget_10.removeRow(self.tableWidget_10.rowCount() - 1)

            cursor.execute(f'''SELECT SUM(fine)
                            FROM loan
                            JOIN copybook ON loan.CopyBook_ID = copyBook.ID
                            JOIN user ON loan.User_ID = user.ID
                            WHERE user.ID = '{user_id}' AND loan.Status = 0;''')

        else:
            return

    def Pay_fine(self):
        loan_id = self.lineEdit_34.text()

        # Kiểm tra loan_id có tồn tại trong bảng loan không
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM loan WHERE ID=%s", (loan_id,))
        result = cursor.fetchone()

        if result:
            # Kiểm tra nếu sách đã được trả
            if result[6] == 1:
                QMessageBox.warning(self, "Cảnh báo", "Sách đã được trả!")
            else:
                cursor.execute("SELECT User_ID FROM loan WHERE ID=%s", (loan_id,))
                result = cursor.fetchone()
                user_id = result[0]

                # Cập nhật Status và Due_date cho loan
                today = datetime.date.today()
                cursor.execute("UPDATE loan SET Status=1, Return_date=%s WHERE ID=%s", (today, loan_id))
                cursor.execute("UPDATE copybook SET Available=1 WHERE ID=%s", (loan_id,))
                db.commit()

                QMessageBox.information(self, "Thông báo", "Cập nhật thành công!")
                cursor.execute(f'''
                                SELECT loan.ID, copybook.ID, book.Title, loan.Loan_date, loan.Due_date, loan.Return_date, loan.fine, loan.Reason, loan.Status
                                FROM loan 
                                JOIN copybook ON loan.CopyBook_ID = CopyBook.ID 
                                JOIN book ON copybook.Book_ID = book.ID 
                                WHERE loan.User_ID = '{user_id}'
                                ORDER BY loan.Status, loan.Due_date
                                ''')
                data = cursor.fetchall()

                self.tableWidget_10.setRowCount(0)
                self.tableWidget_10.insertRow(0)

                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        if column == 8:
                            if item == 0:
                                item = "Borrowing"
                            elif item == 1:
                                item = "Returned"
                            else:
                                item = "Unknown"
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1

                    row_position = self.tableWidget_10.rowCount()
                    self.tableWidget_10.insertRow(row_position)

                if self.tableWidget_10.item(self.tableWidget_10.rowCount() - 1, 0) is None:
                    self.tableWidget_10.removeRow(self.tableWidget_10.rowCount() - 1)

                # Hiển thị thông tin số tiền phạt còn lại
                cursor.execute(f'''SELECT SUM(fine)
                                FROM loan
                                JOIN copybook ON loan.CopyBook_ID = copyBook.ID
                                JOIN user ON loan.User_ID = user.ID
                                WHERE user.ID = '{user_id}' AND loan.Status = 0;''')
                result = cursor.fetchone()
                remaining_fine = result[0] if result[0] else 0
                self.lineEdit_37.setText(str(remaining_fine))
        else:
            QMessageBox.warning(self, "Cảnh báo", "Loan không tồn tại!")
        db.close()

    def Add_New_Book(self):
        # Lấy thông tin nhập vào từ giao diện
        book_title = self.lineEdit_25.text()
        book_description = self.textEdit.toPlainText()
        book_isbn = self.lineEdit_27.text()
        publication_year = self.lineEdit_4.text()

        if publication_year.isdigit():
            # Chuyển đổi giá trị book_id sang kiểu int
            publication_year = int(publication_year)
        else:
            # In ra thông báo lỗi nếu giá trị nhập vào không phải là số nguyên
            print("Publication year must be a legal number")

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        category_name = self.comboBox_9.currentText()
        cursor.execute("SELECT ID FROM category WHERE Name = %s", (category_name,))
        result = cursor.fetchone()
        category_id = result[0]

        publisher_name = self.comboBox_10.currentText()
        cursor.execute("SELECT ID FROM publisher WHERE Name = %s", (publisher_name,))
        result = cursor.fetchone()
        publisher_id = result[0]

        query = "INSERT INTO book (Title, Description, ISBN, Category_ID, Publisher_ID, Publication_year, Quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (book_title, book_description, book_isbn, category_id, publisher_id, publication_year, 0)

        # Kiểm tra các biến đầu vào
        if not all([book_title, book_description, book_isbn, publication_year, category_name, publisher_name]):
            # Hiển thị thông báo lỗi
            print("Please fill in all the required information.")

        else:
            # Kiểm tra xem sách có cùng ISBN đã tồn tại trong bảng book chưa
            cursor.execute("SELECT ID FROM book WHERE ISBN = %s", (book_isbn,))
            result = cursor.fetchone()
            if result:
                QMessageBox.warning(self, "Cảnh báo", "A book with the same ISBN already exists.!")
            else:
                # Thực hiện truy vấn INSERT vào bảng book
                cursor.execute(query, values)
                book_id = cursor.lastrowid
                # Lưu thay đổi


        # Tách tên tác giả thành các phần tử riêng biệt
        author_names = self.lineEdit_22.text().split(',')

        # Thêm thông tin tác giả vào bảng author và lấy ID của tác giả
        author_ids = []
        for author_name in author_names:
            # Kiểm tra tên tác giả đã tồn tại trong bảng author chưa
            query_author = "SELECT ID FROM author WHERE Name = %s"
            cursor.execute(query_author, (author_name,))
            result_author = cursor.fetchone()

            # Nếu tên tác giả đã tồn tại trong bảng author
            if result_author:
                author_id = result_author[0]
            # Nếu tên tác giả chưa tồn tại trong bảng author
            else:
                query_new_author = "INSERT INTO author (Name) VALUES (%s)"
                cursor.execute(query_new_author, (author_name,))
                author_id = cursor.lastrowid
            author_ids.append(author_id)

        # Thêm thông tin về tác giả và sách vào bảng writing
        cursor.execute("SELECT MAX(ID) FROM book")
        result = cursor.fetchone()
        for author_id in author_ids:
            query_writing = "INSERT INTO writing (Author_ID, Book_ID) VALUES (%s, %s)"
            cursor.execute(query_writing, (author_id, book_id))

        # Lưu các thay đổi vào database
        db.commit()
        QMessageBox.information(self, "Thông báo", "Cập nhật thành công!")

    def Add_Copybook(self):
        # Lấy danh sách các ID copybook từ ô textEdit_4
        copybook_ids = self.textEdit_4.toPlainText().strip().split(',')
        # Lấy giá trị ISBN của sách từ ô lineEdit_27
        book_isbn = self.lineEdit_27.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Kiểm tra điều kiện
        if not all([copybook_ids, book_isbn]):
            # Hiển thị thông báo lỗi
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all the required information.")
        else:
            # Kiểm tra ISBN có tồn tại trong database không
            cursor.execute("SELECT ID FROM book WHERE ISBN = %s", (book_isbn,))
            book_id = cursor.fetchone()

            if not book_id:
                QtWidgets.QMessageBox.critical(self, "Error",
                                               f"Book with ISBN {book_isbn} does not exist in the database.")
            else:
                book_id = book_id[0]
                # Kiểm tra các copybook ID đã tồn tại trong database hay chưa
                existing_copybook_ids = []
                for copybook_id in copybook_ids:
                    cursor.execute("SELECT ID FROM copyBook WHERE ID = %s", (copybook_id,))
                    result = cursor.fetchone()
                    if result:
                        existing_copybook_ids.append(result[0])

                if existing_copybook_ids:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setIcon(QtWidgets.QMessageBox.Warning)
                    message_box.setText(
                        f"The following copybook IDs already exist in the database: {', '.join(str(x) for x in existing_copybook_ids)}")
                    message_box.setInformativeText("Do you want to proceed and update these copybooks?")
                    message_box.setWindowTitle("Confirmation")
                    message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    message_box.setDefaultButton(QtWidgets.QMessageBox.No)
                    response = message_box.exec_()

                    if response == QtWidgets.QMessageBox.Yes:
                        # Cập nhật các copybook có ID bị trùng
                        for copybook_id in existing_copybook_ids:
                            cursor.execute("UPDATE copyBook SET Available = 1, Book_ID = %s WHERE ID = %s",
                                           (book_id, copybook_id))
                        db.commit()
                        # Hiển thị thông báo
                        QtWidgets.QMessageBox.information(self, "Thông báo", "Cập nhật thành công!")
                    else:
                        QtWidgets.QMessageBox.information(self, "Thông báo", "Copybooks were not updated.")
                else:
                    # Thêm các copybook mới vào database
                    for copybook_id in copybook_ids:
                        cursor.execute("INSERT INTO copyBook (ID, Book_ID, Available) VALUES (%s, %s, 1)",
                                       (copybook_id, book_id))
                        db.commit()
                    # Hiển thị thông báo
                    QtWidgets.QMessageBox.information(self, "Thông báo", "Cập nhật thành công!")

    def Search_Book(self):
        self.db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        self.cur = self.db.cursor()

        isbn = self.lineEdit_5.text()

        # Lấy thông tin sách theo ISBN
        self.cur.execute(f'''SELECT 
                                book.Title, 
                                book.Description, 
                                book.Publication_year, 
                                author.Name 
                            FROM 
                                book 
                                JOIN writing ON book.ID = writing.Book_ID 
                                JOIN author ON author.ID = writing.Author_ID 
                            WHERE 
                                book.ISBN = '{isbn}';''')
        book_data = self.cur.fetchall()

        if len(book_data) > 0:
            # Hiển thị thông tin sách lên giao diện
            self.lineEdit_8.setText(book_data[0][0])
            self.textEdit_2.setText(book_data[0][1])
            self.lineEdit_6.setText(str(book_data[0][2]))
            authors = [data[3] for data in book_data]
            self.lineEdit_23.setText(", ".join(authors))
        else:
            QMessageBox.warning(self, 'Error', 'Book not found')

        self.db.close()

    def Edit_Book(self):
        # Lấy thông tin sách
        title = self.lineEdit_8.text()
        description = self.textEdit_2.toPlainText()
        author_names = self.lineEdit_23.text()
        publication_year = self.lineEdit_6.text()
        isbn = self.lineEdit_5.text()
        category_id = self.comboBox_9.currentData()
        publisher_id = self.comboBox_10.currentData()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        try:
            # Bắt đầu transaction
            cursor.execute("START TRANSACTION")

            # Kiểm tra điều kiện
            if not all([title, description, author_names, publication_year, isbn]):
                QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all the required information.")
            else:
                # Tìm book_id của sách cần cập nhật
                cursor.execute("SELECT ID FROM book WHERE ISBN = %s", (isbn,))
                book_id = cursor.fetchone()

                if not book_id:
                    QtWidgets.QMessageBox.critical(self, "Error",
                                                   f"Book with ISBN {isbn} does not exist in the database.")
                else:
                    book_id = book_id[0]
                    # Cập nhật thông tin sách
                    cursor.execute(
                        "UPDATE book SET Title = %s, Description = %s, Publication_year = %s, ISBN = %s WHERE ID = %s",
                        (title, description, publication_year, isbn, book_id)
                    )

                    # Cập nhật tác giả của sách
                    author_names = [name.strip() for name in author_names.split(',')]
                    author_ids = []
                    for name in author_names:
                        cursor.execute("SELECT ID FROM author WHERE Name = %s", (name,))
                        result = cursor.fetchone()
                        if result:
                            author_ids.append(result[0])
                        else:
                            cursor.execute("INSERT INTO author (Name) VALUES (%s)", (name,))
                            author_ids.append(cursor.lastrowid)

                    # Xóa các tác giả cũ của sách
                    cursor.execute("DELETE FROM writing WHERE Book_ID = %s", (book_id,))

                    # Thêm các tác giả mới vào sách
                    for author_id in author_ids:
                        cursor.execute("INSERT INTO writing (Author_ID, Book_ID) VALUES (%s, %s)", (author_id, book_id))

                    # Commit transaction
                    db.commit()

                    # Hiển thị thông báo
                    QtWidgets.QMessageBox.information(self, "Thông báo", "Cập nhật thành công!")
        except Exception as e:
            # Rollback transaction
            db.rollback()

            # Hiển thị thông báo lỗi
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
        finally:
            # Đóng kết nối và giải phóng tài nguyên
            cursor.close()
            db.close()

    def Delete_Book(self):
        # Get the book's ISBN from the line edit
        isbn = self.lineEdit_5.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Check if the book exists in the database
        cursor.execute("SELECT * FROM book WHERE ISBN = %s", (isbn,))
        book = cursor.fetchone()

        if book:
            # Check if there are any loans with status 0 (borrowed) for this book
            cursor.execute(
                "SELECT * FROM loan l INNER JOIN copybook c ON l.CopyBook_ID = c.ID WHERE c.Book_ID = %s AND l.Status = 0",
                (book[0],))
            loans = cursor.fetchall()

            if loans:
                QtWidgets.QMessageBox.information(self, "Cannot delete book", "This book cannot be deleted because there are unreturned copies of it.")
            else:
                # Delete writing relations
                cursor.execute("DELETE FROM writing WHERE Book_ID = %s", (book[0],))

                # Delete all related copybooks
                cursor.execute("SELECT * FROM copybook WHERE Book_ID = %s", (book[0],))
                copybooks = cursor.fetchall()

                for copybook in copybooks:
                    cursor.execute("DELETE FROM loan WHERE CopyBook_ID = %s", (copybook[0],))
                    cursor.execute("DELETE FROM copybook WHERE ID = %s", (copybook[0],))

                # Delete the book
                cursor.execute("DELETE FROM book WHERE ID = %s", (book[0],))

                # Commit changes to the database
                db.commit()

                QtWidgets.QMessageBox.information(self,"Book deleted", "The book has been deleted from the database.")
        else:
            QtWidgets.QMessageBox.information(self,"Book not found", "No book with that ISBN was found in the database.")

    def Add_New_User(self):
        # Get user input from line edits
        name = self.lineEdit_9.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password_again = self.lineEdit_12.text()

        # Check if all required fields are filled
        if not name or not email or not password or not password_again:
            QtWidgets.QMessageBox.information(self, "Error", "Please fill in all required fields.")
            return

        # Check if passwords match
        if password != password_again:
            QtWidgets.QMessageBox.information(self, "Error", "Passwords do not match.")
            return

        # Check if email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QtWidgets.QMessageBox.information(self,"Error", "Invalid email address.")
            return

        # Confirm user addition
        confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure you want to add this user?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirm == QtWidgets.QMessageBox.No:
            return

        # Add user to the database
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO user (Name, Email, Password, Is_admin, Debt) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, password, 0, 0.00))
            db.commit()
            QtWidgets.QMessageBox.information(self,"Success", "User added to the database.")
        except Exception as e:
            QtWidgets.QMessageBox.information(self,"Error", str(e))
            db.rollback()

        # Clear line edits
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()

    def Search_User(self):
        # Get the user's ID from the line edit
        user_id = self.lineEdit_13.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT * FROM user WHERE ID = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            # Check if the user is an admin
            if user[4] == 1:
                QtWidgets.QMessageBox.information(self, "User not found", "No user with that ID was found in the database.")
            else:
                # Set the user's name, email, password, and debt in the appropriate line edits
                self.lineEdit_17.setText(user[1])
                self.lineEdit_15.setText(user[2])
                self.lineEdit_16.setText(user[3])
                self.lineEdit_14.setText(str(user[5]))
        else:
            QtWidgets.QMessageBox.information(self, "User not found", "No user with that ID was found in the database.")

    def Edit_User(self):
        # Get the user's ID, name, email, password, and password again from the line edits
        user_id = self.lineEdit_13.text()
        user_name = self.lineEdit_17.text()
        user_email = self.lineEdit_15.text()
        user_password = self.lineEdit_16.text()
        user_password_again = self.lineEdit_18.text()

        # Check if the user exists in the database
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE ID = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            # Check if the password and email match the user's password and email
            if user[2] != user_email:
                QtWidgets.QMessageBox.warning(self, "Warning", "Incorrect password or email")
            # Check if the password again matches the password
            elif user_password != user_password_again:
                QtWidgets.QMessageBox.warning(self, "Warning", "Passwords do not match")

            else:
                # Update the user's information in the database
                cursor.execute("UPDATE user SET name = %s, email = %s, password = %s WHERE ID = %s",
                               (user_name, user_email, user_password, user_id))
                db.commit()
                QtWidgets.QMessageBox.information(self,"User updated", "The user's information has been updated in the database.")

                self.lineEdit_13.clear()
                self.lineEdit_17.clear()
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
                self.lineEdit_18.clear()
                self.lineEdit_14.clear()
        else:
            QtWidgets.QMessageBox.information(self,"User not found", "No user with that ID was found in the database.")

    def Delete_User(self):
        # Get the user's ID, name, email, password, and password again from the line edits
        user_id = self.lineEdit_13.text()
        user_name = self.lineEdit_17.text()
        user_email = self.lineEdit_15.text()
        user_password = self.lineEdit_16.text()
        user_password_again = self.lineEdit_18.text()

        # Check if the user exists in the database
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE ID = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            # Check if the password and email match the user's password and email
            if user[2] != user_email:
                QtWidgets.QMessageBox.warning(self, "Warning", "Incorrect password or email")
            # Check if the password again matches the password
            elif user_password != user_password_again:
                QtWidgets.QMessageBox.warning(self, "Warning", "Passwords do not match")

            else:
                confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure you want to delete this user?",
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if confirm == QtWidgets.QMessageBox.No:
                    return

                # Update the user's information in the database
                cursor.execute("DELETE FROM user WHERE ID = %s", (user_id,))
                db.commit()
                QtWidgets.QMessageBox.information(self, "User deleted",
                                                  "User has been deleted")

                self.lineEdit_13.clear()
                self.lineEdit_17.clear()
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
                self.lineEdit_18.clear()
                self.lineEdit_14.clear()
        else:
            QtWidgets.QMessageBox.information(self, "User not found", "No user with that ID was found in the database.")

    def Add_New_Category(self):
        # Get the category name from the line edit
        category_name = self.lineEdit_19.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Check if the category already exists in the database
        cursor.execute("SELECT * FROM category WHERE Name = %s", (category_name,))
        category = cursor.fetchone()

        if category:
            # If the category already exists, show a warning message
            QtWidgets.QMessageBox.warning(self, "Category exists",
                                          "A category with that name already exists in the database.")
        else:
            # If the category doesn't exist, confirm with the user and insert it into the database
            confirm = QtWidgets.QMessageBox.question(self, "Confirm",
                                                     "Are you sure you want to add this category to the database?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if confirm == QtWidgets.QMessageBox.Yes:
                cursor.execute("INSERT INTO category (Name) VALUES (%s)", (category_name,))
                db.commit()
                QtWidgets.QMessageBox.information(self, "Category added",
                                                  "The category has been successfully added to the database.")
        self.Show_Category()

    def Add_New_Publisher(self):
        # Get the publisher name from the line edit
        publisher_name = self.lineEdit_21.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Check if the publisher already exists in the database
        cursor.execute("SELECT * FROM publisher WHERE Name = %s", (publisher_name,))
        publisher = cursor.fetchone()

        if publisher:
            # If the publisher already exists, show a warning message
            QtWidgets.QMessageBox.warning(self, "Publisher exists",
                                          "A publisher with that name already exists in the database.")
        else:
            # If the publisher doesn't exist, confirm with the user and insert it into the database
            confirm = QtWidgets.QMessageBox.question(self, "Confirm",
                                                     "Are you sure you want to add this publisher to the database?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if confirm == QtWidgets.QMessageBox.Yes:
                cursor.execute("INSERT INTO publisher (Name) VALUES (%s)", (publisher_name,))
                db.commit()
                QtWidgets.QMessageBox.information(self, "Publisher added",
                                                  "The publisher has been successfully added to the database.")
        self.Show_Publisher()

    def Search_Author_Book(self):
        # Get the author's name from the line edit
        author_name = self.lineEdit_24.text()

        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Check if the author exists in the database
        cursor.execute("SELECT * FROM author WHERE Name = %s", (author_name,))
        author = cursor.fetchone()

        if author:
            # Get the books written by the author
            cursor.execute("SELECT b.Title FROM book b INNER JOIN writing w ON b.ID = w.Book_ID WHERE w.Author_ID = %s", (author[0],))
            books = cursor.fetchall()

            if books:
                # Set the text edit to display the book titles
                book_titles = [book[0] for book in books]
                self.textEdit_5.setText("\n".join(book_titles))
            else:
                QtWidgets.QMessageBox.information(self, "No books found", "No books written by this author were found in the database.")
        else:
            QtWidgets.QMessageBox.information(self, "Author not found", "No author with that name was found in the database.")

    def Refresh_Author(self):
        db = con.connect(host='localhost', user='root', password='1234', db='11-3')
        cursor = db.cursor()

        # Get the IDs of authors with no associated books in the writing table
        cursor.execute("""
            SELECT a.ID 
            FROM author a 
            LEFT JOIN writing w ON a.ID = w.Author_ID 
            WHERE w.Author_ID IS NULL
        """)
        authors_to_delete = cursor.fetchall()

        # Prompt user to confirm deletion of authors
        confirm = QtWidgets.QMessageBox.question(self, "Confirm deletion",
                                                 f"Are you sure you want to delete {len(authors_to_delete)} author(s)?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if confirm == QtWidgets.QMessageBox.Yes:
            # Delete authors from author table
            for author in authors_to_delete:
                cursor.execute("DELETE FROM author WHERE ID = %s", (author[0],))

            # Commit changes to the database
            db.commit()

            QtWidgets.QMessageBox.information(self, "Author(s) deleted",
                                              f"{len(authors_to_delete)} author(s) have been deleted from the database.")
        else:
            QtWidgets.QMessageBox.information(self, "Deletion cancelled", "Author deletion has been cancelled.")

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()



