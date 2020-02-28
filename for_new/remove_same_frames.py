# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import os
import shutil

def remove_same_frames_main(frame_dir, frame_save_dir, anno_dir, min_w_ratio, min_h_ratio, SSIM_thredhold):

    image_list = os.listdir(frame_dir)
    #print(type(image_list))

    standard_image_name = image_list[0]
    imageA = cv2.imread(os.path.join(frame_dir, standard_image_name))
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    image_list.remove(image_list[0])

    for image in image_list:
        imageB = cv2.imread(os.path.join(frame_dir, image))
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
    
        if score >= SSIM_thredhold:
            pass
            #os.remove(os.path.join(frame_dir, image))
        else:
            shutil.copy2(os.path.join(frame_dir, standard_image_name), os.path.join(frame_save_dir, standard_image_name))

            #print("SSIM: {}".format(score))
            thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            anno_f = open(os.path.join(anno_dir, standard_image_name.split('.')[0] + ".txt"),"w")

            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if h/grayA.shape[0] >= min_h_ratio and w/grayA.shape[1] >= min_w_ratio:
                    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    anno_text = str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n"
                    anno_f.write(anno_text)

            anno_f.close()

            standard_image_name = image
            imageA = cv2.imread(os.path.join(frame_dir, standard_image_name))
            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)

            # 맨 마지막의 기준 이미지 imageA는 버린다. 


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_frame_dir", required=True, type=str, help="frame directory")
    parser.add_argument("--frame_dir", type=str)
    parser.add_argument("--anno_dir", type=str, help="empty_annotation directory")
    parser.add_argument("--min_w_ratio", required=True, type=float, help="minimum width ratio of AoI")
    parser.add_argument("--min_h_ratio", required=True, type=float, help="minimum height ratio of AoI")
    parser.add_argument("--SSIM_thredhold", required=True, type=float)
    args = parser.parse_args()

    remove_same_frames_main(args.raw_frame_dir, args.frame_dir, args.anno_dir, args.min_w_ratio, args.min_h_ratio, args.SSIM_thredhold)
