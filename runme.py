#!/bin/env python
import argparse
from flask import Flask, request, session, render_template, redirect, url_for
import openai

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--api_key", help="OpenAI API key")
parser.add_argument("--username", help="Accepted username")
parser.add_argument("--password", help="Accepted password")
args = parser.parse_args()
if not args.api_key:
    args.api_key = input("Enter API key:")
if not args.username:
    args.username = input("Enter username:")
if not args.password:
    args.password = input("Enter password:")

# Set up OpenAI API key
openai.api_key = args.api_key

if not args.api_key:
    print("python "+__file__+" --api_key YOUR_API_KEY --username ACCEPTED_USERNAME --password ACCEPTED_PASSWORD")
    exit()

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/',  methods=['GET', 'POST'])
def root():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    print("Showing main page")
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check user credentials here
        if request.form['username'] == args.username and request.form['password'] == args.password:
            session['logged_in'] = True
            return redirect(url_for('/'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def ask():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("Recieved question!")
        # Get question from form data
        question = request.form['user_message']
        # Get IP address
        ip_address = request.remote_addr
        # Log IP address and question
        with open('logfile.txt', 'a') as f:
            f.write(f'{ip_address}: {question}\n')
        # Send question to ChatGPT and get response
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        print("Response received!");
        response
        # Extract the assistant's reply
        answer = response['choices'][0]['message']['content']
        return {'user_message': question, 'bot_message': answer}

if __name__ == '__main__':
#    app.run()
    app.run(host='0.0.0.0')
