import asyncio
import logging
import os
import re
import sys
from functools import partial

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request

from config import load_config


async def index_handler(request: Request):
    async with aiofiles.open("index.html", "r") as index_file:
        index_contents = await index_file.read()

    return web.Response(text=index_contents, content_type="text/html")


def create_zip_process(archive_hash: str):
    command = ["zip", "-", "-r", f"{archive_hash}/"]
    process = asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    return process


async def download_archive(request: Request, response_delay: float):
    archive_hash = request.match_info["archive_hash"]

    if not re.match(r"\w+", archive_hash):
        raise web.HTTPBadRequest(text="Некорректный хэш.")
    elif not os.path.exists(f"{archive_hash}/"):
        raise web.HTTPNotFound(text="Архив не существует или был удален.")

    response = web.StreamResponse()
    response.headers.update({
        "Content-Type": "application/zip",
        "Content-Disposition": f'attachment; filename="{archive_hash}.zip"'
    })

    response.enable_chunked_encoding()
    await response.prepare(request)
    process = await create_zip_process(archive_hash)
    iteration = 1
    chunk_size = 500 * 1024

    try:
        while not process.stdout.at_eof():
            chunk = await process.stdout.read(chunk_size)
            await response.write(chunk)
            logging.debug(f"Sending archive chunk #{iteration}...")
            iteration += 1
            await asyncio.sleep(response_delay)

        await response.write_eof()

    except asyncio.CancelledError:
        logging.error("Download was interrupted: User stopped the downloading")
        raise
    except SystemExit:
        logging.error("Download was interrupted: SystemExit")
    except BaseException as e:
        logging.error(f"Download was interrupted: {type(e).__name__} with args: {e.args}")
    finally:
        if process.returncode != 0:
            process.kill()
        await process.communicate()

        return response


def main():
    logging.basicConfig(
        format=u"%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S",
    )

    config = load_config()

    if not config.log:
        logging.disable(sys.maxsize)

    os.chdir(config.path)
    archive_handler = partial(download_archive, response_delay=config.delay)

    app = web.Application()
    app.add_routes([
        web.get("/", index_handler),
        web.get("/archive/{archive_hash}", archive_handler),
    ])

    web.run_app(app)


if __name__ == "__main__":
    main()
