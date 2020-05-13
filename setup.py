from pathlib import Path
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent
LONG_DESCRIPTION = BASE_DIR.joinpath("README.md").read_text()


setup(
    name="patterntiler",
    version="1.0.0",
    description="Create beautiful wallpapers by tiling your favorite patterns.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/timothypettingill/patterntiler",
    author="Timothy Pettingill",
    author_email="tpettingill@outlook.com",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=[
        "aiofiles==0.5.0",
        "httpx==0.12.1",
        "Jinja2==2.11.2",
        "Pillow==7.1.2",
        "python-multipart==0.0.5",
        "starlette==0.13.4",
        "WTForms==2.3.1",
    ]
)