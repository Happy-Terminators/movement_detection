import os
import argparse


def match_img_anno_main(annotation_dir, image_dir):
    anno_files = list()
    print("annotation_num: " + str(len(os.listdir(annotation_dir))))
    for anno_file in os.listdir(annotation_dir):
        anno_files.append(anno_file)
    

    anno_files_names = list()
    for anno_file_name in anno_files:
        anno_files_names.append(anno_file_name.split('.')[0])


    img_files = list()
    print("image_num: " + str(len(os.listdir(image_dir))))
    for img_file in os.listdir(image_dir):
        img_files.append(img_file)


    img_files_names = list()
    for img_file_name in img_files:
        img_files_names.append(img_file_name.split('.')[0])

    mismatch_annos_names = list(set(anno_files_names) - set(img_files_names))
    mismatch_imgs_names = list(set(img_files_names) - set(anno_files_names))

    if len(mismatch_annos_names) > 0:
        for mismatch_anno in mismatch_annos_names:
            mismatch_index = anno_files_names.index(mismatch_anno)
            mismatch_anno_full_name = anno_files[mismatch_index]
            os.remove(os.path.join(annotation_dir, mismatch_anno_full_name))

        print('removed ' + str(len(mismatch_annos_names)) + " annotations")

    if len(mismatch_imgs_names) > 0:
        for mismatch_img in mismatch_imgs_names:
            mismatch_index = img_files_names.index(mismatch_img)
            mismatch_img_full_name = img_files[mismatch_index]
            os.remove(os.path.join(image_dir, mismatch_img_full_name))

        print('removed ' + str(len(mismatch_imgs_names)) + " images")

    if len(mismatch_annos_names) == 0 and len(mismatch_imgs_names) == 0:
        print("All data matches")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--anno_dir",
        type=str,
        )

    parser.add_argument(
        "--img_dir",
        type=str,
        )

    args = parser.parse_args()

    match_img_anno_main(args.anno_dir, args.img_dir)


