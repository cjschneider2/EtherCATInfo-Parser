#!/usr/bin/env python3

# DEFAULT_XML_DIR = "./xml_test_data"
DEFAULT_XML_DIR = "./xml_data"


# This function gets a list of the XML files from the input path
def get_xml_file_list(in_path):
    import fnmatch
    import os
    files = []
    for root, dirnames, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.xml"):
            files.append(os.path.join(root, filename))
    return files


def do_xml_2_sqlite():
    device_list = []
    import src.gen_sql as gen
    import os
    import src.parser as parse
    # Get a list of files
    files = get_xml_file_list(DEFAULT_XML_DIR)
    print("Found", len(files), "files.")
    # Parse XML files
    for f in files:
        print("File:", f)
        parse.device_from_file(f, device_list)
    print("Created", len(device_list), "device entries.")
    # Create SQLite3 Database
    print("Creating SQLite3 database here:", os.getcwd())
    gen.generate_sqlite3_db(device_list)


def do_xml_2_c_header():
    if argv[1] == "-C":
        # TODO: call the c stuff
        device_list = []


if __name__ == "__main__":
    from sys import argv
    argc = len(argv)
    # Do the default action of reading all the files in the `DEFAULT_XML_DIR`
    # and generating the SQLite3 database from the data
    if argc == 1:
        do_xml_2_sqlite()
    else:
        do_xml_2_c_header()
