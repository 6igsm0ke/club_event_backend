import smtplib
from email.mime.text import MIMEText

sender = "kosbayevadilet@gmail.com"
password = "qdqh uuha hyub yyks"
receiver = "erasyltalgatov5@gmail.com"

msg = MIMEText("This is a test email")
msg['Subject'] = "Test"
msg['From'] = sender
msg['To'] = receiver

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()

print("✅ Email sent!")
