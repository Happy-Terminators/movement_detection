import os
import argparse
import shutil

parser = argparse.ArgumentParser(description = 'parser for preproccess')
parser.add_argument(
    "--cfg_dir",
    type=str,
    )

parser.add_argument(
    "--weight_dir",
    type=str,
    )

parser.add_argument(
    "--video_dir",
    type=str,
    )

args = parser.parse_args()

cfg_directory = args.cfg_dir #os.path.join(os.getcwd(), 'annotations')
weight_directory = args.weight_dir #os.path.join(os.getcwd(), 'after')

cfg_file_names = os.listdir(cfg_directory)
for cfg_file_name in cfg_file_names:
    cfg_full_file_name = os.path.join(cfg_directory, cfg_file_name)
    cfg_short_name = cfg_file_name.split('.')[0]

    weights_file_names = os.listdir(weight_directory)
    for weights_file_name in weights_file_names:
        weight_full_file_name = os.path.join(weight_directory, weights_file_name)
        weights_short_name = weights_file_name.split('.')[0]

        os.system("flow --model " + cfg_full_file_name + " --load " + weight_full_file_name + " --demo data/test_dog.mp4 --saveVideo True --gpu 1.0 ")

        if os.path.isfile("video.avi"):
            new_filename = "video.avi".replace("video", cfg_short_name + "_" + weights_short_name) 
            os.rename("video.avi", new_filename)
            shutil.move(new_filename, args.video_dir)






        