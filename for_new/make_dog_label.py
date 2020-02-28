from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os
import argparse

def make_dog_label_main(anno_dir, image_dir, new_anno_dir):
    imagenet_labels = np.array(open(os.path.join('for_new\\txts\\labels','ImageNetLabels.txt')).read().splitlines())
    dog_labels = np.array(open(os.path.join('for_new\\txts\\labels','dog_label.txt')).read().splitlines())

    #print(cudaGetDevice())
    #print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))


    #with tf.device("/gpu:0"):
    pretrained_model = tf.keras.applications.MobileNet()

    

    for image in os.listdir(image_dir):
        new_anno = ''

        imageA = cv2.imread(os.path.join(image_dir, image))
        cvt_image =  cv2.cvtColor(imageA, cv2.COLOR_BGR2RGB)

        annotations = np.array(open(os.path.join(anno_dir, image.split('.')[0] + '.txt')).read().splitlines())
        #print(annotations)
        if len(annotations) > 0 :
            for annotation in annotations:
                #print(annotation)
                anno_elements = annotation.split(" ")
                x = float(anno_elements[0])
                y = float(anno_elements[1])
                w = float(anno_elements[2])
                h = float(anno_elements[3])

                roi = cvt_image[int(y):int(y+h), int(x):int(x+w)]
                bbox_image = roi

                #cv2.imshow("src", cvt_image)
                #cv2.imshow("dst", bbox_image)
                #cv2.waitKey(600)

                im_pil = Image.fromarray(bbox_image)

                # resize the array (image) then PIL image
                im_resized = im_pil.resize((224, 224))

                #with tf.device("/gpu:0"):
                x_ = tf.keras.preprocessing.image.img_to_array(im_resized)
                x_ = tf.keras.applications.mobilenet.preprocess_input(x_[tf.newaxis,...])
    
                result_before_save = pretrained_model(x_)

                #print()
                decoded = imagenet_labels[np.argsort(result_before_save)[0,::-1][:5]+1]
                #print("저장 전 결과:\n", decoded)
                if decoded[0] in dog_labels:
                    new_anno = new_anno + decoded[0] + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n"
                    #print(new_anno)

        if len(new_anno) > 0:
            new_anno_f = open(os.path.join(new_anno_dir, image.split('.')[0] + '.txt'), 'w')

            new_anno_f.write(new_anno)
        
            new_anno_f.close()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--anno_dir",
        type=str,
        )

    parser.add_argument(
        "--image_dir",
        type=str,
        )

    parser.add_argument(
        "--new_anno_dir",
        type=str,
        )

    args = parser.parse_args()

    make_dog_label_main(args.anno_dir, args.image_dir, args.new_anno_dir)

    