import os
import shutil

def copy_all_contents_to_destination(source, destination):
    
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)

    
    if os.path.isfile(source):
        print(f"source: {source}")
        print(f"destination: {destination}")
        shutil.copy(source, destination)
    else:
        print(f"List of directories {os.listdir(source)}")
        current_obj = os.listdir(source)[0]
        new_path = os.path.join(source, current_obj)
        os.mkdir(os.path.join(destination, current_obj))
        print(f"new path: {new_path}")
        
        copy_all_contents_to_destination(new_path, destination)

    

    


copy_all_contents_to_destination("static", "public")




