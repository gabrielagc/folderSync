# folderSync
Program that synchronizes two folders: source and replica.

The program receives as arguments the folder paths, synchronization interval and log file path in the following order:

`python3 main.py <source path> <replica path> <time interval> <log file path>`

In case replica folder does not exist, it is created. As well, it checks time interval is a positive value to avoid errors in the program.

The library `filecmp` is used to compared both folders, getting files/subdirectories only belonging to source folder and only belonging to replica folder, as common files and directories between both folders.

The library `hashlib` is used to get the MD5 hash of a file to compare the content of the file in both folders and identify if it was modified.