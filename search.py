import click
from pathlib import Path
import yt_dlp


@click.command()
@click.argument("keyword", type=str, metavar="KEYWORD")
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=False, writable=True),
    default="./videos/_searched/",
    help="Output directory for downloaded videos",
)
@click.option("--how-many", type=int, default=25, help="Number of results")
def search_and_download(keyword, output, how_many):
    output_path = Path.cwd() / Path(output) / Path(keyword.replace(" ", "_"))
    output_path.mkdir(parents=True, exist_ok=True)

    ydl_opts = {"outtmpl": str(output_path) + "\\%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f"ytsearch{how_many}:{keyword}"
        info_dict = ydl.extract_info(search_query, download=False)

        if "entries" in info_dict:
            videos = info_dict["entries"]

            for i, video in enumerate(videos, 1):
                video_url = video["webpage_url"]
                title = video["title"]
                uploader = video["uploader"]
                print(
                    f"{i}. Title: {title}\n   URL: {video_url}\n   Uploader: {uploader}\n"
                )

            download_indices = input(
                "Enter the numbers of the videos you want to download (e.g., '1 2 3 5 8') or 'all': "
            ).split()

            if "all" in download_indices:
                download_indices = range(1, len(videos) + 1)
            else:
                download_indices = [int(index) for index in download_indices]

            for index in download_indices:
                if 1 <= index <= len(videos):
                    video = videos[index - 1]
                    video_url = video["webpage_url"]
                    title = video["title"]
                    filename = f"{title}.mp4"
                    ydl.download([video_url])


if __name__ == "__main__":
    search_and_download()
