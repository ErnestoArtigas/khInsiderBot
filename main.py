from time import sleep

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
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

progress.start()

try:
    download_task = progress.add_task(
        description="Download 1",
        total=int(
            4,
        ),
        filename="file_name",
    )
    for i in range(0, 4):
        progress.update(download_task, advance=1)
        sleep(1)
finally:
    progress.stop()

print("tasks", progress.tasks, progress.task_ids)

progress.tasks.clear()

print("tasks", progress.tasks, progress.task_ids)

# progress.start()
# try:
#     download_task = progress.add_task(
#         description="Download 2",
#         total=int(
#             4,
#         ),
#         filename="file_name",
#     )
#     for i in range(0, 4):
#         progress.update(download_task, advance=1)
#         sleep(1)
# finally:
#     progress.stop()
