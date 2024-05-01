
from bokeh.models import HoverTool
from bokeh.plotting import figure, show
from bokeh.models import GlyphRenderer, LabelSet, ColumnDataSource
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.layouts import gridplot



def create_mass_spectrum_plot(ms_dict, line_color):

    masses = list(ms_dict.keys())
    probabilities = list(ms_dict.values())

    source = ColumnDataSource(data={
        'mass': masses,
        'probability': probabilities,
        'mass_text': [f"{mass:.1f}" for mass in masses]  # Text label for each mass
    })

    p = figure(title="Mass Spectrum", x_axis_label='Mass M/z', y_axis_label='Intensity',
               width=800, height=400, x_range=(min(masses) - 1, max(masses) + 1),
               y_range=(0, max(probabilities) + max(probabilities) * 0.1))

    p.segment(x0='mass', y0=0, x1='mass', y1='probability', color= line_color, line_width=2, source=source)

    p.add_tools(HoverTool(tooltips=[("Mass", "@mass{0.0}"), ("Probability", "@probability")]))

    labels = LabelSet(x='mass', y='probability', text='mass_text', level='glyph',
                      x_offset=0, y_offset=5, source=source)
    p.add_layout(labels)

    return p



def superimpose_plots(plot1, plot2):
    """
    Combine two plots into a single layout.

    Args:
    plot1 (figure): First Bokeh figure to combine.
    plot2 (figure): Second Bokeh figure to combine.
    layout (str): Layout orientation, 'horizontal' or 'vertical'.
    toolbar_location (str): Location of the toolbar, can be 'above', 'below', 'left', 'right', or 'none'.

    Returns:
    layout (gridplot): Combined gridplot object.
    """
    new_x_start = min(plot1.x_range.start, plot2.x_range.start) - 20
    new_x_end = max(plot1.x_range.end, plot2.x_range.end) + 20

    combined_plot = figure(title="B-Y-ION Mass Spectrum", x_axis_label=plot1.xaxis[0].axis_label,
                           y_axis_label=plot1.yaxis[0].axis_label,
                           x_range=(new_x_start, new_x_end), y_range=plot1.y_range)

    for plot in [plot1, plot2]:
        for renderer in plot.renderers:
            if isinstance(renderer, GlyphRenderer):
                glyph_clone = renderer.glyph.clone()
                combined_plot.add_glyph(renderer.data_source, glyph_clone)

    combined_plot.tools = plot1.tools + plot2.tools

    html = file_html(combined_plot, CDN)

    return html


if __name__ == '__main__':
    ms = {802.4007260000001: 0.6204353503100348, 803.400921: 0.24436153875197233, 804.4029763333333: 0.08038456698870841, 805.399877: 0.010007372238203072}
    mz = {702.4007260000001: 0.6204353503100348, 703.400921: 0.24436153875197233, 704.4029763333333: 0.08038456698870841, 705.399877: 0.010007372238203072}

    plot1 = create_mass_spectrum_plot(ms, "red")
    plot2 = create_mass_spectrum_plot(mz, "blue")

    dd = superimpose_plots(plot1, plot2)