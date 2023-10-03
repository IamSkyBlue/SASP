# SASP

SASP : SASP auto saves photos<br>
Line 丟在聊天室的照片過七天就會過期不能存取，然後丟相簿又很麻煩，所以搞了個自動備份到 google drive 的機器人<br>

Steps:
1. 創建Line bot: https://developers.line.biz/console ,並填寫機器接收webhook的url (https://myhost.net/callback),並開放Line bot接受群組邀請

2. 把app.py中的 CHANNEL_SECRET 和 access_token 改成自己line bot的

3. client_secrets.json:去自己 google api 頁面下載:
GCP導覽列->
API和服務->
憑證->
建立憑證->
OAuth用戶端ID->
應用程式類型選電腦應用程式->
建立->
下載json->
放到資料夾中並改名為client_secrets.json

4. 第一次啟動會開啟瀏覽器取得雲端硬碟權限,並將驗證資訊存至credentials.json檔案中,同時印出雲端硬碟資料夾ID,請填入至verified_groups.txt

5. 邀請Line bot至群組,輸入!getgid,並將此group id填入至verified_groups.txt
