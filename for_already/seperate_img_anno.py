import os
import argparse
import shutil

def separate_main(source_dir, image_dir, anno_dir):
    for source_file in os.listdir(source_dir):
        fname, ext = os.path.splitext(source_file)
        if ext == ".txt" or ext == ".xml":
            shutil.move(os.path.join(source_dir, source_file), os.path.join(anno_dir, img))
        else:
            shutil.move(os.path.join(source_dir, source_file), os.path.join(image_dir, img))

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
        "--source_dir",
        type=str,
        )

    args = parser.parse_args()

    separate_main(args.source_dir, args.image_dir, args.anno_dir)