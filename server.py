import asyncio
import logging
from datetime import datetime

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request


async def make_archive(folder: str = "./data", name: str = "photos"):
    process = await asyncio.create_subprocess_exec(
        "zip",
        "-",
        folder,
        "-r",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async with aiofiles.open(f"{name}.zip", "wb") as archive:
        while not process.stdout.at_eof():
            new_bytes = await process.stdout.read(100 * 1024)
            await archive.write(new_bytes)


async def main():
    await make_archive(name="dd")


async def archive(request: Request):
    raise NotImplementedError


async def handle_index_page(request: Request):
    async with aiofiles.open("index.html", "r") as index_file:
        index_contents = await index_file.read()  # Будет читаться до конца файла
    return web.Response(text=index_contents, content_type="text/html")


INTERVAL_SECS = 1


async def uptime_handler(request: Request):
    response = web.StreamResponse()
    response.headers["Content-Type"] = "text/html"
    # Отправляем клиенту заголовки, куки, статус код
    await response.prepare(request)

    while True:
        formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{formatted_date}<br>"
        await response.write(message.encode("utf-8"))
        await asyncio.sleep(INTERVAL_SECS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}", archive),
        web.get("/time", uptime_handler)
    ])

    web.run_app(app)
