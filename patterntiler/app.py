from io import BytesIO
from pathlib import Path
from typing import Union

import httpx
from PIL import Image
from starlette.applications import Starlette
from starlette.datastructures import FormData, UploadFile
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .core import fetch_image, handle_image_file, tile_image
from .forms import IndexForm

templates = Jinja2Templates("templates")


class Index(HTTPEndpoint):
    """
    Website homepage.
    """

    async def get(self, request: Request) -> Jinja2Templates.TemplateResponse:
        """
        Display an empty `IndexForm`.
        """
        form = IndexForm()
        ctx = {"request": request, "title": "Index", "form": form}
        return templates.TemplateResponse("index.html", ctx)

    async def post(
        self, request: Request
    ) -> Union[StreamingResponse, Jinja2Templates.TemplateResponse]:
        """
        Handle a submitted `IndexForm`.

        If the form fails validation, redisplay the form with error
        messages. If the form passes validation, use the form data to
        create a wallpaper and return it to the user.

        Raises
        ------
        HTTPException
            If something goes wrong while trying to create the wallpaper.
        """
        form_data: FormData = await request.form()
        form_data = form_data._dict
        image_file: UploadFile = form_data.pop("image_file")
        form = IndexForm(**form_data, image_file=image_file.filename,)

        if form.validate():
            if form.image_file.data:
                pattern = handle_image_file(image_file.file)
                filename = f"{Path(image_file.filename).stem}-{form.width.data}x{form.height.data}.png"
            if form.image_url.data:
                pattern = fetch_image(form.image_url.data)
                filename = f"{Path(form.image_url.data).stem}-{form.width.data}x{form.height.data}.png"
            wallpaper = tile_image(pattern, form.width.data, form.height.data)
            f = BytesIO()
            wallpaper.save(f, format="PNG")
            f.seek(0)
            media_type = "image/png"
            content_disposition = f'attachment; filename="{filename}"'
            return StreamingResponse(
                f,
                headers={"content-disposition": content_disposition},
                media_type=media_type,
            )

        else:
            ctx = {"request": request, "form": form}
            return templates.TemplateResponse("index.html", ctx)


async def http_exception(
    request: Request, e: HTTPException
) -> Jinja2Templates.TemplateResponse:
    ctx = {
        "request": request,
        "title": e.status_code,
        "status_code": e.status_code,
        "message": e.detail,
    }
    return templates.TemplateResponse("exceptions.html", ctx)


routes = [
    Route("/", Index, name="index"),
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
]


exception_handlers = {HTTPException: http_exception}


app = Starlette(routes=routes, exception_handlers=exception_handlers)
