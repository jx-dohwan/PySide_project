import sys
import time
import datetime
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyperclip

def find(chrome, css):
    wait = WebDriverWait(chrome, 5)
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,css)))

def find_all(chrome, css):
    find(chrome,css)
    return chrome.find_elements_by_css_selector(css)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # selenium up
        chrome = webdriver.Chrome("메일뷰어/chromedriver.exe")

        # naver login
        chrome.get("https://mail.naver.com")
        input_id = find(chrome,"#id")
        input_pw = find(chrome,'#pw')
        
        pyperclip.copy("jx7789") # 네이버 아이디
        time.sleep(1)
        input_id.click()
        input_id.send_keys(Keys.CONTROL,'v')
    
        pyperclip.copy("rh74!@EH06")
        time.sleep(1)
        input_pw.click()
        input_pw.send_keys(Keys.CONTROL,'v')
        
        input_pw.send_keys("\n")

        for mail in find_all(chrome,"ol.mailList > li"):
            date = mail.find_element_by_css_selector("li.iDate").text
            now = datetime.datetime.now()
            if len(date) < 6:                
                date = f"{now.month}-{now.day} {date}"
            date = f"{now.year}-{date}"
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            site = "네이버"
            sender = mail.find_element_by_css_selector("mTitle .name a").text
            try:
                attached = mail.find_element_by_css_selector("li.file span.spr:not([title=''])").text
                attached = True
            except:
                attached = False
            print(sender)
            print(date)
        time.sleep(10)


if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())