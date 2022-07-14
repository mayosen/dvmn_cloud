import asyncio
import logging
import re
from os import path

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request


# TODO: Шаг 9. Сервер откажется создавать архив для каталога . или ..


async def index_handler(request: Request):
    async with aiofiles.open("index.html", "r") as index_file:
        index_contents = await index_file.read()  # Будет читаться до конца файла
    return web.Response(text=index_contents, content_type="text/html")


async def create_zip_process(archive_hash: str):
    command = ["zip", "-", "-r", "-j", f"photos/{archive_hash}/"]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return process


async def archive_handler(request: Request):
    archive = request.match_info.get("archive_hash")

    if not re.match(r"\w+", archive):
        raise web.HTTPBadRequest(text="Некорректный хэш.")
    elif not path.exists(f"photos/{archive}"):
        raise web.HTTPNotFound(text="Архив не существует или был удален.")

    response = web.StreamResponse()
    response.headers.update({
        "Content-Type": "application/zip",
        "Content-Disposition": f'attachment; filename="{archive}.zip"'
    })

    await response.prepare(request)
    process = await create_zip_process(archive)
    iteration = 1

    while not process.stdout.at_eof():
        new_bytes = await process.stdout.read(100 * 1024)
        await response.write(new_bytes)
        logging.debug(f"Sending archive chunk #{iteration}...")
        iteration += 1

    await response.write_eof()
    return response


if __name__ == "__main__":
    logging.basicConfig(
        format=u"%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S"
    )

    app = web.Application()
    app.add_routes([
        web.get("/", index_handler),
        web.get("/archive/{archive_hash}", archive_handler),
    ])

    web.run_app(app)
