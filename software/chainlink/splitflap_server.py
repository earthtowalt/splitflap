import sys

from flask import Flask, request, render_template
from splitflap_proto import splitflap_context, ask_for_serial_port
from splitflap_proto import Splitflap

# from API import get_quote

import time

app = Flask(__name__)

with open('badwords.txt', 'r') as f:
    bad_words = [x.strip() for x in f.readlines()]

input_form = '''
<form method="post">
    <label for="user_input">Enter text:</label>
    <input type="text" id="user_input" name="user_input">
    <input type="submit" value="Submit">
</form>'''


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def index():
    user_input = None
    mean = False

    if request.method == 'POST': 
        if request.form.get('submit_button') == 'Tell me a Joke':
            print('no')
            # send_splitflap_text('no')
        else:
            user_input = request.form.get('user_input')
            if user_input in bad_words:
                mean = True
            print(user_input)
            # send_splitflap_text(user_input)
    
    return render_template('home.html', user_input=user_input, mean=mean)

# First endpoint - Root URL "/"
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        send_splitflap_text(user_input)
        return '<p>You submitted: ' + user_input + '</p>' + input_form
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
    return 'Your input: ' + input

@app.route('/reset')
def reset():
    send_splitflap_text('@')
    return ''

@app.route('/thinking')
def magic(): 
    time.sleep(5)
    for t in ('ummmmm', 'duhhhh', 'hmmmmm', '......'): 
        send_splitflap_text(t)
        time.sleep(10)

    return ""

@app.route('/jack-hot')
def magic2(): 
    time.sleep(1)
    for t in (' jack ', '  is  ', ' hot ', ' wow '): 
        send_splitflap_text(t)
        time.sleep(7)
    return ""

def send_splitflap_text(text): 
    sanitized = text[:6].lower()
    
    print('setting text: ' + sanitized)
    s.set_text(sanitized, force_movement=Splitflap.ForceMovement.ONLY_NON_BLANK)

# @app.route('/ticker/<input>')
# def ticker(input):
#     quote = get_quote(input)
#     send_splitflap_text(quote)
#     return 'Ticker: ' + input +', quote: ' + quote


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
    sys.exit(0)

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = ask_for_serial_port()
        
    with splitflap_context(port) as s:
        app.run(host='0.0.0.0', port=5000)

