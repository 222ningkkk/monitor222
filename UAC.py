import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import time

# ======== 配置 ========
URL = "https://www.unionathleticsclub.com/shopuac"
TARGET_TEXT = "Sold out. Look out for Dragon gear Fall 2025."

# 发件邮箱（用 Gmail）
SENDER_EMAIL = "wW993450372@gmail.com"
SENDER_PASS = "zkzfrxgeiprzwsrw"  # Gmail 应用专用密码
RECEIVER_EMAIL = "993450372@qq.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# ======== 主逻辑 ========
def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0 (compatible; UAC-monitor/1.0)"}
    r = requests.get(URL, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = Header("UAC 上新监控", "utf-8")
    msg["To"] = Header(RECEIVER_EMAIL, "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        print("✅ 邮件发送成功！")
    except Exception as e:
        print("❌ 邮件发送失败：", e)

def main():
    print("检查页面中是否仍包含提示文字...")
    html = fetch_page()
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    if TARGET_TEXT in page_text:
        print("仍然显示提示语（尚未上新）")
    else:
        print("⚠️ 提示语已消失，可能上新了！")
        subject = "【UAC】提示语消失，上新可能开始！"
        body = f"页面中已找不到提示语：\n\n『{TARGET_TEXT}』\n\n请访问：{URL}"
        send_email(subject, body)

if __name__ == "__main__":
    main()

