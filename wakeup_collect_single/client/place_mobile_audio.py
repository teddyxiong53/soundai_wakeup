import glob
import os, os.path
import sys
import shutil

txt_files = glob.glob("./phone/*.txt")
pcm_files = glob.glob("./phone/*.pcm")

target_dirs = glob.glob("./audio_files/*")



def copy_files(suffix):
    if suffix == "pcm":
        files = txt_files
    else:
        files = pcm_files
    skip_num = len("./phone/")
    skip = len("./audio_files/")
    for f in files:
        id = f[skip_num: skip_num+3]
        filename = f[skip_num:]
        # print(filename)
        # print(id)
        # 找到对应的目录
        for d in target_dirs:
            id_dir = d[skip: skip+3]
            # print(id_dir)
            if id == id_dir:
                #print("found id {} target dir".format(id))
                #找到了目录，就把对应的文件拷贝到下面。
                if os.path.exists(f) and os.path.exists(d):
                    dst = "{}/mobile/{}".format(d, filename)
                    shutil.copyfile(f, dst)
                    print("copy {} to {}".format(f, dst))

copy_files("txt")
copy_files("pcm")
