# Mercedes-Benz Car Inventory Monitoring

This script is designed to monitor the inventory of Mercedes-Benz cars available on the official website. It periodically checks for updates in the inventory and notifies via email if there are any changes.

## Prerequisites

Python 3.x installed on your system.
Necessary Python libraries: requests, json, smtplib, time, os, ssl, email.mime.

## Usage

To start monitoring the Mercedes-Benz car inventory, run the script main.py. You can execute the script by running python main.py.

## Features

Initial Inventory Check: Upon running the script, it fetches the available cars for the first time and stores the data in the oldCars.txt file.
Periodic Checking: The script continuously monitors the inventory, checking for updates every 5 minutes.
Notification: If there are any changes in the inventory, it sends an email notification with the updated inventory details.
Attachment: The email notification includes an attachment (oldCars.txt) containing the previous inventory details for comparison.
