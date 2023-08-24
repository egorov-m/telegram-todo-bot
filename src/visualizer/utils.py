from aiogram.types import BufferedInputFile
from plotly.graph_objs import Figure

from src.bot.structures.types import ImageFormat


def fig_to_html(fig: Figure, filename: str) -> str:
    html: str = fig.to_html(full_html=False)
    return _get_input_file(html, filename, ".html")


def fig_to_json(fig: Figure, filename: str) -> str:
    json: str = fig.to_json()
    return _get_input_file(json, filename, ".json")


def fig_to_image(fig: Figure,
                 filename: str,
                 *,
                 img_format: ImageFormat = ImageFormat.JPG,
                 height: int = 720,
                 width: int = 1280) -> BufferedInputFile:
    file: bytes = fig.to_image(format=str(img_format),
                               engine="kaleido",
                               height=height,
                               width=width)
    return _get_input_file(file, filename, f".{img_format}")


def _get_input_file(data: bytes | str, filename: str, ext: str) -> BufferedInputFile:
    if not filename.endswith(ext):
        filename += ext
    if isinstance(data, str):
        data = data.encode(encoding="utf-8")
    return BufferedInputFile(file=data, filename=filename)
