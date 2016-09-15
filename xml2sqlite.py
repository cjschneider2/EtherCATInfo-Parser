#!/usr/bin/env python3

#DEFAULT_XML_DIR = "./xml_data"
DEFAULT_XML_DIR = "./xml_test_data"

# This function gets a list of the XML files from the input path
def get_xml_file_list(in_path):
    import fnmatch
    import os
    files = []
    for root, dirnames, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.xml"):
            files.append(os.path.join(root, filename))
    return files

if __name__ == "__main__":
    import src.parser as parse
    from sys import argv
    argc = len(argv)
    # Do the default action of reading all the files in the `DEFAULT_XML_DIR`
    # and generating the SQLite3 database from the data
    if argc == 1:
        device_list = []
        # Get a list of files
        files = get_xml_file_list(DEFAULT_XML_DIR)
        print "Found", len(files), "files."
        # Parse XML files
        for f in files:
            parse.device_from_file(f, device_list)
        # Create SQLite3 Database
        print "Created", len(device_list), "device entries."
    else:
        if argv[1] == "-C":
            # do the c stuff
            device_list = []
