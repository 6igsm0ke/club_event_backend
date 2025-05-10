import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Token

SENDER = "kosbayevadilet@gmail.com"
PASSWORD = "qdqh uuha hyub yyks"


def send_email_verification(user):
    token = Token.objects.create(user=user, purpose=0)
    verification_link = f"http://172.20.10.10:8000/api/v1/auth/verify/{token.pk}/"

    subject = "Email Verification"
    to_email = user.email

    text_content = f"""Hello {user.first_name or user.email},
Please verify your email by clicking the link below:
{verification_link}
Thank you!
"""
    html_content = f"""
    <html>
        <body>
            <p>Hello {user.first_name or user.email},</p>
            <p>Please verify your email by clicking the button below:</p>
            <p>
                <a href="{verification_link}" 
                   style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none;">
                   Verify Email
                </a>
            </p>
            <p>Thank you!</p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, to_email, msg.as_string())
    server.quit()

    print("📩 Verification email sent!")
    return verification_link


def send_password_reset_email(user):
    token = Token.objects.create(user=user, purpose=1)
    reset_link = f"http://172.20.10.10:8000/api/v1/auth/request_password_reset/{token.pk}/"

    subject = "Reset Your Password"
    to_email = user.email

    text_content = f"""Hello {user.first_name or user.email},
You can reset your password using the link below:
{reset_link}
If you didn’t request this, you can ignore this email.
"""
    html_content = f"""
    <html>
        <body>
            <p>Hello {user.first_name or user.email},</p>
            <p>You can reset your password by clicking the button below:</p>
            <p>
                <a href="{reset_link}" 
                   style="background-color: #e63946; color: white; padding: 10px 20px; text-decoration: none;">
                   Reset Password
                </a>
            </p>
            <p>If you didn’t request this, you can ignore this email.</p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, to_email, msg.as_string())
    server.quit()

    print("📩 Password reset email sent!")
    return reset_link


def send_event_registration_email(user, event):
    subject = "Event Registration Confirmation"
    to_email = user.email

    text_content = f"""Hello {user.first_name or user.email},
You have successfully registered for the event: {event.title}.
Date: {event.date.strftime('%Y-%m-%d')}
Location: {event.location}

If you didn’t register, please ignore this email.
"""

    html_content = f"""
    <html>
        <body>
            <p>Hello {user.first_name or user.email},</p>
            <p>You have successfully registered for the event:</p>
            <h3>{event.title}</h3>
            <p><strong>Date:</strong> {event.date.strftime('%Y-%m-%d')}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p>If you didn’t register, please ignore this email.</p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, to_email, msg.as_string())
        server.quit()
        print("📩 Event registration email sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
    