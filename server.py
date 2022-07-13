import asyncio


async def make_archive(folder: str = "./data", name: str = "photos"):
    process = await asyncio.create_subprocess_exec(
        "zip",
        "-",
        folder,
        "-r",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    with open(f"{name}.zip", "wb") as archive:
        while not process.stdout.at_eof():
            new_bytes = await process.stdout.read(100 * 1024)
            archive.write(new_bytes)


async def main():
    await make_archive(name="dd")


asyncio.run(main())
