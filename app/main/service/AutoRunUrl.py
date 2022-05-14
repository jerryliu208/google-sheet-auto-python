# _*_ coding: utf8 _*_

#爬蟲用ㄉ套件
from selenium import webdriver
from app.util.web_driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#爬蟲
from app.main.crawler.SupermetricsRefresh import SupermetricsQueries

#其他ㄉ套件
from pynput.keyboard import Key, Controller
import pyautogui
import time
from os.path import exists
import pathlib

class AutoRunUrl():
    
    def __init__(self, isDebug, file_url, column_name):
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities['pageLoadStrategy'] = 'normal'
        desired_capabilities['applicationCacheEnabled'] = False
        webDriver = WebDriver()
        
        self.driver = webDriver.getDriver()
        self.wait = WebDriverWait(self.driver, 60)
        self.isDebug = isDebug
        self.file_url = file_url
        self.column_name = column_name
    
    #對AutoRun表單的A行進行動作
    def AutoRun(self):
        
        
        #為防止選單(Linux的menu)干擾爬蟲執行，所以開始前先按一下Esc鍵
        pyautogui.press('esc') 

        time.sleep(2)

        # 先開一個分頁，確保瀏覽器不會消失
        pyautogui.hotkey('ctrl', 't')

        time.sleep(2)

        # 切掉第一個分頁
        pyautogui.hotkey('ctrl', '1')        

        # 先看現在活著幾個分頁
        print('now alive tabs: ' + str(len(self.driver.window_handles)))
        # 取得上次開了幾個分頁，如果是第一次執行會回傳0 #
        tabs_counter = self.getOepnTabCounter()   
        print('will close tabs: ' + str(tabs_counter))   

        # 關掉舊的tabs #
        for idx in range(0, tabs_counter):
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(2)

        time.sleep(5)
        print("after_close_tabs_number: " + str(len(self.driver.window_handles)))

        now_tabs_count = len(self.driver.window_handles)

        if now_tabs_count > 1:
            for idx in range(0,  now_tabs_count - 1):
                if len(self.driver.window_handles) == 1:
                    break
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)

        time.sleep(2)
        print("second_close_tabs_number: " + str(len(self.driver.window_handles)))

        # 回到剛剛Ctrl + T 的那頁
        first_page = self.driver.window_handles[0]
        self.driver.switch_to_window(first_page)
        self.driver.get(self.file_url)
           
        column = 1			#某行的「第幾欄」
        value = "value"		#欄位中的值，預設為value，因為當其為空字串時會跳出while迴圈
        
        #為防止某天tab被改名字，導致下方ㄉwhile進入無窮迴圈，所以先測試有沒有AutoRun這個Tab，如果沒有就直接罷工
        try: #點擊名為「AutoRun」的Tab
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(),'AutoRun')]")))
            time.sleep(3)
            autorun_tab = self.driver.find_element(By.XPATH, "//*[contains(text(),'AutoRun')]")
            autorun_tab.click()
        except Exception as e:
            print("點擊Tab AutoRun錯誤："+str(e))
            return

        #抓A行每個欄位，直到A行的某欄位為空值為止
        while value != "" :

            try: #點擊名為「AutoRun」的Tab
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(),'AutoRun')]")))
                time.sleep(3)
                autorun_tab = self.driver.find_element(By.XPATH, "//*[contains(text(),'AutoRun')]")
                autorun_tab.click()
            except Exception as e:
                # 這個會點不到大概就是沒回應了，可以直接跳掉
                print("點擊Tab AutoRun錯誤："+str(e))
                self.saveOpenTabsCounter(column - 1)
                #self.driver.refresh()
                break
                
        
            #輸入框輸入欲選取欄位之座標
            self.wait.until(EC.presence_of_all_elements_located((By.ID, 't-name-box')))
            table_name_input = self.driver.find_element(By.ID, 't-name-box')
            table_name_input.click()
            #table_name_input.send_keys(Keys.BACK_SPACE)
            table_name_input.clear()
            table_name_input.send_keys(self.column_name+str(column))	#輸入欄位座標，如：A2，即為A行第二欄
            table_name_input.send_keys(Keys.ENTER)
            
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='t-formula-bar-input']/div[1]")))
            column_value = self.driver.find_element(By.XPATH, "//div[@id='t-formula-bar-input']/div[1]").text #取得該欄位中的值
            #print("column_value = "+column_value)
            value = column_value

            if value != "": #若該欄位的值不為空
                if column == 1: #若為第一欄，則用滑鼠移動去抓取欄位中的連結（因為第一欄會放公式，所以只能用滑鼠去抓連結）
                    pyautogui.moveTo(111, 314, duration=2) #有提示訊息網頁的第一欄位置
                    pyautogui.click()
                    
                    self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='t-formula-bar-input']/div[1]")))
                    first_column_value = self.driver.find_element(By.XPATH, "//div[@id='t-formula-bar-input']/div[1]").text #取得第一欄位中的值
                    str_pos = first_column_value.find('=') #要檢查欄位值是否為公式的話，就檢查字串的第一個字是不是'='
                    
                    #如果發現欄位中的值不是公式，表示沒有點到第一欄(因為爬蟲的第一個頁面的網頁上方會有提示訊息，如果被關過的話提示訊息會不見，就會導致第一欄的位置不一樣)
                    if str_pos != 0: 
                        pyautogui.moveTo(97, 280, duration=2) #沒有提示訊息網頁的第一欄位置
                        pyautogui.click()
                        pyautogui.moveTo(100, 280, duration = 2) #點選欄位後要移動一下，彈窗才會跳出來
                        self.wait.until(EC.presence_of_all_elements_located((By.ID, 'docs-linkbubble-link-text')))
                        self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'docs-linkbubble-link-text')))
                        link_bubble = self.driver.find_element(By.ID, 'docs-linkbubble-link-text')
                    else:
                        pyautogui.moveTo(100, 314, duration=2) #點選欄位後要移動一下，彈窗才會跳出來
                        self.wait.until(EC.presence_of_all_elements_located((By.ID, 'docs-linkbubble-link-text')))
                        link_bubble = self.driver.find_element(By.ID, 'docs-linkbubble-link-text')
                        #link = link_bubble.get_attribute("href")
                        #print("url in column 1 is = "+link)
                        #url = link
                    link_bubble.click()

                else:
                    self.driver.execute_script('window.open("'+value+'")')

                page_index = column
                #以新分頁打開連結後，執行對該分頁動作的function
                SupermetricsQueries(self.driver, self.wait, self.isDebug, page_index)
                
            # 每做一次就記錄一次
            self.saveOpenTabsCounter(column)
            # 完成該分頁動作後將欄位值+1，用以對AutoRun下個欄位進行動作
            column = column + 1
            time.sleep(1)

        # 試試看這樣會不會比較少沒回應 - By Watson
        self.driver.quit()

    """
    @function_name : getOepnTabCounter
    @author        : Watson
    @created       : 2021/12/21

    @feature:
        因為分頁有可能當掉沒有回應，所以要用ctrl + w的方式關掉分頁，
        所以去取得上次開了幾個分頁，沒有檔案的話會建一個，免擔心很安全的程式

    Returns:
        int: 回傳上次開幾個分頁的數量

    """        
    def getOepnTabCounter(self):
        old_tabs_counter = 0
        record_path = 'app/static/tabs_record.txt'
        file_exists = exists(record_path)
        print('is_tabs_record_file_exist: ' + str(file_exists))

        # 第一次才會是0 #
        if file_exists == True:
            with open(record_path, 'r') as f:
                content = f.read()
                if content == '':
                    old_tabs_counter = 0
                else:
                    old_tabs_counter = int(content)
                f.close()
        else:
            pathlib.Path('app/static/').mkdir(parents=True, exist_ok=True)
            with open(record_path, 'w'): pass
            old_tabs_counter = 0

        return old_tabs_counter

    """
    @function_name : saveOpenTabsCounter
    @author        : Watson
    @created       : 2021/12/21

    @feature:
        用來保存開了幾個分頁的程式，會寫到app/static/tabs_record.txt

    Args:
        column_number (int): 開了多少分頁的數量
    Returns:
        none!

    """
    def saveOpenTabsCounter(self, column_number):
        print(column_number)
        record_path = 'app/static/tabs_record.txt'
        with open(record_path, 'w') as f:
            f.write(str(column_number))
            f.close()
            
    def run(self):
        try:
            self.AutoRun()
        except Exception as e:
            print("AutoRun()錯誤:"+str(e))