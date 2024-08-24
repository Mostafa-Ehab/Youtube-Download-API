from os import path, system
import string
import random


def escape(s):
    """
    Escape special characters.

    https://github.com/jacebrowning/memegen#special-characters
    """
    for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                     ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''"), ("|", "-")]:
        s = s.replace(old, new)
    return s

# Define a function


def generate_trace_id(length=16):
    # Define all possible characters
    characters = string.ascii_letters + string.digits
    # Create random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    # Set the return value to the generated string
    return random_string


def load_title_dict():
    with open("./music/title", "r", encoding="utf-8") as file:
        data = file.readlines()
    titles_dict = {}
    for row in data:
        id, *title = row.split("|")
        titles_dict[id] = "|".join(title)

    return titles_dict


def get_file_name(id, title, res):
    if res:
        return f"{id}/{title}-{res}.mp4"
    else:
        return f"{id}/{title}-MP3.mp3"


def download_stream(id, title, audio, video, res):
    if res:
        if not path.isfile(f"music/{id}/{title}-MP3"):
            audio.download(f"music/{id}", f"{title}-MP3")

        if not path.isfile(f"music/{id}/{title}-{res}"):
            video.download(f"music/{id}", f"{title}-{res}")

        system(
            f'ffmpeg -i "music/{id}/{title}-{res}" -i "music/{id}/{title}-MP3" -c:v copy -c:a aac "music/{id}/{title}-{res}.mp4"')

    else:
        if not path.isfile(f"music/{id}/{title}-MP3"):
            audio.download(f"music/{id}", f"{title}-MP3")

        system(
            f'ffmpeg -i "music/{id}/{title}-MP3" "music/{id}/{title}-MP3.mp3"')


def file_download(id, title, audio, video=None, res=None):
    download_stream(id, title.strip(), audio, video, res)
