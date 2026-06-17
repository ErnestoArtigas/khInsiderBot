"""
Code written by Ernesto Artigas.
Licence GNU General Public Licence v3.0.
"""

import asyncio
import concurrent.futures
import os
import re
from multiprocessing import cpu_count
from urllib.parse import unquote

import aiofiles
import httpx
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table

from core.dependencies import rich_console


def remove_invalid_chars(string) -> str:
    return re.sub(pattern=r'[\\\/?:*"<>|]', repl="", string=string)


def extract_decode_filename(url: str) -> str:
    return unquote(string=url.split("/")[-1])


def create_directory(
    directory_name: str,
) -> str | None:
    path = os.path.join(os.getcwd(), directory_name)
    try:
        os.mkdir(path=path)
        return path
    except OSError:
        rich_console.print_exception(show_locals=True)
        return None


def parallel_download_files(links: list[str], path: str) -> None:
    """
    To get the right size_chunks, there are two rules:
    - If the array's length is smaller than the cpu_count, then each chunks is 1 element long.
    - Else, we use the cpu_count to divide the array's length.
    """
    size_chunks = round(
        number=len(links) / (len(links) if len(links) < cpu_count() else cpu_count())
    )

    # Divides the array into chunks for each processes.
    links_chunked = [
        links[i : i + size_chunks] for i in range(0, len(links), size_chunks)
    ]

    futures = []

    with rich_console.status(
        status=f"[bold cyan]Using {len(links_chunked)} cores to download {len(links)} tracks..."
    ) as _:
        # Running as much workers as chunks in the array (lower or equal to cpu_count).
        progress_table = Table.grid()
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=len(links_chunked)
        ) as executor:
            for i in range(len(links_chunked)):
                futures.append(
                    executor.submit(
                        process_download_files, links_chunked[i], path, progress_table
                    )
                )

        with Live(progress_table, refresh_per_second=10):
            concurrent.futures.wait(futures)


def process_download_files(links: list[str], path: str, progress_table: Table) -> None:
    async def async_download_files(
        links: list[str], path: str, progress_table: Table
    ) -> None:
        async with httpx.AsyncClient() as client:
            await download_files(
                links=links, path=path, client=client, progress_table=progress_table
            )

    asyncio.run(
        main=async_download_files(links=links, path=path, progress_table=progress_table)
    )


async def download_files(
    links: list[str], path: str, client: httpx.AsyncClient, progress_table: Table
) -> None:
    progress_bar = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )
    progress_table.add_row(Panel.fit(progress_bar))

    for link in links:
        file_name = extract_decode_filename(url=link)
        async with aiofiles.open(file=os.path.join(path, file_name), mode="wb") as file:
            async with client.stream(method="GET", url=link) as response:
                download_task = progress_bar.add_task(
                    f"Download {file_name}",
                    total=int(
                        response.headers["Content-Length"],
                    ),
                    filename=file_name,
                )
                async for chunk in response.aiter_bytes():
                    await file.write(chunk)
                    progress_bar.update(download_task, advance=len(chunk))
