# Motion Detection Email Notifier

## Description
This project is a motion detection application that uses a webcam to monitor for movement. When motion is detected, the application captures an image and sends it via email to a specified recipient. The application is built using OpenCV for image processing and the smtplib library for email functionality. Captured images are stored temporarily in an "images" folder, which is cleaned up after sending the email.

## Features
- Real-time motion detection using a webcam
- Captures and saves images when motion is detected
- Sends captured images via email
- Automatically cleans up stored images after sending

## Requirements
- Python 3.x
- OpenCV
- imghdr
- smtplib

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/armanulhaq/camera-alert
   cd camera-alert
