import sys
import time
import threading
import requests
from PyQt5 import QtGui
from os import environ
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import Qt
import pyttsx3
from PyQt5.Qt import *
from UdemyUi import *
import udemy_res



in_url = "https://app.real.discount"

category = ['teaching-academics', 'development', 'it-software',
            'marketing', 'finance-accounting', 'office-productivity', 'business', 'design', 'personal-development', 'health-fitness', 'photography-video', 'lifestyle', 'music', 'home-sub_categoryprovements', 'electronic', 'lifestyle-home', 'computers', 'health-household']
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButtonSignUp.clicked.connect(self.seleThread)
        self.ui.pushButtonFilter.clicked.connect(self.filterThread)
        self.ui.listWidgetCategory.itemClicked.connect(self.listsThread)
        self.ui.pushButtonEnroll.clicked.connect(self.enrollThread)
        self.ui.spinBox.setValue(1)
        self.ui.doubleSpinBox.setValue(10.00)

    def seleThread(self):
        t = threading.Thread(target=self.signUp)
        t.start()

#     def signUp(self):
#         try:
#             if len(self.ui.lineEditFullName.text()) == 0 or len(self.ui.lineEditEmail.text()) == 0 or len(self.ui.lineEditPassword.text()) == 0:
#                 speak("please enter all fields")
#                 self.ui.labelWarning.setText("please enter all fields")
#                 time.sleep(5)
#                 self.ui.labelWarning.clear()

#             else:
#                 # self.ui.labelWarning.clear()
#                 speak("trying to create udemy account")

#                 self.ui.labelWarning.setText("Creating udemy account.....")
#                 chrome_options = Options()
#                 chrome_options.add_argument("--headless")
#                 try:
#                     pass
#                     # driver = webdriver.Chrome(
#                 #     # executable_path=f"C:\\Program Files (x86)\\UdemyCoursesEnroller\\chromedriver.exe", chrome_options=chrome_options)
#                 # except:
#                 #     speak("Check your chrome version or contact software publisher")
#                 # self.ui.labelWarning.setText("You can contact software publisher")


#                 # driver.get(
#                 #     "https://www.udemy.com/join/signup-popup/?locale=en_US&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")
#                 # try:
                

#                 #     driver.find_element_by_name("fullname").send_keys(
#                         self.ui.lineEditFullName.text())
#                     driver.find_element_by_name("email").send_keys(
#                         self.ui.lineEditEmail.text())
#                     driver.find_element_by_name("password").send_keys(
#                         self.ui.lineEditPassword.text())
#                     driver.find_element_by_id("submit-id-submit").click()
#                     driver.find_element_by_link_text("Skip for now").click()
#                     speak("successfully created your udemy account")
#                     self.ui.labelWarning.setText("\nsuccessfully created your udemy account")
#                     time.sleep(5)
#                     self.ui.labelWarning.clear()
#                     driver.close()
#                 except:
#                     speak("Failed to create udemy account")
#                     self.ui.labelWarning.setText("Failed to create udemy account")
#                     time.sleep(5)
#                     self.ui.labelWarning.clear()
#                     driver.close()
#         except:
#             speak("Check your chrome version")
    def filterThread(self):
        th = threading.Thread(target=self.main)
        th.start()

    def main(self):
        try:

            self.ui.labelMsg.clear()
            # speak("now processing started..")
            pages = self.ui.spinBox.value()
            pages = self.ui.spinBox.value()
            n = 1

            for i in range(pages):
                self.ui.labelMsg.setText(f"Processing page {n}")
                n += 1
                url = f"https://app.real.discount/filter/?category={self.ui.comboBoxCategory.currentText()}&store={self.ui.comboBoxStore.currentText()}&duration={self.ui.comboBoxDuration.currentText()}&price={self.ui.comboBoxPrice.currentText()}&rating={self.ui.comboBoxRating.currentText()}&language={self.ui.comboBoxLanguage.currentText()}&search={self.ui.lineEditKeyword.text()}&submit=Filter&page={i+1}"
                if "Category" in url or " & " in url or "Store" in url or "Duration" in url or "Price" in url or "Rating" in url or "Language" in url:
                    url = url.replace("Category", "All")
                    url = url.replace(" & ", "+%26+")
                    url = url.replace("Store", "All")
                    url = url.replace("Duration", "All")
                    url = url.replace(" Price $", "All")
                    url = url.replace("Rating", "All")
                    url = url.replace("Language", "All")

                url = requests.get(url)
                soup = BeautifulSoup(url.text, "html.parser")

                links = soup.select('.col-sm-12.col-md-6.col-lg-4.col-xl-4')
                for link in links:
                    link = link.find('a')
                    link = link.attrs["href"]

                    url_n = requests.get(in_url + "/" + link)
                    soup_new = BeautifulSoup(url_n.text, "html.parser")
                    xlink = soup_new.select(
                        ".col-lg-7.col-md-12.col-sm-12.col-xs-12")
                    for x in xlink:
                        x = x.findAll("a")[1]
                        x = x.attrs["href"]
                    webbrowser.open(x)

                    # print(x)
                    time.sleep(self.ui.doubleSpinBox.value())
            speak(f"Successfully scraped {pages} pages")
            
            self.ui.labelMsg.setText(f"Successfully scraped {pages} page(s)")

        except Exception as e:
            print(e)

    def listsThread(self):
        thd = threading.Thread(target=self.lists)
        thd.start()

    def lists(self):
        self.ui.listWidgetSubCategory.clear()
        urlx = requests.get(
            f"https://app.real.discount/category/{self.ui.listWidgetCategory.currentItem().text()}")

        soupx = BeautifulSoup(urlx.text, "html.parser")
        title = soupx.select(".col-xl-3.col-md-4")
        sub_category = ''
        for i in title:
            i = i.findAll("a")[0]
            i = i.attrs["href"]
            i = str(i)
            sub_category = sub_category+i

        sub_category = sub_category[1:]
        if "//" in sub_category:
            sub_category = sub_category.replace("//", "/")
        sub_category = sub_category.split("/")
        for items in sub_category:
            if items in sub_category:
                sub_category.remove(items)
        for i in range(len(sub_category)):
            self.ui.listWidgetSubCategory.addItem(sub_category[i])

    def enrollThread(self):
        then = threading.Thread(target=self.enroll)
        then.start()

    def enroll(self):

        try:
            speak("now processing started..")
            self.ui.labelMsg.clear()
            pages = self.ui.spinBox.value()
            pages = self.ui.spinBox.value()
            n = 1

            for i in range(pages):
                self.ui.labelMsg.setText(f"Processing page {n}")
                n += 1
                url = requests.get(
                    f"https://app.real.discount/subcategory/{self.ui.listWidgetSubCategory.currentItem().text()}/?pages={i+1}")
                soup = BeautifulSoup(url.text, "html.parser")
                links = soup.select('.col-xl-4.col-md-6')
                for link in links:
                    link = link.find('a')
                    link = link.attrs["href"]
                    url_n = requests.get(in_url + "/" + link)
                    soup_new = BeautifulSoup(url_n.text, "html.parser")
                    xlink = soup_new.select(
                        ".col-lg-7.col-md-12.col-sm-12.col-xs-12")
                    for x in xlink:
                        x = x.findAll("a")[1]
                        x = x.attrs["href"]
                    webbrowser.open(x)
                    time.sleep(self.ui.doubleSpinBox.value())
            speak(f"Successfully scraped {pages} page(s)")
            self.ui.labelMsg.setText(f"Successfully scraped {pages} pages")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
