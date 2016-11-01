# -------------------------------------------------------------------------- #
# SQLite3 generator Functions ---------------------------------------------- #
# -------------------------------------------------------------------------- #


def generate_sqlite3_db(devices):
    import src.utils as utils
    import sqlite3
    import pickle
    import hashlib
    # Debug Info
    print("Using sqlite3 py-module version:", sqlite3.version)
    print("Using sqlite3 c-library version:", sqlite3.sqlite_version)
    # Generate Version information for the DB
    db_version_no = hashlib.md5(pickle.dumps(devices)).hexdigest()
    print("Version String : ", db_version_no)
    # Generate the SQLite DB
    # con = sqlite3.connect(":memory:") # In memory db for testing
    con = sqlite3.connect("ecat_devices.sqlite")  # DB-File
    cur = con.cursor()
    # Drop the tables ( if they already exist )
    cur.execute("DROP TABLE IF EXISTS version")
    cur.execute("DROP TABLE IF EXISTS devices")
    cur.execute("DROP TABLE IF EXISTS pdos")
    # Create the new tables
    print("Creating database tables")
    dev_id = 1
    pdo_id = 1
    # add the Version table
    cur.execute("CREATE TABLE version \
    (ver_id INTEGER_PRIMARY KEY, version STRING)")
    cur.execute("INSERT INTO version VALUES (?, ?)", (1, db_version_no))
    # create Device and PDO tables
    cur.execute("CREATE TABLE devices \
    (dev_id INTEGER PRIMARY KEY, \
    vendor_id INTEGER, \
    product_code INTEGER, \
    revision INTEGER, type)")
    cur.execute("CREATE TABLE pdos \
    (pdo_id INTEGER PRIMARY KEY, \
    db_idx INTEGER, \
    set_idx INTEGER, \
    pdo_idx INTEGER,\
    pdo_subidx INTEGER, \
    bit_len INTEGER, \
    pdo_dir, \
    sync_man INTEGER, \
    name, data_type)")
    for dev in devices:
        # Here, we need to make sure that the numbers are in their correct
        # formats before we insert them into the database
        _hex = utils.strip_pound_hex(dev.vendor_id)
        if (_hex == ''):
            continue
        v_id = int(_hex, 16)

        _hex = utils.strip_pound_hex(dev.product_code)
        if (_hex == ''):
            continue
        p_code = int(_hex, 16)

        _hex = utils.strip_pound_hex(dev.revision_no)
        if (_hex == ''):
            continue
        r_no = int(_hex, 16)

        # Add device info into device table
        cur.execute("insert into devices values (?, ?, ?, ?, ?)",
                    (dev_id,
                     v_id,
                     p_code,
                     r_no,
                     dev.typ))
        # Add pdos to the pdo table
        # print "Adding PDOs for device:"
        pdos = []
        # TxPdo entries
        for pdo in dev.tx_pdo:
            pdos.append(pdo)
        # RxPdo entries
        for pdo in dev.rx_pdo:
            pdos.append(pdo)
        # create the output
        for pdo in pdos:
            try:
                set_index = int(utils.strip_pound_hex(pdo.index), 16)
            except:
                print("ERROR: Missing set_index:", dev.name[0],
                      " >> ", pdo.index)
                set_index = int(0)
            for entry in pdo.entry:
                # skip 'empty' addresses or indexes
                if entry.index == "#x0" \
                   or entry.index == "0" \
                   or entry.sub_index == "":
                    continue
                # skip entries without a defined Sync-Manager
                if entry.sm == "-1":
                    continue
                # add the pdo entry to the list
                # Try to convert the subindex as an integer and if that fails
                # we will try to interpret it as a hex value.
                try:
                    _sub_idx = int(entry.sub_index)
                except ValueError:
                    _sub_idx = int(utils.strip_pound_hex(entry.sub_index), 16)
                cur.execute(
                    "insert into pdos values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (pdo_id,
                     dev_id,
                     set_index,
                     int(utils.strip_pound_hex(entry.index), 16),
                     _sub_idx,
                     entry.bit_len,
                     entry.direction,
                     int(entry.sm),
                     entry.name,
                     entry.data_type))
                pdo_id += 1
        # increment our db-index after we're done with the current device
        dev_id += 1
    print("\n", "Selecting inserted data")
    cur.execute("select * from devices")
    rows = cur.fetchall()
    print("Number of Entries Found:", len(rows))
    con.commit()
    con.close()
