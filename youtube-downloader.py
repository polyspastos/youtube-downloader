import subprocess
import click
from pathlib import Path
from datetime import datetime, timedelta


@click.command()
@click.option("--audio", is_flag=True, help="Download audio only")
@click.option("--days", type=int, default=7, help="Number of days to check for recent videos")
@click.argument("item_list", type=click.Path(exists=True), default="item_list.txt")
def download_videos_from_item_list(item_list, audio, days):
    items = Path(item_list).read_text().splitlines()

    videos_dir = Path("videos")
    videos_dir.mkdir(exist_ok=True)

    date_after = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

    for item in items:
        print(f"Downloading videos from the last {days} days for item: {item}")

        if not item.startswith('#'):
            if item.startswith('playlist:'):
                command = (
                    f"yt-dlp --break-on-reject "
                    f"{item.split(':', 1)[-1]} "
                    f"--output videos/{item}/%(title)s.%(ext)s "
                    "--download-archive downloaded_already.txt"
                )            
            elif item.startswith('full:'):
                command = (
                    f"yt-dlp --break-on-reject "
                    f"https://www.youtube.com/@{item.split(':', 1)[-1]} "
                    f"--output videos/full_dl/{item.split(':', 1)[-1]}/%(title)s.%(ext)s "
                    "--download-archive downloaded_already.txt"
                )            
            else:
                command = (
                    f"yt-dlp --break-on-reject --dateafter {date_after} "
                    f"https://www.youtube.com/@{item} "
                    f"--output videos/{item}/%(title)s.%(ext)s "
                    "--download-archive downloaded_already.txt"
                )

            if audio:
                command += (
                    " --extract-audio --audio-format best "
                    "--audio-quality 0 "
                    f"--output /audio/%(title)s.%(ext)s "
                    "--ffmpeg-location c:/Users/tecton/tools/ffmpeg-master-latest-win64-gpl-shared/ffmpeg-master-latest-win64-gpl-shared/bin/"
                )

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print("Error occurred while executing the command:")
                print(stderr)

                print("Moving to the next item.")
                continue

            print("Command executed successfully.")
            print(stdout)


if __name__ == "__main__":
    download_videos_from_item_list()
