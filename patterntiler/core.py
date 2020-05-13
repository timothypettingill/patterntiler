from io import BytesIO
from math import ceil
from pathlib import Path
from typing import IO, Any, Optional, Union

import httpx
from PIL import Image
from starlette.exceptions import HTTPException

_FileLike = IO


def tile_image(
    im: Image.Image, width: int, height: int, mode: Optional[str] = "RGB", **kwargs: Any
) -> Image.Image:
    """
    Tile an image to a given width and height.

    Parameters
    ----------
    im
        The image to tile.
    width
        The width of the new image.
    height
        The height of the new image.
    mode
        The mode of the new image. Default is None, which will infer
        the mode from `im`.
    **kwargs
        Keyword arguments to pass to `Image.new`.

    Returns
    -------
    PIL.Image.Image
        A Pillow image object.
    
    Examples
    --------
    >>> from PIL import Image
    
    >>> im = Image.open("path/to/image.png")
    >>> tiled = tile_image(im, 1920, 1080)
    
    """
    im_out = Image.new(mode, (width, height), **kwargs)

    h_tiles = ceil(width / im.width)
    v_tiles = ceil(height / im.height)

    for i in range(v_tiles):
        y = im.height * i
        for j in range(h_tiles):
            x = im.width * j
            im_out.paste(im, box=(x, y))

    return im_out


def handle_image_file(file: _FileLike) -> Image.Image:
    """
    Open an image file as a Pillow image object.

    Parameters
    ----------
    file
        The image file.
    
    Returns
    -------
    PIL.Image.Image
        A Pillow image object.
    
    Raises
    ------
    HTTPException
        If the file cannot be found, or the image cannot be opened and 
        identified.

    Example
    -------
    >>> from io import BytesIO
    # assume the `raw_img` variable contains raw image data as bytes
    >>> f = BytesIO(raw_img)
    >>> im = handle_image_file(f)
    """
    try:
        im = Image.open(file)
        return im
    except IOError as e:
        raise HTTPException(500, detail=str(e))


def fetch_image(url: str) -> Image.Image:
    """
    Fetch an image from a given URL.

    Parameters
    ----------
    url
        The image URL.

    Returns
    -------
    PIL.Image.Image
        A Pillow Image object.

    Raises
    ------
    HTTPException
        If the response's status code is not 200 OK.

    Examples
    --------
    >>> url = "https://www.toptal.com/designers/subtlepatterns/patterns/moroccan-flower-dark.png"
    >>> im = fetch_image(url)
    """
    r = httpx.get(url)
    if not r.status_code == httpx.codes.OK:
        raise HTTPException(r.status_code, detail=r.reason_phrase)
    f = BytesIO(r.content)
    im = handle_image_file(f)
    return im
