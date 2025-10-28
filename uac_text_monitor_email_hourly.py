import requests, smtplib, os
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# ========== 配置部分 ==========
URL = "https://www.unionathleticsclub.com/shopuac"
TARGET_TEXT = "Sold out"
SMTP_SERVER, SMTP_PORT = "smtp.gmail.com", 465

# 从环境变量读取发件邮箱信息（在 GitHub Secrets 中配置）
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASS  = os.environ.get("SENDER_PASS")

# 收件人列表（可添加多个邮箱）
RECEIVER_EMAILS = [
    "993450372@qq.com",
    "Forza.wang@foxmail.com"
]
# ========== 结束配置 ==========


def fetch_page():
    """抓取网页内容"""
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    return r.text


def send_email(subject, body):
    """发送邮件给多个收件人"""
    msg = MIMEMultipart()
    msg["From"] = Header("UAC 上新监控", "utf-8")
    msg["To"] = Header(", ".join(RECEIVER_EMAILS), "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        print(f"✅ 邮件已发送给 {', '.join(RECEIVER_EMAILS)}")
    except Exception as e:
        print("❌ 邮件发送失败：", e)


def check_once():
    """检测目标文本是否仍然存在"""
    html = fetch_page()
    page_text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    return TARGET_TEXT in page_text


def main():
    print("🔍 正在检查页面中是否仍包含提示文字...")
    if check_once():
        print("仍然显示提示语（尚未上新）")
    else:
        print("⚠️ 提示语已消失，上新可能开始！")
        subject = "【UAC】提示语消失，上新可能开始！"
        body = f"页面中已找不到提示语：\n\n『{TARGET_TEXT}』\n\n请访问：{URL}"
        send_email(subject, body)

    print("✅ 检查完成，程序退出。")


if __name__ == "__main__":
    main()
