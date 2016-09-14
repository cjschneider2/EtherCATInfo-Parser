# The `parser_top_level` function takes the EtherCATInfo XML files and
# parses out the relevant device profile information
def device_from_file(file_name, device_list):
    from objects.device import Device
    from objects.fmmu import Fmmu
    from objects.sm import Sm
    from utils import lookup_location_id
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_name)
    root = tree.getroot()
    # Setting the vendor_id for the devices in this file
    file_vendor_id = root.find('./Vendor/Id').text
    # `Device` (Optional 0..inf)
    for device in root.iter('Device'):
        dev = Device()
        # `Type` (Mandatory 1)
        #     Device identity incl. name, product code, revision no
        typ = device.find("Type")
        dev.typ = typ.text
        #     Vendor Specific vendor Identifier
        dev.vendor_id = file_vendor_id
        #     Vendor Specific product code
        dev.product_code = typ.get("ProductCode", "")
        #     Vendor Specific revision number
        dev.revision_no = typ.get("RevisionNo", "")
        #     All devices with the same combo of `ProductCode`
        #     && `RevisionNo` should write a serial number to `SerialNo`
        dev.serial_no = typ.get("SerialNo", "")
        #     Specifies if the product code should be equal to the eeprom
        #     value (default: "EQ"), or if it is not checked ("NONE")
        dev.check_product_code = typ.get("CheckProductCode", "EQ")
        # NOTE: Other `Type` values are currently ignored
        # `HideType` (Optional 0..inf)
        #     Contains revision numbers of devices which should not be
        #     displayed in configuration tools...
        # NOTE: values `ProductCode` and `ProductRevision` are ignored
        for typ in device.findall("HideType"):
            dev.hide_type.append(typ.attrib.get("RevisionNo", ""))
            # `AlternativeType` (Optional 0..inf) (Vendor Specific)
            # `ProductCode` (Optional) (future use)
            # `RevisionNo`  (Optional) (future use)
            # `SubDevice` (Optional 0..inf)
            #     Used to display EtherCAT slaves built from more than one
            #     EtherCAT Slave Controller. 
            # `ProductCode` (Optional)
            # `RevisionNo` (Optional)
            # `PreviousDevice` (Optional)
            # `PreviousPortNo` (Optional)
            # `Name` (Mandatory 1..inf)
            #     Detailed name of the device
        for name in device.findall("Name"):
            lc_id_val = name.get("LcId", "")
            lc_id = lookup_location_id(lc_id_val)
            dev.name.append((lc_id, name.text))
            # `Comment` (Optional 0..inf)
            # `URL` (Optional 0..inf)
            #    Url pointing to the vendor's homepage where the ESI may
            #    be downloaded.
        for url in device.findall("URL"):
            lc_id_val = url.get("LcId", "")
            lc_id = lookup_location_id(lc_id_val)
            dev.url.append((lc_id, url.text))
            # `Info` (Optional 0..1)
            #    Additional information about the device
            #info = device.find("Info")
            #    # `Mailbox`
            #        # `Timeout`
            #            # `RequestTimeout`
            #mbox_request_timeout = info.find("./Mailbox/Timeout/RequestTimeout")
            #if mbox_request_timeout is not None:
            #    print "MailboxRequestTimeout =", mbox_request_timeout.text
            #            # `ResponseTimeout`
            #mbox_response_timeout = info.find("./Mailbox/Timeout/ResponseTimeout")
            #if mbox_response_timeout is not None:
            #    print "MailboxResponseTimeout =", mbox_response_timeout.text
            # `Electrical`
            # `VendorSpecific`
            # `StateMachine`
            # `Timeout`
            # `PreopTimeout`
            # `SafeopOpTimeout`
            # `BackToInitTimeout`
            # `BackToSafeopTimeout`
            # `GroupType` (Mandatory 1)
            #     Reference to a group which this element should be assigned
            #     to. The reference is defined in the element `Groups`.
        dev.group_type = device.find("GroupType").text
        # `Profile` (Optional 0..inf)
        #     Description of the used profile and object dictionary 
        #     including the data type definitions.
        # `ChannelInfo`
        # `Dictionary`
        # `DataTypes`
        # `DataType`
        # `Name`
        # `BaseType` (Optional)
        # `BitSize`
        # `ArrayInfo` (Optional)
        # `LBound`
        # `Elements`
        # `EnumInfo` (Optional)
        # `Text`
        # `Enum`
        # `SubItem` (Optional)
        # `SubIndex`
        # `Name`
        # `Type`
        # `BitSize`
        # `BitOffs`
        # `Flags`
        # `Access`
        # `Category`
        # `Backup`
        # `Setting`
        # `Object`
        # `Index`
        # `Name`
        # `Type`
        # `BitSize`
        # `Info`
        # `DefaultData`
        # `SubItem`
        # `Name`
        # `Info`
        # `DefaultData`
        # `Flags`
        # `Access`
        # `Category`
        # `DiagMessages`
        # `TextId`
        # `MessageText`
        # `Fmmu` (Optional 0..inf)
        #     Assigns FMMU to Sync-Manager; Definition of the FMMU usage.
        #     Allowed values:
        #         'Outputs'   -> used for RxPdo
        #         'Inputs'    -> used for TxPdo
        #         'MBoxState' -> used to poll the input Mailbox State (0x080D.0)
        # NOTE: Mandatory if more than one FMMU for the same direction is used
        #       to map data to non-constructive memory areas.
        # NOTE: Sm count starts at 0
        for fmmu in device.findall("Fmmu"):
            _fmmu = Fmmu()
            _fmmu.usage = fmmu.text
            dev.fmmu.append(_fmmu)
            # `Sm` (Optional 0..inf)
            #     Description of the Sync-Manager including start address and
            #     direction of transmission.
            #     Allowed values:
            #         'MBoxOut' -> Mailbox data (Master -> Slave)
            #         'MBoxIn'  -> Mailbox data (Slave  -> Master)
            #         'Outputs' -> Process data (Master -> Slave)
            #         'Inputs'  -> Process data (Slave  -> Master)
            #     The first Sync-Manager describes `SyncManager0` and then next
            #     `SyncManager1` and so on. If more than one Sync-Manager of the
            #     same direction and buffer mode are used the attribute Pdo@Su is
            #     mandatory.
        for sman in device.findall("Sm"):
            sm = Sm()
            dev.sm.append(sm)
            sm.typ = sman.text
            sm.min_size = sman.get("MinSize", "")
            sm.max_size = sman.get("MaxSize", "")
            # NOTE: Mandatory for Mailbox Sync-Manager
            #     Process Data Sync-Manager default length is based on the
            #     default PDO assignment in the Rx/Tx-Pdo entries.
            sm.default_size = sman.get("DefaultSize", "")
            # NOTE: If a Sync-Manager is configured for 3-buffer mode the
            #       occupied memory is 3x the length and should be considered
            #       in the calculation of the following Sync-Manager Address.
            sm.start_address = sman.get("StartAddress", "")
            sm.control_byte = sman.get("ControlByte", "")
            sm.enable = sman.get("Enable", "")
            #     if '1' then master should enable the Sync-Manager only in the
            #     operational state; if '0' the State machine is handled by host
            #     controller.
            # NOTE: True for devices with a digital I/O interface
            sm.op_only = sman.get("OpOnly", "")
            # `Su` (Optional 0..inf) (Perhaps mandatory, see above)
            #     Defines a timing context by defining different datagrams, possibly
            #     in different frames, which are identified by this string.
            # `SeparateSu` (Optional)
            # `SeparateFrame` (Optional)
            # `DependOnInputState` (Optional)
            # `FrameRepeatSupport` (Optional)
            # `RxPdo` (Optional 0..inf)
            #     Description of the output process data.
        for rxp in device.findall("RxPdo"):
            rx = RxPdo()
            rx.fixed = rxp.get("Fixed", "0")
            rx.sm = rxp.get("Sm", "-1")
            # NOTE: Skipping other RxPdo attributes
            # NOTE: RxPdo area : 0x1600 - 0x17FF
            rxp_index = rxp.find("Index")
            rxp_name = rxp.find("Name")
            rxp_exclude = rxp.find("Exclude")
            # `Index`
            if rxp_index is not None:
                rx.index = rxp_index.text
                # `Name`
            if rxp_name is not None:
                rx.name = rxp_name.text
                # `Exclude` (Optional)
            if rxp_exclude is not None:
                rx.exclude = rxp_exclude.text
                # `Entry`
            for item in rxp.findall("Entry"):
                ent = PdoEntry()
                ent_idx = item.find("Index")
                ent_subidx = item.find("SubIndex")
                ent_bitlen = item.find("BitLen")
                ent_name = item.find("Name")
                ent_datatype = item.find("DataType")
                # `Index`
                if ent_idx is not None:
                    ent.index = ent_idx.text
                    # `SubIndex`
                if ent_subidx is not None:
                    ent.sub_index = ent_subidx.text
                    # `BitLen`
                if ent_bitlen is not None:
                    ent.bit_len = ent_bitlen.text
                    # `Name`
                if ent_name is not None:
                    ent.name = ent_name.text
                    # `DataType`
                if ent_datatype is not None:
                    ent.data_type = ent_datatype.text
                    ent.sm = rx.sm
                    ent.direction = "RX"
                    rx.entry.append(ent)
                    dev.rx_pdo.append(rx)

        #     Description of the input process data
        for txp in device.findall("TxPdo"):
            tx = TxPdo()
            #    '0' -> Pdo Mapping can be changed
            #    '1' -> Pdo not configurable
            tx.fixed = txp.get("Fixed", "0")
            #    Default Sm for this PDO (included by default)
            tx.sm = txp.get("Sm", "-1")
            # NOTE: Skipping other RxPdo attributes
            # NOTE: TxPdo area : 0x1A00 - 0x1BFF
            txp_index = txp.find("Index")
            txp_name = txp.find("Name")
            txp_exclude = txp.find("Exclude")
            # `Index`
            if txp_index is not None:
                tx.index = txp_index.text
                # `Name`
            if txp_name is not None:
                tx.name = txp_name.text
                # `Exclude` (Optional)
            if txp_exclude is not None:
                tx.exclude = txp_exclude.text
                # `Entry`
            for item in txp.findall("Entry"):
                ent = PdoEntry()
                ent_idx = item.find("Index")
                ent_subidx = item.find("SubIndex")
                ent_bitlen = item.find("BitLen")
                ent_name = item.find("Name")
                ent_datatype = item.find("DataType")
                # `Index`
                if ent_idx is not None:
                    ent.index = ent_idx.text
                    # `SubIndex`
                if ent_subidx is not None:
                    ent.sub_index = ent_subidx.text
                    # `BitLen`
                if ent_bitlen is not None:
                    ent.bit_len = ent_bitlen.text
                    # `Name`
                if ent_name is not None:
                    ent.name = ent_name.text
                    # `DataType`
                if ent_datatype is not None:
                    ent.data_type = ent_datatype.text
                    ent.sm = tx.sm
                    ent.direction = "TX"
                    tx.entry.append(ent)
                    dev.tx_pdo.append(tx)
                    # `Mailbox` (Optional 0..1)
                    #     Description of available mailbox protocols
        mailbox = device.find("Mailbox")
        if mailbox is not None:
            # NOTE: if the object isn't present then it's not available in
            #       the slave device
            dev.mailbox = Mailbox()
            # `AoE`
            mbox_aoe = mailbox.find("AoE")
            if mbox_aoe is not None:
                dev.mailbox.aoe = mbox_aoe.attrib
                # `CoE`
            mbox_coe = mailbox.find("CoE")
            if mbox_coe is not None:
                dev.mailbox.coe = mbox_coe.attrib
                # `EoE`
            mbox_eoe = mailbox.find("EoE")
            if mbox_eoe is not None:
                dev.mailbox.eoe = mbox_eoe.attrib
                # `FoE`
            mbox_foe = mailbox.find("FoE")
            if mbox_foe is not None:
                dev.mailbox.foe = mbox_foe.attrib
                # `SoE`
            mbox_soe = mailbox.find("SoE")
            if mbox_soe is not None:
                dev.mailbox.soe = mbox_soe.attrib
                # `VoE`
            mbox_voe = mailbox.find("VoE")
            if mbox_voe is not None:
                dev.mailbox.voe = mbox_voe.attrib
                # `Dc` (Optional 0..1)
                #     Description of the following synchronization modes if available:
                #     {Freerun | Synchronous w/ Sm Event | Distributed Clocks}
        dc = device.find("Dc")
        if dc is not None:
            dev.dc = Dc()
            # `OpMode` (Optional 0..inf)
            for item in dc.findall("OpMode"):
                opmode = DcOpMode()
                dc_name = item.find("Name")
                dc_desc = item.find("Desc")
                dc_assign = item.find("AssignActivate")
                dc_cyc_syn0 = item.find("CycleTimeSync0")
                dc_sft_snc0 = item.find("ShiftTimeSync0")
                dc_cyc_syn1 = item.find("CycleTimeSync1")
                dc_sft_snc1 = item.find("ShiftTimeSync1")
                # `Name`
                if dc_name is not None:
                    opmode.name = dc_name.text
                    # `Desc`
                if dc_desc is not None:
                    opmode.desc = dc_desc.text
                    # `AssignActivate`
                if dc_assign is not None:
                    opmode.assign_activate = dc_assign.text
                    # `CycleTimeSync0`
                if dc_cyc_syn0 is not None:
                    opmode.cycle_time_sync_0 = dc_cyc_syn0.text
                    # `ShiftTimeSync0`
                if dc_sft_snc0 is not None:
                    opmode.shift_time_sync_0 = dc_sft_snc0.text
                    # `CycleTimeSync1`
                if dc_cyc_syn1 is not None:
                    opmode.cycle_time_sync_1 = dc_cyc_syn1.text
                    # `ShiftTimeSync1`
                if dc_sft_snc1 is not None:
                    opmode.shift_time_sync_1 = dc_sft_snc1.text
                    dev.dc.op_mode.append(opmode)
                    # `Slots` (Optional 0..??)
                    #     Defines the combination of possibilities of the modules which may
                    #     be used if the device supports Modular Device Profiles (ETG.5001)
                    #     The modules are defined in the `Modules` element
                    # `ESC` (Optional 0..??)
                    #     Initialization values of the EtherCAT Slave Controller Watchdog 
                    #     registers
                    # `Eeprom` (Optional 0..1)
                    # `AssignToPdi` : '0' -> access assigned to PDI during Init -> PreOp
                    #               : '1' -> Eeprom PDI access in all states except Init
                    # NOTE: Either `Eeprom@Data` is present or the other three are present.
                    # NOTE: EEPROM data format is little-endian
        if device.find("Eeprom") is not None:
            dev.eeprom = Eeprom()
            eeprom_data = device.find("./Eeprom/Data")
            eeprom_bytesize = device.find("./Eeprom/ByteSize")
            eeprom_configdata = device.find("./Eeprom/ConfigData")
            eeprom_bootstrap = device.find("./Eeprom/BootStrap")
            # `Data`
            #     Complete EEPROM data; length is implicit
            if eeprom_data is not None:
                dev.eeprom.data = eeprom_data.text
                # `ByteSize`
            if eeprom_bytesize is not None:

                dev.eeprom.byte_size = eeprom_bytesize.text
                # `ConfigData`
            if eeprom_configdata is not None:
                dev.eeprom.config_data = eeprom_configdata.text
                # `BootStrap`
            if eeprom_bootstrap is not None:
                dev.eeprom.bootstrap = eeprom_bootstrap.text
                #NOTE: There are three possibilities for images and if there is an
                #      image then only one of these can be chosen
                #     The hex binary data of a BMP file with dimensions of 16x14 pixels
                #     which may be shown by config tool.
                #NOTE: The color 0xFF00FF is transparent.
                # `Image16x14` (Optional 0..1)
                # `ImageFile16x14` (Optional 0..1)
                # `ImageData16x14` (Optional 0..1)
                # `VendorSpecific`
                #     Vendor Specific elements of `DeviceType`
                # Add our device to the list of devices
    device_list.append(dev)
