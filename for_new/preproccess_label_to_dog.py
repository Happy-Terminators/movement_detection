import os
import argparse

parser = argparse.ArgumentParser(description = 'parser for preproccess')
parser.add_argument(
    "--anno_dir",
    type=str,
    )

parser.add_argument(
    "--result_dir",
    type=str,
    )

parser.add_argument(
    "--source_labels",
    type=str,
    )

parser.add_argument(
    "--dest_label",
    type=str,
    )

args = parser.parse_args()

annotation_dir = args.anno_dir #os.path.join(os.getcwd(), 'annotations')
preproccessed_dir = args.result_dir #os.path.join(os.getcwd(), 'after')
annotation_labels = args.source_labels.split(',')
dest_label = args.dest_label
#print(annotation_labels)


filenames = os.listdir(annotation_dir)
for filename in filenames:
    annotation_full_filename = os.path.join(annotation_dir, filename)
    preproccessed_full_filename = os.path.join(preproccessed_dir, filename)
    #print(preproccessed_full_filename)

    anno_f = open(annotation_full_filename, 'r')
    data = anno_f.read()
    anno_f.close()

    for label in annotation_labels:
        data = data.replace(label, dest_label)

    prepro_f = open(preproccessed_full_filename, 'w')
    prepro_f.write(data)
    prepro_f.close()


print()
print('----------------------------------------------------')
print(str(len(filenames)) + " annotations changed. ")
print(str(annotation_labels) + "->" + dest_label)
print('----------------------------------------------------')

    


