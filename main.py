import filecmp
import os
import hashlib
import shutil
import time
import argparse
import logging

def run(source, replica, time_interval, log_file):
    """
    Run script periodically and log is initialized
    
    Parameters:
        source (str): Source folder path
        replica (str): Replica folder path
        time_interval (int): Time interval the script is running
        log_file (str): Log file path
    """

    if not os.path.exists(source):
        raise argparse.ArgumentError(None, "Source folder does not exist")
    if not os.path.exists(replica):
        os.makedirs(replica) #Create replica folder in case it does not exist
    if time_interval <= 0:
        raise argparse.ArgumentError(None, "Time interval must be a positive value")

    logging.basicConfig(
    filename=log_file,  
    level=logging.INFO,               
    format='%(asctime)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'      
    )
    logging.info(f"Starting sync: Source folder: {source} Replica folder: {replica} Time interval: {time_interval}")
    while (True):
        folders_sync(source, replica)
        time.sleep(time_interval)

def folders_sync(source, replica):
    """
    Sync two folders one-way
    
    Parameters:
        source (str): Source folder path
        replica (str): Replica folder path

    """
    cmp_dir = filecmp.dircmp(source, replica)
    
    #Get files/subdirectories only existing in source folder
    for file in cmp_dir.left_only:
        copy_file(file, source, replica)

    #Get files/subdirectories only existing in replica folder
    for file in cmp_dir.right_only:
        delete_file(file, replica)

    #Get files in common
    if cmp_dir.common_files:
        check_common_files(cmp_dir.common_files, source, replica)

    #Continue checking directories in both folders
    for common_dir in cmp_dir.common_dirs:
        dir_source = os.path.join(source, common_dir)
        dir_replica = os.path.join(replica, common_dir)
        folders_sync(dir_source, dir_replica)

def copy_file(file, source, replica):
    """
    Create/copy a file/subdirectory from source folder to replica folder
    
    Parameters:
        file (str): File name
        source (str): Path of the source folder
        replica (str): Path of the replica folder

    """
    file_path = os.path.join(source, file)
    dest_file_path = os.path.join(replica, file)
    method = "updated" if os.path.exists(dest_file_path) else "created"
    try:
        #Check if it is a directory
        if os.path.isdir(file_path):
            shutil.copytree(file_path, dest_file_path)
        else:
            shutil.copy2(file_path, dest_file_path)
        msg = f"The file: {file_path} was {method}"
        logging.info(msg)
        print(msg)

    except Exception as e:
            logging.error(f"Error copying file: {file}")

def delete_file(file, replica):
    """
    Delete a file/subdirectory from replica folder
    
    Parameters:
        file (str): File name
        replica (str): Path of the replica folder

    """
    file_path = os.path.join(replica, file)
    try:
        #Check if it is a directory
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.unlink(file_path)
        
        msg = f"The file: {file_path} was deleted"
        logging.info(msg)
        print(msg)
    except Exception as e:
            logging.error(f"Error deleting file: {file_path}")

def check_common_files(common_files, source, replica):
    """
    Compare content of common files between source and replica folders
    
    Parameters:
        common_files (list): List of common files
        source (str): Path of the source folder
        replica (str): Path of the replica folder

    """
    for common_file in common_files:
        file_source = os.path.join(source, common_file)
        file_replica = os.path.join(replica, common_file)

        md5_source = get_md5(file_source)
        md5_replica = get_md5(file_replica)

        if md5_source != md5_replica:
            copy_file(common_file, source, replica)
        else:
            logging.info(f"The file: {file_source} is synchronized")

def get_md5(file):
    """
    Calculate md5 hash of a file
    
    Parameters:
        file (str): File path

    """
    md5 = hashlib.md5()
    with open(file, 'rb') as file:
        md5.update(file.read())
    return md5.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Synchronization of two folders (source and replica)")

    parser.add_argument("source", type=str, help="Source folder path")
    parser.add_argument("replica", type=str, help="Replica folder path")
    parser.add_argument("time_interval", type=int, help="Synchronization interval(seconds)")
    parser.add_argument("log_file", type=str, help="Log file path")


    args = parser.parse_args()
    
    run(args.source, args.replica, args.time_interval, args.log_file)



