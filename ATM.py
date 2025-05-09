import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QStackedWidget, QFormLayout
)
from PyQt6.QtCore import Qt


class AppData:
    def __init__(self):
        self.language = "fa"
        self.password = "1234"
        self.balance = 100000


class LanguagePage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        self.init_ui()

    def init_ui(self):
        label = QLabel("لطفاً زبان خود را انتخاب کنید")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_fa = QPushButton("فارسی")
        btn_en = QPushButton("English")
        btn_fa.setFixedSize(80, 40)
        btn_en.setFixedSize(80, 40)

        btn_fa.clicked.connect(lambda: self.select("fa"))
        btn_en.clicked.connect(lambda: self.select("en"))

        h = QHBoxLayout()
        h.addWidget(btn_fa, alignment=Qt.AlignmentFlag.AlignLeft)
        h.addStretch()
        h.addWidget(btn_en, alignment=Qt.AlignmentFlag.AlignRight)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(label)
        layout.addLayout(h)
        layout.addStretch()

        self.setLayout(layout)

    def select(self, lang):
        self.data.language = lang
        self.stack.setCurrentIndex(1)


class LoginPage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        self.init_ui()

    def init_ui(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.error = QLabel()
        self.error.setStyleSheet("color: red")
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error.hide()

        self.button = QPushButton()
        self.button.setFixedSize(100, 35)
        self.button.clicked.connect(self.check_password)

        v = QVBoxLayout()
        v.addStretch()
        v.addWidget(self.label)
        v.addWidget(self.input)
        v.addWidget(self.error)
        v.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        v.addStretch()
        self.setLayout(v)

    def showEvent(self, _):
        if self.data.language == "fa":
            self.label.setText("رمز عبور را وارد کنید:")
            self.button.setText("ورود")
        else:
            self.label.setText("Enter your password:")
            self.button.setText("Login")
        self.error.hide()
        self.input.clear()

    def check_password(self):
        if self.input.text() == self.data.password:
            self.stack.setCurrentIndex(2)
        else:
            msg = "رمز اشتباه است!" if self.data.language == "fa" else "Incorrect password!"
            self.error.setText(msg)
            self.error.show()


class MainMenuPage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        self.init_ui()

    def init_ui(self):
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 16px;")

        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        self.btn3 = QPushButton()
        self.btn4 = QPushButton()

        for btn in [self.btn1, self.btn2, self.btn3, self.btn4]:
            btn.setFixedSize(100, 35)

        self.btn1.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn2.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.btn3.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        self.btn4.clicked.connect(lambda: self.stack.setCurrentIndex(6))

        row1 = QHBoxLayout()
        row1.addWidget(self.btn1, alignment=Qt.AlignmentFlag.AlignLeft)
        row1.addStretch()
        row1.addWidget(self.btn2, alignment=Qt.AlignmentFlag.AlignRight)

        row2 = QHBoxLayout()
        row2.addWidget(self.btn3, alignment=Qt.AlignmentFlag.AlignLeft)
        row2.addStretch()
        row2.addWidget(self.btn4, alignment=Qt.AlignmentFlag.AlignRight)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addLayout(row1)
        layout.addLayout(row2)
        self.setLayout(layout)

    def showEvent(self, _):
        if self.data.language == "fa":
            self.title.setText("منوی اصلی")
            self.btn1.setText("موجودی")
            self.btn2.setText("کارت به کارت")
            self.btn3.setText("برداشت وجه")
            self.btn4.setText("تغییر رمز")
        else:
            self.title.setText("Main Menu")
            self.btn1.setText("Balance")
            self.btn2.setText("Transfer")
            self.btn3.setText("Withdraw")
            self.btn4.setText("Change PIN")


class BalancePage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_btn = QPushButton()
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def showEvent(self, _):
        text = f"موجودی شما: {self.data.balance:,} تومان" if self.data.language == "fa" else f"Your balance is: {self.data.balance:,} Toman"
        self.label.setText(text)
        self.back_btn.setText("بازگشت" if self.data.language == "fa" else "Back")


class TransferPage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        
        self.card_label = QLabel()
        self.amount_label = QLabel()
        self.card_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.result = QLabel()
        self.result.setStyleSheet("color: green")
        
        self.transfer_btn = QPushButton()
        self.back_btn = QPushButton()
        
        self.transfer_btn.clicked.connect(self.transfer)
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        
        layout = QVBoxLayout()
        layout.addWidget(self.card_label)
        layout.addWidget(self.card_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.transfer_btn)
        layout.addWidget(self.back_btn)
        layout.addWidget(self.result)
        self.setLayout(layout)

    def showEvent(self, _):
        if self.data.language == "fa":
            self.card_label.setText("شماره کارت مقصد:")
            self.amount_label.setText("مبلغ انتقال:")
            self.transfer_btn.setText("انتقال")
            self.back_btn.setText("بازگشت")
        else:
            self.card_label.setText("Destination card number:")
            self.amount_label.setText("Amount:")
            self.transfer_btn.setText("Transfer")
            self.back_btn.setText("Back")
        self.card_input.clear()
        self.amount_input.clear()
        self.result.clear()

    def transfer(self):
        try:
            amount = int(self.amount_input.text())
            if amount <= self.data.balance:
                self.data.balance -= amount
                self.result.setText("انتقال انجام شد" if self.data.language == "fa" else "Transfer complete")
            else:
                self.result.setText("موجودی کافی نیست" if self.data.language == "fa" else "Insufficient funds")
        except ValueError:
            self.result.setText("مبلغ نامعتبر" if self.data.language == "fa" else "Invalid amount")


class WithdrawPage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        self.init_ui()

    def init_ui(self):
        self.amount_label = QLabel()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("مبلغ دلخواه را وارد کنید" if self.data.language == "fa" else "Enter custom amount")
        self.result = QLabel()
        self.result.setStyleSheet("color: green")

        # دکمه‌های مبلغ از پیش تعیین شده
        self.btn_50k = QPushButton("50,000")
        self.btn_100k = QPushButton("100,000")
        self.btn_150k = QPushButton("150,000")
        self.btn_200k = QPushButton("200,000")
        self.btn_custom = QPushButton("مبلغ دلخواه" if self.data.language == "fa" else "Custom Amount")

        # تنظیم اندازه دکمه‌ها
        for btn in [self.btn_50k, self.btn_100k, self.btn_150k, self.btn_200k, self.btn_custom]:
            btn.setFixedSize(100, 40)

        # اتصال دکمه‌ها به توابع مربوطه
        self.btn_50k.clicked.connect(lambda: self.withdraw(50000))
        self.btn_100k.clicked.connect(lambda: self.withdraw(100000))
        self.btn_150k.clicked.connect(lambda: self.withdraw(150000))
        self.btn_200k.clicked.connect(lambda: self.withdraw(200000))
        self.btn_custom.clicked.connect(self.custom_withdraw)

        # دکمه بازگشت
        self.back_btn = QPushButton()
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # چیدمان افقی برای دکمه‌ها
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.btn_50k)
        hbox1.addWidget(self.btn_100k)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.btn_150k)
        hbox2.addWidget(self.btn_200k)

        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(self.btn_custom)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.result)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def showEvent(self, _):
        if self.data.language == "fa":
            self.amount_label.setText("مبلغ مورد نظر را انتخاب کنید:")
            self.back_btn.setText("بازگشت")
        else:
            self.amount_label.setText("Select an amount:")
            self.back_btn.setText("Back")
        self.amount_input.clear()
        self.result.clear()

    def withdraw(self, amount):
        if amount <= self.data.balance:
            self.data.balance -= amount
            msg = f"برداشت موفق: {amount:,} تومان" if self.data.language == "fa" else f"Withdrawn: {amount:,} Toman"
            self.result.setText(msg)
        else:
            msg = "موجودی کافی نیست!" if self.data.language == "fa" else "Insufficient balance!"
            self.result.setText(msg)

    def custom_withdraw(self):
        try:
            amount = int(self.amount_input.text())
            self.withdraw(amount)
        except ValueError:
            msg = "لطفاً یک عدد وارد کنید!" if self.data.language == "fa" else "Please enter a valid number!"
            self.result.setText(msg)


