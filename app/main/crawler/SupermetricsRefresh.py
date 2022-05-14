# _*_ coding: utf8 _*_

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta

from threading import Thread
import pyautogui
import time

isRefresh = False

#打開AutoRun中連結後要執行的function
def SupermetricsQueries(driver, wait, isDebug, page_index):
	#切換到在AutoRun打開的新分頁
	driver.switch_to.window(driver.window_handles[page_index])

	try: #點擊名為「SupermetricsQueries」的Tab
		wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(),'SupermetricsQueries')]")))
		time.sleep(3)
		supermetrics_tab = driver.find_element(By.XPATH, "//*[contains(text(),'SupermetricsQueries')]")
		supermetrics_tab.click()
	except Exception as e:
		print("點擊Tab SupermetricsQueries錯誤："+str(e))
		print("點擊Tab SupermetricsQueries錯誤_alive_tabs" + str(len(driver.window_handles)))
		#supermetrics_driver.close()
		driver.switch_to.window(driver.window_handles[0])
		return
 
	#輸入框輸入欲選取欄位之座標
	wait.until(EC.presence_of_all_elements_located((By.ID, 't-name-box')))
	table_name_input = driver.find_element(By.ID, 't-name-box')
	table_name_input.click()
	time.sleep(2)
	#table_name_input.send_keys(Keys.BACK_SPACE)
	table_name_input.clear()
	table_name_input.send_keys('H'+str(21))	#輸入欄位座標，如：A2，即為A行第二欄
	table_name_input.send_keys(Keys.ENTER)

	#取得H21欄位(上次更新時間)的值，用來偵測上次更新時間是否大於30分鐘前
	wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='t-formula-bar-input']/div[1]")))
	column_value = driver.find_element(By.XPATH, "//div[@id='t-formula-bar-input']/div[1]").text #取得該欄位中的值
	date_time_str = column_value #取得日期時間字串
	try:
		datetime_object = str_to_datetime(date_time_str) #將其轉換為datetime物件
	except Exception as e:
		print("轉換時間錯誤："+str(e))
		driver.switch_to.window(driver.window_handles[0])
		return
	time_diff = datetime.now() - datetime_object #現在時間與表格中的時間差多少
	max_diff = timedelta(minutes=30)
 
	if time_diff > max_diff or isDebug: #如果上次更新時間為30分鐘前，就點擊外掛程式的按鈕更新
		#點選外掛程式按鈕
		wait.until(EC.presence_of_all_elements_located((By.ID, 'docs-extensions-menu')))
		button = driver.find_element(By.ID, 'docs-extensions-menu')
		time.sleep(5)
		button.click()
  
		#for debug mode
		"""
		time.sleep(10)
		print("supermetrics = " + str(pyautogui.position()))
		pyautogui.click(pyautogui.position())
		time.sleep(10)
		print("refresh all = " + str(pyautogui.position()))
		pyautogui.click(pyautogui.position())
		"""
		#for real mode
		pyautogui.moveTo(524, 385, duration=2)
		pyautogui.click() #點擊Supermetrics
		pyautogui.moveTo(830, 385, duration=2)
		pyautogui.moveTo(830, 455, duration=2)
		pyautogui.click() #點擊Refresh all
  
		#點擊外掛程式的更新鈕後會跳出一個顯示更新進度的彈窗，偵測到彈窗消失後代表更新已完成，完成就關閉這個分頁，繼續接下來的動作
		try:
			wait_modal = WebDriverWait(driver, 30) #偵測refresh all的彈窗有沒有跳出來，30秒就夠了。
			wait_modal.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='modal-dialog docs-dialog script-app-dialog']"))) #先等彈窗跳出來
			wait_modal_disappeared = WebDriverWait(driver, 1800) #因為彈窗更新要等比較久，所以新建一個等待器，用來等彈窗消失的
			"""
			wait_modal_disappeared.until(EC.invisibility_of_element((By.XPATH, "//div[@class='modal-dialog docs-dialog script-app-dialog']"))) #然後等彈窗消失
			#print("彈窗已消失...")
			supermetrics_driver.close()
			"""
			t = Thread(target=wait_for_refresh_modal_disappeared, args=(wait_modal_disappeared, driver))
			t.start()
		except Exception as e:
			global isRefresh
			if isRefresh == True: 
				isRefresh = False
				driver.switch_to.window(driver.window_handles[0])
				return
			else:
				print("錯誤 = "+str(e))
				driver.refresh()
				isRefresh = True
				refresh_supermetrics_queries(driver, wait, isDebug, page_index)
			
	else:
		#supermetrics_driver.close()
		pass

	#切換回去AutoRun那頁
	driver.switch_to.window(driver.window_handles[0])
 
def wait_for_refresh_modal_disappeared(wait, driver):
	wait.until(EC.invisibility_of_element((By.XPATH, "//div[@class='modal-dialog docs-dialog script-app-dialog']"))) #然後等彈窗消失
	#print("彈窗已消失...")
	#driver.close()

def str_to_datetime(date_time_str):
    #取得時間的字串格式應為「2000/10/10 下午 08:10:30」或「2000-10-10 20:10:30」，要把它轉成時間物件才能比大小
	date_time_arr = date_time_str.split(' ') #先用空白把「日期」、「上下午」、「時間」分開
 
	#因為有某個google sheet裡面的時間格式跟大家不一樣= ="，陣列會少一個index，所以弄一個try catch
	try: 
		time_arr = date_time_arr[2].split(':') #時間用":"把時、分、秒分開
		if (date_time_arr[1] == "下午" or date_time_arr[1] == "PM") and time_arr[0] != "12": #如果是下午1點過後就把小時+12
			time_arr[0] = str(int(time_arr[0]) + 12)
	except: 
		time_arr = date_time_arr[1].split(':')#陣列少一個index的話就是24小時制的，就不用+12了，直接把時、分、秒分開就好
  
	time_str = time_arr[0]+':'+time_arr[1]+':'+time_arr[2] #轉換、計算好後再把時間都組起來
	date_str = date_time_arr[0] #日期不用轉換，拿到的字串可直接用
	datetime_str = date_str+' '+time_str #最後組成一個要轉成時間物件的字串
 
	#同樣是因為有某個google sheet裡面的時間格式跟大家不一樣= ="，字串會不符合格式，所以弄一個try catch
	try: 
		datetime_object = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
	except:
 		datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
   
	return datetime_object
 

def refresh_supermetrics_queries(driver, wait, isDebug, page_index):
	SupermetricsQueries(driver, wait, isDebug, page_index)