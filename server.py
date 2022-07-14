import asyncio

import aiofiles
import aiohttp
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


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}", archive)
    ])
    web.run_app(app)
