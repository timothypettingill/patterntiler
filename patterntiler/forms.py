from PIL import Image
import re

from typing import Optional
from wtforms import Form, StringField, IntegerField, FileField, Field
from wtforms.validators import (
    Optional,
    Regexp,
    URL,
    NumberRange,
    DataRequired,
    StopValidation,
)

Image.init()
IMAGE_FILE_EXTENSIONS = [x[1:] for x in Image.EXTENSION.keys()]
IMAGE_FILE_REGEX_PATTERN = re.compile(
    fr"^.*\.({'|'.join(IMAGE_FILE_EXTENSIONS)})$", flags=re.IGNORECASE
)


def image_file_or_image_url_required(form: Form, field: Field) -> None:
    """
    Ensure an image file or image URL was provided.
    """
    if not form.image_file.data and not form.image_url.data:
        raise StopValidation(message="An image file or image URL must be provided.")


class OptionalIf:
    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def __call__(self, form: Form, field: Field) -> None:
        if form.data.get(self.field_name):
            field.errors[:] = []
            raise StopValidation()


class IndexForm(Form):
    image_file = FileField(
        label="Image File",
        validators=[
            image_file_or_image_url_required,
            OptionalIf("image_url"),
            Regexp(IMAGE_FILE_REGEX_PATTERN, message="This filetype is not supported."),
        ],
    )
    image_url = StringField(
        label="Image URL",
        validators=[
            image_file_or_image_url_required,
            OptionalIf("image_file"),
            URL(),
            Regexp(IMAGE_FILE_REGEX_PATTERN, message="This filetype is not supported."),
        ],
    )
    width = IntegerField(
        label="Width",
        description="Enter target width in pixels",
        validators=[DataRequired(), NumberRange(min=0, max=3840)],
    )
    height = IntegerField(
        label="Height",
        description="Enter target height in pixels",
        validators=[DataRequired(), NumberRange(min=0, max=2160)],
    )
