import os, shutil

def copy_dir(src, dst):
    files = os.listdir(src)
    for file in files:
        src_path = os.path.join(src, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            dst_path = os.path.join(dst, file)
            os.mkdir(dst_path)
            copy_dir(src_path, dst_path)

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_dir("static", "public")

main()