class ChangePINPage(QWidget):
    def __init__(self, stack, data):
        super().__init__()
        self.stack = stack
        self.data = data
        
        self.pin_label = QLabel()
        self.new_pin = QLineEdit()
        self.result = QLabel()
        
        self.change_btn = QPushButton()
        self.back_btn = QPushButton()
        
        self.change_btn.clicked.connect(self.change_pin)
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        
        layout = QVBoxLayout()
        layout.addWidget(self.pin_label)
        layout.addWidget(self.new_pin)
        layout.addWidget(self.change_btn)
        layout.addWidget(self.back_btn)
        layout.addWidget(self.result)
        self.setLayout(layout)

    def showEvent(self, _):
        if self.data.language == "fa":
            self.pin_label.setText("رمز جدید را وارد کنید:")
            self.change_btn.setText("تغییر رمز")
            self.back_btn.setText("بازگشت")
        else:
            self.pin_label.setText("Enter new passcode:")
            self.change_btn.setText("Change PIN")
            self.back_btn.setText("Back")
        self.new_pin.clear()
        self.result.clear()

    def change_pin(self):
        pin = self.new_pin.text()
        if len(pin) >= 4:
            self.data.password = pin
            self.result.setText("رمز تغییر کرد" if self.data.language == "fa" else "PIN changed")
        else:
            self.result.setText("رمز باید حداقل ۴ رقم باشد" if self.data.language == "fa" else "PIN must be at least 4 digits")


class ATMApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.data = AppData()
        self.stack = QStackedWidget()

        self.stack.addWidget(LanguagePage(self.stack, self.data))    # index 0
        self.stack.addWidget(LoginPage(self.stack, self.data))       # index 1
        self.stack.addWidget(MainMenuPage(self.stack, self.data))    # index 2
        self.stack.addWidget(BalancePage(self.stack, self.data))     # index 3
        self.stack.addWidget(TransferPage(self.stack, self.data))    # index 4
        self.stack.addWidget(WithdrawPage(self.stack, self.data))    # index 5
        self.stack.addWidget(ChangePINPage(self.stack, self.data))   # index 6

        self.stack.setWindowTitle("ATM")
        self.stack.resize(400, 300)
        self.stack.setCurrentIndex(0)
        self.stack.show()


if __name__ == "__main__":
    app = ATMApp(sys.argv)
    sys.exit(app.exec())