# Refresh Supermetrics Query Automatically

<br>

## 遠端桌面網址&登入使用者：
* [**遠端桌面連結(測試用，連結無效)**](https://test.com "Remote Desktop->測試用，連結無效")
* **登入使用者：** user123@gmail.com

## 部署VM連結：
* [**VM的GCP連結(測試用，連結無效)**](https://test.com "URL of VM->測試用，連結無效")

## 第一次部署步驟： 
1. ### 首先將專案clone至VM上
	* 專案在vm的路徑: /path
	* 終端機執行: ```cd /path```
	* 終端機執行:
		* HTTP:```git clone http://github/google-sheet-auto.git```
		* SSH:```git clone ssh://github/google-sheet-auto.git```
 <br>
 
2. ### 以shell script模擬真實的使用者啟動Chrome
	* 到專案目錄: ```cd google-sheet-auto```
	* **linux環境**
		* 終端機執行：```sh init_browser.sh```
		* 瀏覽器啟動後請登入{{user}}的Google帳號，剛剛用來呼叫shell script的終端機請保留著不要關。<br><br>

	* **mac環境**
		* 終端機執行：```sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222  --args --disable-web-security --disable-site-isolation-trials```
<br>

3. ### 打開此Python爬蟲程式
    * 「新開一個」終端機執行：```python3 main_app.py```
	* **重要事項：** 打開此爬蟲程式前請先確認瀏覽器目前的分頁位置是否位於「第一個分頁」，若不是的話請切換至第一個分頁後再執行程式，否則會程式會出錯。
<br>

4. ### 設定排程自動執行
    * 終端機執行：```crontab -e```
    即可在終端機中編輯指令，達成排程自動執行程式的效果。
    也可將程式時的訊息單獨儲存在一個.log檔中。
	* **更多Crontab詳細使用方法請參考：**
	    * [**Linux 設定 crontab 例行性工作排程教學與範例**](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/ "crontab tutorial")
	    * [**Crontab 排程產生器**](https://crontab-generator.org "crontab generator")
	* Crontab排程（每小時執行一次）：
	```
	*/60 * * * * /path/google-sheet-auto/auto_run.sh >> /path/Desktop/google-sheet.log 2>&1
	```

## 重啟部署步驟
1. 連入test遠端桌面把整個chrome瀏覽器關閉，如果沒看到chrome瀏覽器就跳過這一步
2. 刪掉tabs_record.txt，刪掉的原因是上次打開分頁數量的紀錄還留著，直接跑會關掉其他分頁
``` rm /path/google-sheet-auto/app/static/tabs_record.txt ```
3. ```cd /path/google-sheet-auto ```
4. ```sh init_browser.sh```
5. ```sh auto_run.sh```
