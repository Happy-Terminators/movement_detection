import os
import subprocess
import pytube
import re

import argparse

def download_youtuber_main(video_dir):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          "]+", flags=re.UNICODE)

    youtube_url_file = open(os.path.join("for_new\\txts\\urls", "current_url.txt"), 'r')
    urls = youtube_url_file.read()
    urls = urls.split("\n")
    youtube_url_file.close()
    youtube_url_file = open(os.path.join("for_new\\txts\\urls", "current_url.txt"), 'w')
    youtube_url_file.close()

    youtube_title_file = open(os.path.join("for_new\\txts\\urls", "searched_urls.txt"), 'r')
    titles = youtube_title_file.read()
    titles = titles.split("\n")
    youtube_title_file.close()
    youtube_title_file = open(os.path.join("for_new\\txts\\urls", "searched_urls.txt"), 'a')

    if urls[-1] == "":
        del urls[-1]

    if titles[-1] == "":
        del titles[-1]

    for url in urls:
        yt = pytube.YouTube(url)

        if url in titles:
            print("already done downloading " + url)

        else:
            streams = list()
            best_stream = None
            
            for e in yt.streams.filter(file_extension='mp4', only_video=True).all():
                if e.resolution is not None:
                    streams.append(e)


            for i, e in enumerate(streams):
                #print(e)

                if i == 0 :
                    best_stream = streams[i]

                if i == len(streams) - 1:
                    break

                if int(streams[i].resolution[:-1]) < int(streams[i + 1].resolution[:-1]):
                    best_stream = streams[i + 1].resolution


            vids = yt.streams.filter(file_extension='mp4', only_video=True).all()

            print("downloading " + url)
            youtube_title_file.write(url + '\n')

            best_stream.download(video_dir)

    youtube_title_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--video_dir",
        type=str,
        )

    args = parser.parse_args()

    download_youtuber_main(args.video_dir)

