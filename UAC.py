import requests, smtplib, time, os
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

URL = "https://www.unionathleticsclub.com/shopuac"
TARGET_TEXT = "Sold out. Look out for Dragon gear Fall 2025."
SMTP_SERVER, SMTP_PORT = "smtp.gmail.com", 465

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASS  = os.environ.get("SENDER_PASS")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

CHECK_INTERVAL = 3600  # 每小时检测一次

def fetch_page():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    return r.text

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = Header("UAC 上新监控", "utf-8")
    msg["To"] = Header(RECEIVER_EMAIL, "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
    print("✅ 邮件发送成功！")

def check_once():
    html = fetch_page()
    page_text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    return TARGET_TEXT in page_text

def main():
    print("🔍 启动 UAC 持续监控（每小时运行）...")
    notified = False
    while True:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 检查中...")
        if check_once():
            print("仍然显示提示语（尚未上新）")
        else:
            print("⚠️ 提示语已消失，上新可能开始！")
            if not notified:
                send_email("【UAC】提示语消失，上新可能开始！",
                           f"页面中已找不到提示语：\n\n『{TARGET_TEXT}』\n\n请访问：{URL}")
                notified = True
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
