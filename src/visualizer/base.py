from os import path
import urllib.parse
import urllib.request

import plotly
from aiogram.types import BufferedInputFile
from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure
from plotly.io import kaleido
from sqlalchemy.engine import Row

from src.bot.structures.types import VisualizeFormat
from src.visualizer.utils import fig_to_html, fig_to_json, fig_to_image

# Configuring plotlyjs to run the engine standalone without invoking cdn
kaleido.scope.plotlyjs = urllib.parse.urljoin("file:",
                                              urllib.request.pathname2url(path.join(plotly.__path__[0],
                                                                                    "package_data",
                                                                                    "plotly.min.js")))


_timeline_buttons = [dict(count=1,
                          label="1 hour",
                          step="hour",
                          stepmode="backward"),
                     dict(count=1,
                          label="1 day",
                          step="day",
                          stepmode="backward"),
                     dict(count=7,
                          label="1 week",
                          step="day",
                          stepmode="backward"),
                     dict(count=1,
                          label="1 month",
                          step="month",
                          stepmode="backward"),
                     dict(count=6,
                          label="6 months",
                          step="month",
                          stepmode="backward"),
                     dict(count=1,
                          label="1 year",
                          step="year",
                          stepmode="backward"),
                     dict(step="all")]


def _get_fig_timeline(data: list[Row], title: str):
    df: DataFrame = DataFrame(data)
    date_title = df.columns[0]
    count_title = df.columns[2]
    df = df.pivot_table(index=date_title,
                        columns=df.columns[1],
                        values=count_title,
                        aggfunc="sum").fillna(0).reset_index()
    fig = px.line(df, x=date_title, y=df.columns, title=title)
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=_timeline_buttons,
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date",
            title=date_title
        ),
        yaxis=dict(title=count_title))

    return fig


def visualize_timeline(data: list[Row],
                       *,
                       title: str,
                       filename_no_ext: str,
                       visualize_format: VisualizeFormat,
                       height: int = 720,
                       width: int = 1280) -> BufferedInputFile:
    fig: Figure = _get_fig_timeline(data, title)
    match visualize_format:
        case VisualizeFormat.HTML:
            return fig_to_html(fig, filename_no_ext)
        case VisualizeFormat.JSON:
            return fig_to_json(fig, filename_no_ext)
        case _:
            return fig_to_image(fig,
                                filename_no_ext,
                                img_format=visualize_format,
                                height=height,
                                width=width)
