# _*_ coding: utf8 _*_
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path

######### 使用方法 #########
# /**
#  *
#  * 程式說明: 
#  *
#  * 請先用init_browser.sh建立一個有登入過的瀏覽器，這樣才有登入的cookie。
#  * 
# */ 

class WebDriver():

	def __init__(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
		driver = webdriver.Chrome(chrome_options=chrome_options)
		wait = WebDriverWait(driver, 300)

		self.__driver = driver
		self.__wait = wait

	def getDriver(self):
		# driver
		return self.__driver

	def getWait(self):
		# wait for some element appear
		return self.__wait
