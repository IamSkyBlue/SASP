# SASP

SASP : SASP auto saves photos<br>
Line 丟在聊天室的照片過七天就會過期不能存取，然後丟相簿又很麻煩，所以搞了個自動備份到 google drive 的機器人<br>
<br>
機器人本體在 heroku 上運行，透過 webhook 溝通<br>
<br>
app.py:主體，記得把 CHANNEL_SECRET 和 Line_bot_token 改成自己的<br>
client_secrets.json:去自己 google api 頁面下載<br>
Procfile:heroku config<br>
requirements.txt:heroku config<br>
runtime.txt:heroku config<br>
settings.yaml: PyDrive 文件 https://pythonhosted.org/PyDrive/<br>
verified_groups.txt:heroku 會自動休眠、重啟<br>
所以就把 line_group_id 和 gdrive 資料夾 id 直接存起來這樣就不用每次重啟都找半天<br>
<br>
部屬前請先在自己電腦 run 一次，他會直接開瀏覽器做 authentication，資訊會直接存到 credentials.json<br>
(我就偷懶 👍
