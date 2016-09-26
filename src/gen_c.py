# -------------------------------------------------------------------------- #
# C header generator Functions --------------------------------------------- #
# -------------------------------------------------------------------------- #

def gen_all_file(devices):
    import glob
    # find our files
    file_paths = glob.glob("./Beckhoff_EtherCAT_XML/*.xml")
    # run the parser
    for path in file_paths:
        parser_top_level(path, devices)
    # run the generator
    _hdr = generate_header()
    _dev = generate_device_list(devices)
    return (_hdr, _dev)

def gen_test_file(devices):
    parser_top_level("./file.xml", devices)
    parser_top_level("./file1.xml", devices)
    # run the generator
    _hdr = generate_header()
    _dev = generate_device_list(devices)
    return (_hdr, _dev)

def generate_c_headers():
    devices = []
    #(hdr, devs) = gen_all_file(devices)
    (hdr, devs) = gen_test_file(devices)
    # print out the number of devices found
    print "Generated configuration for", len(devices), "devices"
    # Test the file to see if it can compile
    test_header(hdr, devs)

# -------------------------------------------------------------------------- #
# Devices -> File as string functions -------------------------------------- #
# -------------------------------------------------------------------------- #

# This is a test function to print out the c_file to the console for
# development. This may also be used for piping into an output file.
def c_file_as_str_from_devices(devices):
    output_lines = []
    # actual lines we're storing. We need to save them before hand to make sure
    # that the Id we assign to the device is consistent throughout the struts.
    bk_vendor_id = "0x00000002" # TODO: This should be read from the file
    device_lines = []
    fmmu_lines = []
    sm_lines = []
    rx_lines = []
    tx_lines = []
    pdo_entry_info = []
    pdo_string_map = dict()
    pdo_string_lst = []
    pdo_string_idx = 0
    entry_str_idx = 0
    idx = 0
    for dev in devices:
        pc  = parse_hex(dev.product_code)
        rev = parse_hex(dev.revision_no)
        # -- DEVICE ENTRIES
        # if the device doesn't have a product code / revision number we'll
        # skip it as these won't be able to be read from the driver anyways
        if pc == "":
            continue
        # create the actual device data entry
        fstr = '{{ {:>4}, {:>10}, {:>10}, {:>10}, "{}" }}'
        device_lines.append(fstr.format(idx, bk_vendor_id, pc, rev, dev.typ))
        # -- /DEVICE ENTRIES

        # -- PDO ENTRIES
        pdos = []
        # TxPdo entries
        for pdo in dev.tx_pdo:
            pdos.append(pdo)
        # RxPdo entries
        for pdo in dev.rx_pdo:
            pdos.append(pdo)
        # create the output
        for pdo in pdos:
            for entry in pdo.entry:
                # skip 'empty' addresses or indexes
                if entry.index == "#x0" or entry.index == "0" or entry.sub_index == "":
                    continue
                # skip entries without a defined Sync-Manager
                if entry.sm == "-1":
                    continue
                # calculate the string db entry
                if entry.name not in pdo_string_map:
                    pdo_string_map[entry.name] = pdo_string_idx;
                    entry_str_idx = pdo_string_idx
                    pdo_string_idx = pdo_string_idx + 1
                else:
                    entry_str_idx = pdo_string_map[entry.name]
                # add the pdo entry to the list
                pdo_entry_info.append(
                    '{{ {:>4}, {:>6}, {:>2}, {:>3}, {:2}, {:>2}, {:>2}, {} }}'
                    .format(
                    str(idx),
                    parse_hex(entry.index),
                    parse_hex(entry.sub_index),
                    entry.bit_len,
                    entry.direction,
                    entry.sm,
                    entry_str_idx,
                    parse_bdt(entry.data_type)))
        # -- /PDO ENTRIES
        #
        idx += 1
    # Collect the string db entries
    string_db = dict()
    for (k, v) in pdo_string_map.iteritems():
        if not string_db.has_key(v):
            string_db[v] = k
    for (k, v) in string_db.iteritems():
        pdo_string_lst.append('{{ {}, "{}" }}'.format(k, v))
    # -- WRITE OUT DATA
    # HEADER
    output_lines.append(device_list_header)
    # DEVICES
    output_lines.append("""struct ec_device ec_devices[] = {\n""")
    output_lines.append(
        """/* {db_index, vendor_id, prod_code, rev_num, type_str} */\n""")
    data_len = len(device_lines)
    for i, line in enumerate(device_lines):
        if i == (data_len - 1):
            output_lines.append("    {}".format(line))
        else:
            output_lines.append("    {},\n".format(line))
    output_lines.append("""\n};\n\n""")
    # PDOs
    output_lines.append("""struct pdo_entry_info pdo_entries[] = {\n""")
    output_lines.append(
        """/* {db_idx, idx, sub-idx, bit_len, dir, SM, name_idx} */\n""")
    pdo_len = len(pdo_entry_info)
    for i, line in enumerate(pdo_entry_info):
        if i == (pdo_len - 1):
            output_lines.append("    {}".format(line))
        else:
            output_lines.append("    {},\n".format(line))
    output_lines.append("""\n};\n\n""")
    # PDO -> String db
    output_lines.append("""struct pdo_string_entry pdo_string_db[] = {\n""")
    output_lines.append("""/* {name_idx, pdo_description_string} */\n""")
    pdo_e_len = len(pdo_string_lst)
    for i, line in enumerate(pdo_string_lst):
        if i == (pdo_e_len - 1):
            output_lines.append("    {}".format(line))
        else:
            output_lines.append("    {},\n".format(line))
    output_lines.append("""\n};\n\n""")
    # FOOTER
    output_lines.append(device_list_footer)
    return output_lines

def c_header_str():
    import c_templates as TPL
    output_lines = []
    # STRUCTS
    output_lines.append(TPL.device_info_header)
    output_lines.append(TPL.header_device_struct_defn)
    output_lines.append(TPL.header_pdo_entry_info)
    output_lines.append(TPL.device_info_footer)
    return output_lines

# -------------------------------------------------------------------------- #
# Test Functions ----------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def test_header(_hdr, _dev):
    from subprocess import check_output
    import c_templates as TPL
    # Create the C file
    with open("./build/_test.c", "w+") as c_file:
        c_file.write(TPL.test_c_main_txt)
    # Create the Device Header file
    with open("./build/ethercat_device_info.h", "w+") as h_file:
        h_file.writelines(_hdr)
    # Create the Device List Header file
    with open("./build/ethercat_device_list.h", "w+") as h_file:
        h_file.writelines(_dev)
    # Run the complier & read the output
    output = check_output(["gcc", "-std=c99", "_test.c"])
    # compare the output
    return

def test_program():
    from subprocess import check_output
    # Run the complier & read the output
    output = check_output(["gcc", "-std=c99","-Wall", "build/_test.c"])
    # TODO: compare the output
    return
