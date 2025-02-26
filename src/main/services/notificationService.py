import os
import json
import logging
from flask import Flask, request
from flask_socketio import SocketIO, emit
from threading import Lock
from redis import Redis
from twilio.rest import Client as TwilioClient
from smtplib import SMTP
from email.mime.text import MIMEText

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
socketio = SocketIO(app)

# Initialize Redis for message queue
redis = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)

# Twilio configuration for SMS
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'user@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'password')

# Lock for thread safety
thread_lock = Lock()

# Set up logging
logging.basicConfig(level=logging.INFO)

def send_email(to_email, subject, message):
    """Send an email notification."""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    with SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
    logging.info(f"Email sent to {to_email}")

def send_sms(to_phone, message):
    """Send an SMS notification."""
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone
    )
    logging.info(f"SMS sent to {to_phone}")

def notify_users(notification):
    """Notify users through WebSocket and other channels."""
    # Emit notification to all connected clients
    socketio.emit('notification', notification)

    # Send email if specified
    if 'email' in notification:
        send_email(notification['email'], notification['subject'], notification['message'])

    # Send SMS if specified
    if 'phone' in notification:
        send_sms(notification['phone'], notification['message'])

@app.route('/notify', methods=['POST'])
def notify():
    """Endpoint to receive notifications."""
    data = request.json
    notification = {
        'message': data.get('message'),
        'subject': data.get('subject', 'New Notification'),
        'email': data.get('email'),
        'phone': data.get('phone')
    }
    
    # Push notification to Redis for processing
    redis.rpush('notifications', json.dumps(notification))
    
    # Notify users immediately
    notify_users(notification)

    return {'status': 'success', 'message': 'Notification sent'}, 200

def background_worker():
    """Background worker to process notifications from Redis."""
    while True:
        _, notification = redis.blpop('notifications')
        notification = json.loads(notification)
        notify_users(notification)

if __name__ == '__main__':
    # Start background worker
    socketio.start_background_task(target=background_worker)
    socketio.run(app, host='0.0.0.0', port=5000)
