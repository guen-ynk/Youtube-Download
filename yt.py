import errno
import os

import youtube_dl

path = os.path.dirname(__file__)

try:
    os.mkdir((path + "/music"))
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './music/%(title)s.%(ext)s',
    'ffmpeg_location': './ffmpeg/bin/',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
ydl_optsmp4 = {
    'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'outtmpl': './music/%(title)s.%(ext)s',
}


def read_txt(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def download(playlist):
    for i in playlist:
        if "https://" in i:
            if "!" in i[0]:
                i = i[1:]
                with youtube_dl.YoutubeDL(ydl_optsmp4) as ydl:
                    ydl.download([i])
            else:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([i])
        else:
            ydl_opts['outtmpl'] = './music/' + i + '/%(title)s.%(ext)s'
            ydl_optsmp4['outtmpl'] = './music/' + i + '/%(title)s.%(ext)s'


if __name__ == '__main__':
    download(read_txt("./Playlist.txt"))
