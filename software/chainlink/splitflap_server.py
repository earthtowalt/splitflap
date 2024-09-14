import sys
from pathlib import Path

from flask import Flask, request, render_template, redirect
from splitflap_proto import splitflap_context, ask_for_serial_port
from splitflap_proto import Splitflap

# from API import get_quote

import random
import time


NO_FLAPPY = False

punishment_links = ['https://www.istockphoto.com/photo/middle-finger-gm140472118-3415406']

with open (Path(__file__).parent / 'hamilton.txt', 'r') as f:
    hamilton_text = f.read()

easter_eggs = {
    'jack': '😎😎😎😎', 
    'christ': 'Mono queen??',
    'julia': '💃💃💃'
}

bad_actors = dict()

app = Flask(__name__)

with open(Path(__file__).parent / 'badwords.txt', 'r') as f:
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
    warn_about_behavior = False
    output = ''

    if bad_actors.get(request.host, -1) >= 3:
        bad_actors[request.host] = 0
        warn_about_behavior = True

    if request.method == 'POST': 
        if request.form.get('submit_button') == 'Tell me a Joke':
            output = 'no'
        else:
            user_input = request.form.get('user_input').lower()
            if any(x in user_input for x in bad_words):
                mean = True
                bad_actors[request.host] = bad_actors.get(request.host, 0) + 1
                print(bad_actors, request.host)
                if bad_actors[request.host] >= 3:
                    return redirect(random.choice(punishment_links), code=302)
            output = user_input
    
        if not NO_FLAPPY:
            print(output)
            send_splitflap_text(output)

    if user_input:
        default_response = f'You last entered: "{user_input}".'
        if mean:
            default_response += " (and that wasn't very nice!)"
        response_text = easter_eggs.get(user_input, default_response)
    
    else:
        response_text = None

    # hack: if this is hamilton, render hamilton
    if user_input in ('hammie', 'hamilt', 'hammy'):
        return render_template('hamilton.html')

    return render_template('home.html', response_text=response_text, mean=mean, warn_about_behavior=warn_about_behavior)

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

    if NO_FLAPPY:
        app.run(host='0.0.0.0', port=5000, debug=True)
        sys.exit(0)

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = ask_for_serial_port()
        
    with splitflap_context(port) as s:
        app.run(host='0.0.0.0', port=5000)

