import os
import shutil


def copy_all_contents_to_destination(source, destination):
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)

    names = []
    if not os.path.isfile(source):
        names = os.listdir(source)
        print(f"File contents: {names}")

    for name in names:
        src_path = os.path.join(source, name)
        dest_path = os.path.join(destination, name)
        if os.path.isfile(name):
            shutil.copy(src_path, dest_path)
        else:
            if not os.path.exists(os.path.join(destination, name)):
                copy_all_contents_to_destination(src_path, dest_path)


copy_all_contents_to_destination("static", "public")
