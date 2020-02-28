import os
import argparse
import shutil

from for_new.get_urls import get_youtube_urls
from for_new.youtube_downloader import download_youtuber_main
from for_new.extract_frame_from_video import video2frame_main
from for_new.remove_same_frames import remove_same_frames_main
from for_new.make_dog_label import make_dog_label_main
from for_already.convert_txt_2_xml import convert_txt_2_xml_main
from for_already.match_img_anno import match_img_anno_main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--scroll_times",
        type=int,
        )

    parser.add_argument(
        "--maximum_play_time",
        type=int,
        )

    parser.add_argument(
        "--frame_interval",
        type=int,
        )

    parser.add_argument(
        "--min_w_ratio", 
        required=True, 
        type=float,
        help="minimum width ratio of AoI"
        )

    parser.add_argument(
        "--min_h_ratio", 
        required=True, 
        type=float, 
        help="minimum height ratio of AoI"
        )

    parser.add_argument(
        "--SSIM_thredhold", 
        required=True, 
        type=float
        )

    args = parser.parse_args()

    # folder directory
    video_dir = os.path.join("for_new", "youtube_videos")
    frame_dir = os.path.join("for_new", "frames")
    image_dir = os.path.join("for_new", "images")
    raw_txt_annotations_dir = os.path.join("for_new", 'annotations', 'raw_txts')
    labeled_txt_annotations_dir = os.path.join("for_new", 'annotations', 'labeled_txts')
    labeled_xml_annotations_dir = os.path.join("for_new", 'annotations', 'labeled_xmls')
    human_validation_dir = os.path.join("for_new", "human_validation")

    #url txt files
    new_urls_txt_dir = os.path.join("for_new\\txts\\urls", "new_urls.txt")
    current_urls_txt_dir = os.path.join("for_new\\txts\\urls", "current_url.txt")

    # create directorys at start
    if os.path.exists(video_dir) == False:
        os.makedirs(video_dir)

    if os.path.exists(frame_dir) == False:
        os.makedirs(frame_dir)

    if os.path.exists(image_dir) == False:
        os.makedirs(image_dir)

    if os.path.exists(raw_txt_annotations_dir) == False:
        os.makedirs(raw_txt_annotations_dir)

    if os.path.exists(labeled_txt_annotations_dir) == False:
        os.makedirs(labeled_txt_annotations_dir)

    if os.path.exists(labeled_xml_annotations_dir) == False:
        os.makedirs(labeled_xml_annotations_dir)

    if os.path.exists(human_validation_dir) == False:
        os.makedirs(human_validation_dir)

    # use moduels
    get_youtube_urls(args.scroll_times, args.maximum_play_time) # crawl youtube urls

    for new_url in open(new_urls_txt_dir).read().splitlines():
        current_url_txt_file = open(current_urls_txt_dir, 'w')
        current_url_txt_file.write(new_url)
        current_url_txt_file.close()

        download_youtuber_main(video_dir)

        print("extracting frames...")
        video2frame_main(video_dir, frame_dir, args.frame_interval)

        current_video = os.listdir(video_dir)
        os.remove(os.path.join(video_dir, current_video[0]))

        print("detecting movement spots...")
        remove_same_frames_main(frame_dir, image_dir, raw_txt_annotations_dir, args.min_w_ratio, args.min_h_ratio, args.SSIM_thredhold)
        for frame_file in os.listdir(frame_dir):
            os.remove(os.path.join(frame_dir, frame_file))
        

        make_dog_label_main(raw_txt_annotations_dir, image_dir, labeled_txt_annotations_dir)
        for raw_txt_file in os.listdir(raw_txt_annotations_dir):
            os.remove(os.path.join(raw_txt_annotations_dir, raw_txt_file))


        match_img_anno_main(labeled_txt_annotations_dir, image_dir)

        convert_txt_2_xml_main(image_dir, labeled_xml_annotations_dir, labeled_txt_annotations_dir)
        for labeled_txt_file in os.listdir(labeled_txt_annotations_dir):
            os.remove(os.path.join(labeled_txt_annotations_dir, labeled_txt_file))

        for xml in os.listdir(labeled_xml_annotations_dir):
            shutil.move(os.path.join(labeled_xml_annotations_dir, xml), os.path.join(human_validation_dir, xml))

        for img in os.listdir(image_dir):
            shutil.move(os.path.join(image_dir, img), os.path.join(human_validation_dir, img))

    # del all directorys and files
    new_url_txt_file = open(os.path.join("for_new\\txts\\urls", "new_urls.txt"), 'w')
    new_url_txt_file.close()

    # message
    print("use \"python labeling\\labelImg.py " + human_validation_dir + " " + os.path.join('for_new\\txts\\labels','dog_label.txt' + "\" to verify results by human-touch"))