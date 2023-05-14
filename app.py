

from flask import Flask, session, request, render_template, redirect, url_for
import openai
import os

app = Flask(__name__)
app.secret_key = '123efg@12345'

API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError('No API Key found')

openai.api_key = API_KEY

@app.route('/')
def index():
    prompts = session.get('prompts', [])
    responses = session.get('responses', [])
    return render_template('index.html', prompts=prompts, responses=responses)

@app.route('/reset-history')
def reset_history():
    session['prompts'] = []
    session['responses'] = []
    return redirect(url_for('index'))

@app.route('/generate_text', methods=['POST'])
def generate_text():
    prompt = request.form['prompt']
    prompts = session.get('prompts', [])
    responses = session.get('responses', [])
    prompts.append(prompt)
    response = openai.Completion.create(engine='text-davinci-003', prompt=prompt, max_tokens=2000)
    response_text = response['choices'][0]['text']
    responses.append(response_text)
    session['prompts'] = prompts
    session['responses'] = responses
    return render_template('index.html', prompts=prompts, responses=responses, response=response_text, prompt=prompt)

if __name__ == '__main__':
    app.run(debug=True)
