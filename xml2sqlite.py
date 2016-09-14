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
    from src import *
    # Get a list of files
    files = get_xml_file_list(DEFAULT_XML_DIR)
    print "Found", len(files), "files."
    # Parse
