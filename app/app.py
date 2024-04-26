from flask import Flask, request, render_template_string
from b_y_ion import *

app = Flask(__name__)

@app.route('/')
def form():
    form_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
        }
        form {
            border: 1px solid #ccc;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }
        label, input {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }
        input[type="text"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
    </head>
    <body>
        <form action="/result" method="post">
            <label for="peptide">Enter Peptide Sequence:</label>
            <input type="text" id="peptide" name="peptide">
            <input type="submit" value="Calculate">
        </form>
    </body>
    </html>
    '''
    return form_html

@app.route('/result', methods=['POST'])
def result():
    try:
        peptide = request.form['peptide']
        df, b_frag, y_frag = cal_b_y_ion_mass(peptide)
        # Use Pandas to convert the DataFrame to HTML
        df_html = df.to_html(classes='dataframe', border=0)

        # Render the HTML with styling
        html = render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body, html {
                    height: 100%;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-family: Arial, sans-serif;
                }
                .dataframe {
                    border-collapse: collapse;
                    width: 60%;
                    margin: auto;
                }
                .dataframe, .dataframe th, .dataframe td {
                    border: 1px solid #ddd;
                    text-align: left;
                    padding: 8px;
                }
                .dataframe th {
                    background-color: #f2f2f2;
                }
                .dataframe tr:nth-child(even){background-color: #f9f9f9;}
                .dataframe tr:hover {background-color: #f1f1f1;}
            </style>
        </head>
        <body>
            {{ table|safe }}
        </body>
        </html>
        ''', table=df_html)

        return html

    except Exception as e:
        return f"Error processing the request: {str(e)}"

if __name__ == '__main__':

    app.run()
