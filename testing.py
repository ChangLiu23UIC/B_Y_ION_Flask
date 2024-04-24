from flask import Flask, request, render_template_string
import pandas as pd
from main import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['input_string']
        df = cal_b_y_ion_mass(user_input)
        return render_template_string("""
        <html>
            <head>
                <title>DataFrame Output</title>
            </head>
            <body>
                <h1>Resulting DataFrame</h1>
                {{ data_frame | safe }}
                <br>
                <a href="/">Go Back</a>
            </body>
        </html>
        """, data_frame=df.to_html())
    return '''
    <html>
        <body>
            <h1>Enter String Input</h1>
            <form method="post">
                String Input: <input type="text" name="input_string"><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
