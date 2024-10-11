# Motion Detection and Email Notification App

## Description
This application detects motion using a webcam and sends an email notification with a captured image when motion is detected. It leverages OpenCV for video capture and image processing, and uses the `smtplib` library to send emails.

## Features
- Real-time motion detection using webcam
- Captures images of detected motion
- Sends email notifications with the captured images
- Automatically cleans up old images to save storage space

## Technologies Used
- Python
- OpenCV
- smtplib
- EmailMessage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/armanulhaq/camera-alert.git
   cd motion-detection-email
2.  Install the required packages:
   ```bash
   pip install opencv-python
   ```
3. Set up your email credentials in the script:
   ```bash
   PASSWORD = "your_email_password"
   SENDER = "your_email@gmail.com"
   RECEIVER = "recipient_email@gmail.com"
   ```
4. Run the application:
   ```bash
   python main.py
