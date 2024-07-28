from flask import Flask, request
from splitflap_proto import splitflap_context
from splitflap_proto import Splitflap

from API import get_quote

import time

app = Flask(__name__)

input_form = '''
        <form method="post">
            <label for="user_input">Enter text:</label>
            <input type="text" id="user_input" name="user_input">
            <input type="submit" value="Submit">
        </form>
    '''


# First endpoint - Root URL "/"
@app.route('/update/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        send_splitflap_text(user_input)
        return f'<p>You submitted: {user_input}</p>' + input_form
    return input_form

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/apple-touch*')
def apple_touch(): 
    return ''

# Second endpoint - "/<input>"
@app.route('/update/<input>')
def display_input(input):
    send_splitflap_text(input)
    return f'Your input: {input}'

@app.route('/reset')
def reset():
    send_splitflap_text('@')
    return ''

@app.route('/magic')
def magic(): 
    time.sleep(5)
    for t in ('ummmmm', 'duhhhh', 'hmmmmm', '......'): 
        send_splitflap_text(t)
        time.sleep(10)

    return ""

@app.route('/you-magic')
def magic2(): 
    time.sleep(1)
    for t in (' jack ', '  is  ', ' hot ', ' wow '): 
        send_splitflap_text(t)
        time.sleep(7)
    return ""

def send_splitflap_text(text): 
    # Show a random word every 10 seconds
    sanitized = text[:6].lower()

    print(f'setting text: {sanitized}')
    s.set_text(sanitized, force_movement=Splitflap.ForceMovement.ONLY_NON_BLANK)

@app.route('/ticker/<input>')
def ticker(input):
    quote = get_quote(input)
    send_splitflap_text(quote)
    return f'Ticker: {input}, quote: {quote}'


if __name__ == '__main__':
    with splitflap_context('ttyAMA0') as s:
        app.run(host='192.168.1.68', port=5000)

