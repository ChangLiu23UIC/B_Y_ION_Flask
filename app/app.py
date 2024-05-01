from flask import Flask, request, render_template_string
from b_y_ion import *
from visualize_ms import *
from b_y_spectrum_data import *
from bokeh.embed import components


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
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f7f7f7;
            }
            form {
                background-color: #fff;
                border: none;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 10px;
                display: flex;
                flex-direction: column;
                width: 300px;
            }
            input[type="text"] {
                width: 100%;
                padding: 12px;
                margin-bottom: 20px;
                border: 2px solid #ccc;
                border-radius: 8px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                border-color: #007bff;
                outline: none;
            }
            input[type="submit"] {
                padding: 12px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-bottom: 10px; /* Add spacing between buttons if desired */
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            input[type="submit"]:first-of-type {
                background-color: #28a745; /* A green color for the first button */
            }
            input[type="submit"]:first-of-type:hover {
                background-color: #218838; /* Darken the green on hover */
            }
        </style>
    </head>
    <body>
        <form action="/result" method="post">
            <input type="text" id="data" name="data" placeholder="Enter Peptide Sequence or Sample Data" oninput="this.value = this.value.toUpperCase()">
            <input type="submit" value="B-Y Ion Separation">
            <input type="submit" formaction="/isotope" value="Isotope Analysis">
        </form>
    </body>
    </html>

    '''
    return form_html

@app.route('/result', methods=['POST'])
def handle_result():
    data = request.form['data']
    # Assume cal_b_y_ion_mass returns results appropriate for rendering
    df, b_frag, y_frag = cal_b_y_ion_mass(data)
    df_html = df.to_html(classes='dataframe', border=0)
        # Render the HTML with styling and additional tables
    return render_template_string('''
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
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }
            .dataframe {
                border-collapse: collapse;
                width: 60%;
                margin: 20px auto;
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
        <h2>Main Data</h2>
        {{ table|safe }}
    </body>
    </html>
    ''', table=df_html)


@app.route('/isotope', methods=['POST'])
def handle_isotope():
    data = request.form['data']
    isotope_dict = read_isotope_csv("isotope.csv")
    result = isotope_calculator(data, isotope_dict)
    plot = create_mass_spectrum_plot(result)
    return plot


if __name__ == '__main__':

    app.run()
