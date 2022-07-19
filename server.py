import asyncio
import logging
import re
import sys
from os import path

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request

from config import load_config


async def index_handler(request: Request):
    async with aiofiles.open("index.html", "r") as index_file:
        index_contents = await index_file.read()

    return web.Response(text=index_contents, content_type="text/html")


def create_zip_process(archive_hash: str):
    command = ["zip", "-", "-r", "-j", f"{config.path}/{archive_hash}/"]
    process = asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    return process


class ServerError(Exception):
    pass


async def archive_handler(request: Request):
    archive = request.match_info.get("archive_hash")

    if not re.match(r"\w+", archive):
        raise web.HTTPBadRequest(text="Некорректный хэш.")
    elif not path.exists(f"{config.path}/{archive}"):
        raise web.HTTPNotFound(text="Архив не существует или был удален.")

    response = web.StreamResponse()
    response.headers.update({
        "Content-Type": "application/zip",
        "Content-Disposition": f'attachment; filename="{archive}.zip"'
    })

    await response.prepare(request)
    # response.enable_chunked_encoding()
    process = await create_zip_process(archive)
    iteration = 1
    chunk_size = 500 * 1024

    try:
        while not process.stdout.at_eof():
            chunk = await process.stdout.read(chunk_size)
            await response.write(chunk)
            logging.debug(f"Sending archive chunk #{iteration}...")
            iteration += 1

            # if iteration == 1000:
                # raise ServerError
                # raise SystemExit
            await asyncio.sleep(config.delay)

        await response.write_eof()

    except asyncio.CancelledError:
        logging.error("Download was interrupted: User stopped the downloading")
        process.kill()
        await process.communicate()
    except ServerError:
        logging.error("Download was interrupted: IndexError")
        process.kill()
        await process.communicate()
    except SystemExit:
        logging.error("Download was interrupted: SystemExit")
        process.kill()
        await process.communicate()
    finally:
        return response


if __name__ == "__main__":
    logging.basicConfig(
        format=u"%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S",
    )

    config = load_config()

    if config.nolog:
        logging.disable(sys.maxsize)

    app = web.Application()
    app.add_routes([
        web.get("/", index_handler),
        web.get("/archive/{archive_hash}", archive_handler),
    ])

    web.run_app(app)
