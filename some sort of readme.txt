###### WARNING ###### WARNING ###### WARNING ######
1)	Moving files

	This program will move all files in given directory except:
	- subsequent directories
	- files in subsequent directories
	
	1.1 Origin directory
		The program will do nothing if the given "from" directory 
		doesn't exist or doesn't contain any files.
		The origin directory, and any empty parent directories,
		will be removed if no files remain in any child or parent 
		directory after execution.
	
	1.2 Destination directory
		You can create a path to move the files that doesn't exist yet, 
		thought you can't create new folders with the directory chooser.
		To create such a path, simply specify it in the textfield.
	
2)	Renaming files

	This program will rename all moved files to the chosen pattern.
	
	
3)	Options

	3.4 Smart Digits
	The Smart Digits are not smart enough to keep track with the whole batch.
	This option checks the number of files in the given directory and choses
	the appropriate number of leading zeroes. This does not include the files
	at the destination folder.
