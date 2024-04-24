from flask import Flask, request, render_template_string
from b_y_ion import *

app = Flask(__name__)

@app.route('/')
def form():
    form_html = '''
    <form action="/result" method="post">
        <label for="peptide">Enter Peptide Sequence:</label>
        <input type="text" id="peptide" name="peptide">
        <input type="submit" value="Calculate">
    </form>
    '''
    return form_html

@app.route('/result', methods=['POST'])
def result():
    peptide = request.form['peptide']
    df = cal_b_y_ion_mass(peptide)
    return render_template_string(df.to_html(classes='data'))

if __name__ == '__main__':
    app.run(debug=True)
