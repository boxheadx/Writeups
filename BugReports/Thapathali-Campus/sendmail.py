import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_host = "smtp.mailtrap.io"
smtp_port = 2525
username = "e7fb3789b74a0f"
password = "5793f6823f72b0"

sender = "admin@tcioe.edu.np"
recipients = ["sajen.078bei048@tcioe.edu.np"]
subject = "test"
body = "test"


message = MIMEMultipart()
message["From"] = sender
message["To"] = ", ".join(recipients)
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(username, password)

server.sendmail(sender, recipients, message.as_string())

server.quit()


