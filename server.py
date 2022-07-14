import asyncio
import logging

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request


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
    response = web.StreamResponse()
    response.headers.update({
        "Content-Type": "application/zip",
        "Content-Disposition": f'attachment; filename="{archive}.zip"'
    })

    await response.prepare(request)
    process = await create_zip_process(archive)

    while not process.stdout.at_eof():
        new_bytes = await process.stdout.read(100 * 1024)
        await response.write(new_bytes)
        logging.debug("new iteration")

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
