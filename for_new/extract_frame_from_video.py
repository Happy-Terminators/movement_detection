import cv2
import os
import hashlib
import argparse


def video2frame(invideofilename, save_path, video_name, interval):
    pre_name = video_name
    encoded_string = pre_name.encode()
    #print(encoded_string)
    hexdigest = hashlib.sha256(encoded_string).hexdigest()

    vidcap = cv2.VideoCapture(invideofilename)
    count = 0
    saved_frame_num = 0
    while True:
        success,image = vidcap.read()
        if not success:
            break
            #print ('Read a new frame: ', success)
        
        if count % interval == 0:
            fname = hexdigest + "_" + "{}.jpg".format("{0:05d}".format(count))
            cv2.imwrite(os.path.join(save_path, fname), image) # save frame as JPEG file
            saved_frame_num += 1
        count += 1
    print("from " + video_name + " {} images are extracted in {}.". format(saved_frame_num, save_path))
    return saved_frame_num

def video2frame_main(video_dir, frame_dir, frame_interval):
    total_saved_num = 0

    for video in os.listdir(video_dir):
        total_saved_num += video2frame(os.path.join(video_dir, video), frame_dir, video.split('.')[0], frame_interval)

    print("Total saved frames are " + str(total_saved_num) + " frames.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--video_dir",
        type=str,
        )

    parser.add_argument(
        "--frame_dir",
        type=str,
        )

    parser.add_argument(
        "--frame_interval",
        type=int,
        )

    args = parser.parse_args()

    video2frame_main(args.video_dir, args.frame_dir, args.frame_interval)

    
    