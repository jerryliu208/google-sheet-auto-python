# _*_ coding: utf8 _*_

#Service
from app.main.service.AutoRunUrl import AutoRunUrl

#其他ㄉ套件
import time
def main():
	isDebug = True
	#正式的google sheet
	file_url = 'https://test_url.com'	
	
	#對AutoRun表單的A行進行動作
	auto_run = AutoRunUrl(isDebug, file_url, 'A')	#A行
	auto_run.run()
 
	#停留2000秒
	#time.sleep(2000)
 
if __name__ == "__main__":
	main()
