import filecmp
import os
import hashlib
import shutil



def folders_sync(source, replica):
    """
    Sync two folders one-way
    
    Parameters:
        source (str): Path of the source folder
        replica (str): Path of the replica folder

    """
    cmp_dir = filecmp.dircmp(source, replica)
    
    for file in cmp_dir.left_only:
        create_file(file, source, replica)

    for file in cmp_dir.right_only:
        delete_file(file, source, replica)

    if cmp_dir.common_files:
        check_common_files(cmp_dir.common_files, source, replica)


    for common_dir in cmp_dir.common_dirs:
        dir_source = os.path.join(source, common_dir)
        dir_replica = os.path.join(replica, common_dir)
        folders_sync(dir_source, dir_replica)

def create_file(file, source, replica):
    """
    Create a file/subdirectory from source folder to replica folder
    
    Parameters:
        file (str): File name
        source (str): Path of the source folder
        replica (str): Path of the replica folder

    """
    file_path = os.path.join(source, file)
    dest_file_path = os.path.join(replica, file)
    try:
        if os.path.isdir(file_path):
            shutil.copytree(file_path, dest_file_path)
        else:
            shutil.copy2(file_path, dest_file_path)

    except Exception as e:
            print(f"Error copying file: {file}")


def delete_file(file, replica):
    """
    Delete a file/subdirectory from replica folder
    
    Parameters:
        file (str): File name
        replica (str): Path of the replica folder

    """
    file_path = os.path.join(replica, file)
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.unlink(file_path)
    except Exception as e:
            print(f"Error deleting file: {file_path}")


def check_common_files(common_files, source, replica):
    """
    Compare content of common files between source and replica folders
    
    Parameters:
        common_files (list): List of names of common files
        source (str): Path of the source folder
        replica (str): Path of the replica folder

    """
    for common_file in common_files:
        print(common_file)
        file_source = os.path.join(source, common_file)
        file_replica = os.path.join(replica, common_file)

        md5_source = get_md5(file_source)
        md5_replica = get_md5(file_replica)

        if md5_source != md5_replica:
            create_file(common_file, source, replica)
 

def get_md5(file):
    md5 = hashlib.md5()
    with open(file, 'rb') as file:
        md5.update(file.read())
    return md5.hexdigest()


