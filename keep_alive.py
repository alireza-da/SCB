from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
  return "Bot is alive."

@app.route('/bot_name')
def show_bot_name():
  return "Social Credit Manager"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()