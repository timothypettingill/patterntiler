# PatternTiler

PatternTiler is a web app that allows users to create 
wallpapers out of tileable patterns. It was built using [starlette](https://www.starlette.io), a high performance Python ASGI framework.

![PatternTiler index page](./screenshots/index.png?raw=true)

## Usage

Open the web app in your browser at https://www.patterntiler.com or 
follow the installation instructions to run the app locally on your 
machine.


## Installation

> Requires Python 3.8+

Clone or download this repository.

```sh
$ git clone git@github.com:timothypettingill/patterntiler.git
```

Install the required packages.

```sh
$ pip install -r requirements.txt
```

Run the app with uvicorn or another ASGI server.

```sh
$ uvicorn patterntiler.app:app
```

## Dependencies

- aiofiles
- httpx
- Jinja2
- Pillow
- python-multipart
- starlette
- WTForms

## Roadmap

- [x] Create MVP
- [x] Handle image URLs.
- [ ] Expose API
- [ ] Add size presets for popular devices
- [ ] Integrate with https://www.subtlepatterns.com

# License

PatternTiler is licensed under the [MIT license](./LICENSE).



