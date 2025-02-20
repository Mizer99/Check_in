import telebot
import os
import pandas as pd
import schedule
import time
from datetime import datetime

TOKEN = os.getenv(8033825348:AAGLwwfuLpGrMOVxNJ-MajMdnVXmLKoPGek)  # Use environment variable for security
bot = telebot.TeleBot(TOKEN)

data = []  # List to store records

@bot.message_handler(commands=['work_on', 'off', 'wc', 'food_break', 'smoke', 'other', 'back'])
def track_activity(message):
    user = message.from_user
    command = message.text[1:]  # Remove "/"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data.append({"User ID": user.id, "Username": user.username, "Action": command, "Time": timestamp})
    
    bot.reply_to(message, f"✅ {command} recorded at {timestamp}")

# Function to generate and send the daily Excel report
def send_daily_report():
    if not data:
        return

    df = pd.DataFrame(data)
    file_name = "daily_report.xlsx"
    df.to_excel(file_name, index=False)

    with open(file_name, "rb") as file:
        bot.send_document(USER_ID, file, caption="📊 Daily Work Report")

    data.clear()  # Reset after sending

# Schedule the report at UTC+5:30
schedule.every().day.at("00:00").do(send_daily_report)

# Run the schedule in a background thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

import threading
threading.Thread(target=run_schedule).start()

bot.polling()
