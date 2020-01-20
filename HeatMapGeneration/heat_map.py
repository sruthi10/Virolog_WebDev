from math import pi
import pandas as pd

from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure
#from bokeh.sampledata.unemployment1948 import data
data = pd.read_csv("geneExpressionData_test.csv")
data['Description'] = data['Description'].astype(str)
data = data.set_index('Description')
#data.drop('Annual', axis=1, inplace=True)
data.columns.name = 'Tissue'

genes = list(data.index)
tissues = list(data.columns)

# reshape to 1D array or rates with a gene description and tissue for each row.
df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()

# this is the colormap
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

source = ColumnDataSource(df)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="Gene Expression Localization", x_range=genes, y_range=list(reversed(tissues)), x_axis_location="above", plot_width=1200, plot_height=1200, tools=TOOLS, toolbar_location='below')

p.title.text_font_size = "15pt"
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "12pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="Description", y="Tissue", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="12pt", ticker=BasicTicker(desired_num_ticks=len(colors)), formatter=PrintfTickFormatter(format="%d"), label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('Location', '@Description - @Tissue'),
     ('Value', '@rate'),
]

show(p)      # show the plot