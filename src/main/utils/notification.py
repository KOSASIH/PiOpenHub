import smtplib
import logging
import requests
from twilio.rest import Client
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, email_config: Dict[str, Any] = None, sms_config: Dict[str, Any] = None):
        self.email_config = email_config
        self.sms_config = sms_config

        if email_config:
            self.smtp_server = email_config.get('smtp_server')
            self.smtp_port = email_config.get('smtp_port')
            self.email_user = email_config.get('email_user')
            self.email_password = email_config.get('email_password')

        if sms_config:
            self.twilio_client = Client(sms_config['account_sid'], sms_config['auth_token'])
            self.twilio_from_number = sms_config['from_number']

    def send_email(self, to: List[str], subject: str, body: str) -> None:
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                message = f"Subject: {subject}\n\n{body}"
                server.sendmail(self.email_user, to, message)
                logger.info(f"Email sent to {to}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def send_sms(self, to: str, message: str) -> None:
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_from_number,
                to=to
            )
            logger.info(f"SMS sent to {to}")
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")

    def send_push_notification(self, device_token: str, title: str, message: str) -> None:
        # Example using Firebase Cloud Messaging (FCM)
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=YOUR_SERVER_KEY'  # Replace with your server key
        }
        payload = {
            'to': device_token,
            'notification': {
                'title': title,
                'body': message
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"Push notification sent to {device_token}")
        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")

# Example usage
if __name__ == "__main__":
    # Email configuration
    email_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'email_user': 'your_email@example.com',
        'email_password': 'your_password'
    }

    # SMS configuration
    sms_config = {
        'account_sid': 'your_twilio_account_sid',
        'auth_token': 'your_twilio_auth_token',
        'from_number': '+1234567890'
    }

    notification_service = NotificationService(email_config=email_config, sms_config=sms_config)

    # Send an email
    notification_service.send_email(
        to=['recipient@example.com'],
        subject='Test Email',
        body='This is a test email notification.'
    )

    # Send an SMS
    notification_service.send_sms(
        to='+0987654321',
        message='This is a test SMS notification.'
    )

    # Send a push notification
    notification_service.send_push_notification(
        device_token='your_device_token',
        title='Test Notification',
        message='This is a test push notification.'
    )
