import sys
import platform
import time
import sys
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException

# IMPORT / GUI AND MODULES
# ///////////////////////////////////////////////////////////////
from modules import *

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Botimazon"
        description = "Botimazon APP - Automate your shopping experience"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_shop.clicked.connect(self.buttonClick)
        widgets.btn_payment.clicked.connect(self.buttonClick)
        widgets.btn_userconfig.clicked.connect(self.buttonClick)
        widgets.btn_start.clicked.connect(self.amazon_bot)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_shop":
            widgets.stackedWidget.setCurrentWidget(widgets.shop)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW PAYMENT PAGE
        if btnName == "btn_payment":
            widgets.stackedWidget.setCurrentWidget(widgets.payment) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # SHOW USER CONFIG PAGE
        if btnName == "btn_userconfig":
            widgets.stackedWidget.setCurrentWidget(widgets.userconfig) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_start":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


    def amazon_signin(self, account, password):
        driver.get("https://www.amazon.com/")
        driver.find_element_by_xpath("//*[@id='nav-link-accountList-nav-line-1']").click()
        # account = input("Enter account: ")
        # password = input("Enter password: ")
        driver.find_element_by_xpath("//input[@type='email']").send_keys(account)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(3)

        # Detect verification
        if driver.find_elements_by_xpath("//div[@class='a-section a-spacing-large']") !=0:
            print("Please verify your amazon account")
            while True:
                if driver.find_elements_by_xpath("//div[1]/div/div/div/a[@class='nav-hidden-aria  ']"):
                    print("Verification complete")
                    break
                time.sleep(1)


    def amazon_watch(self, link):
        driver.get(link)
        title = driver.find_element_by_xpath("//span[@id='productTitle']").text
        status = driver.find_element_by_xpath("//div[@id ='availability']").text.split(".")[0]
        return title, status

    def amazon_buy(self, link):
        driver.get(link)
        driver.find_element_by_xpath("//input[@id='buy-now-button']").click()
        time.sleep(5)
        try:
            driver.switch_to.frame("turbo-checkout-iframe")
            driver.find_element_by_xpath("//input[@id='turbo-checkout-pyo-button']").click()
        except NoSuchFrameException:
            print("ERROR: No payment method available on your account")
            sys.exit()
        time.sleep(10)
        order_id = driver.current_url.split("&")[3].split("=")[1]
        # order_img = driver.find_element_by_xpath("//div[@class='a-section image-panel']/div/img").get_attribute('src')
        est_delivery = driver.find_element_by_xpath("//span[@class='a-color-success a-text-bold']").text
        return order_id, est_delivery

    def ifttt_notify(self, key, order_id, title, est_delivery):
        data = {
            'value1': order_id,
            'value2': title,
            'value3': est_delivery
        }
        requests.post(f"https://maker.ifttt.com/trigger/amazon_order_status/with/key/{key}", data=data)

    def amazon_bot(self):
        link = self.lineEdit_5.text()
        account = self.lineEdit_4.text()
        password = self.lineEdit_3.text()
        key = self.lineEdit_2.text()

        global driver
        chromepath = "Others\\chromedriver.exe"
        driver = webdriver.Chrome(chromepath)
        while True:
            title, status = self.amazon_watch(link)
            #title =
            print(f'{title}: {status}')
            if status == "In Stock":
                self.amazon_signin(
                    account=account,
                    password=password
                )
                time.sleep(3)
                order_id, est_delivery = self.amazon_buy(link)
                break
        self.ifttt_notify(
            key = key,
            order_id = order_id,
            title = (title[:50] + '..') if len(title) > 75 else title,
            est_delivery = est_delivery
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
