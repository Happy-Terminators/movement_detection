import os
import argparse
import shutil
from lxml import etree

def change_main(image_dir, anno_dir, keyword_image_dir):
   
    for index, image_file in enumerate(os.listdir(image_dir)):
        new_filename = keyword_image_dir + "_" + str(index) + '.jpg'
        os.rename(os.path.join(image_dir, image_file), os.path.join(image_dir, new_filename))

    for index, anno_file in enumerate(os.listdir(anno_dir)):
        tree = etree.parse(os.path.join(anno_dir, anno_file))
        root = tree.getroot()
 
        # Get data
        kids = root.getchildren()
 
        for child in kids:
            if child.tag == "filename":
                img_file_name = child.text
                new_img_file_name = keyword_image_dir + "_" + str(index) + '.jpg'

                f = open(os.path.join(anno_dir, anno_file), 'r')
                all_string = f.read()
                f.close()
                
                f = open(os.path.join(anno_dir, anno_file), 'w')
                f.write(all_string.replace(img_file_name, new_img_file_name))
                f.close()

                #print("changed names")

        new_filename = keyword_image_dir + "_" + str(index) + '.xml'
        os.rename(os.path.join(anno_dir, anno_file), os.path.join(anno_dir, new_filename))
        

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
        "--keyword",
        type=str,
        )

    args = parser.parse_args()

    change_main(args.image_dir, args.anno_dir, args.keyword)
