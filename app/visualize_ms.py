from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, ColumnDataSource, LabelSet

def create_mass_spectrum_plot(ms_dict, output_path='mass_spectrum.html'):
    # Prepare data
    masses = list(ms_dict.keys())
    probabilities = list(ms_dict.values())

    # Create ColumnDataSource for better integration with Bokeh
    source = ColumnDataSource(data={
        'mass': masses,
        'probability': probabilities,
        'mass_text': [f"{mass:.1f}" for mass in masses]  # Text label for each mass
    })

    # Output to static HTML file
    output_file(output_path)

    # Create a new plot with width and height
    p = figure(title="Mass Spectrum", x_axis_label='Mass M/e', y_axis_label='Intensity',
               width=800, height=400, x_range=(min(masses) - 1, max(masses) + 1),
               y_range=(0, max(probabilities) + max(probabilities) * 0.1))

    # Add segments (vertical lines) for each mass/probability pair
    p.segment(x0='mass', y0=0, x1='mass', y1='probability', color="firebrick", line_width=2, source=source)

    # Add Hover tool to display mass and probability
    p.add_tools(HoverTool(tooltips=[("Mass", "@mass{0.0}"), ("Probability", "@probability")]))

    # Create labels for each peak
    labels = LabelSet(x='mass', y='probability', text='mass_text', level='glyph',
                      x_offset=0, y_offset=5, source=source)
    p.add_layout(labels)

    # Save the plot
    save(p)

    return output_path

if __name__ == '__main__':
    ms = {802.4007260000001: 0.6204353503100348, 803.400921: 0.24436153875197233, 804.4029763333333: 0.08038456698870841, 805.399877: 0.010007372238203072}
    create_mass_spectrum_plot(ms)