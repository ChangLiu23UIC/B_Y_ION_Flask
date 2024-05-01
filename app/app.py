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
            font-family: Arial, sans-serif;
        }
        form {
            border: 1px solid #ccc;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }
        label, input, a.button {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }
        input[type="text"], a.button {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"], a.button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
        }
        input[type="submit"]:hover, a.button:hover {
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
        <a href="/isotope" class="button">Go to Isotope Analysis</a>  <!-- Link styled as button -->
    </body>
    </html>
    '''
    return form_html

@app.route('/result', methods=['POST'])
def handle_result():
    try:
        peptide = request.form['peptide']
        df, b_frag, y_frag = cal_b_y_ion_mass(peptide)  # Assume returns DataFrame and lists for b and y ions

        # Use Pandas to convert the main DataFrame to HTML
        df_html = df.to_html(classes='dataframe', border=0)

        # Convert b and y fragmentation lists to HTML table
        b_frag_html = pd.DataFrame(b_frag).to_html(classes='dataframe',
                                                   border=0)  # Assuming b_frag is list of dicts or similar
        y_frag_html = pd.DataFrame(y_frag).to_html(classes='dataframe',
                                                   border=0)  # Assuming y_frag is list of dicts or similar

        # Render the HTML with styling and additional tables
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
            <h2>B Fragmentation</h2>
            {{ b_frag_table|safe }}
            <h2>Y Fragmentation</h2>
            {{ y_frag_table|safe }}
        </body>
        </html>
        ''', table=df_html, b_frag_table=b_frag_html, y_frag_table=y_frag_html)

        return html

    except Exception as e:
        return f"Error processing the request: {str(e)}"


@app.route('/isotope', methods=["GET"])
def handle_isotope():
    if request.method == 'GET':
        try:
            sample = request.form['sample']
            isotope_dict = read_isotope_csv("isotope.csv")
            result = isotope_calculator(sample, isotope_dict)

            plot = create_mass_spectrum_plot(result)
            script, div = components(plot)

            df = pd.DataFrame(result)
            df_html = df.to_html(classes='dataframe', border=0)

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
                        flex-direction: column;
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
                {{ script|safe }}
            </head>
            <body>
                {{ div|safe }}
                {{ table|safe }}
            </body>
            </html>
            ''', script=script, div=div, table=df_html)

            return html
        except Exception as e:
            return f"Error processing the request: {str(e)}"


if __name__ == '__main__':

    app.run()
