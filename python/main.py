# Class stubs for programmatic object creation -------------------------------
class Device(object):
    hide_type = []
    rx_pdo = []
    tx_pdo = []
    pass

class Eeprom(object):
    pass

class Dc(object):
    op_mode = []
    pass

class DcOpMode(object):
    pass

class TxPdo(object):
    entry = []
    pass

class RxPdo(object):
    entry = []
    pass

class PdoEntry(object):
    pass

class Mailbox(object):
    pass

# Utility functions ---------------------------------------------------------- 
def parse_location_id(val):
    if val is "1033":
        return "En"
    elif val is "1031":
        return "De"
    else:
        return "Unknown"

# parser functions ----------------------------------------------------------- 
def parser_top_level(file_name):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_name)
    root = tree.getroot()
    devices = []
    # `Device` (Optional 0..inf)
    for device in root.iter('Device'):
        dev = Device()
        # `Type` (Mandatory 1)
        #     Device identity incl. name, product code, revision no
        typ = device.find("Type")
        dev.typ = typ.text
        print "ProductType =", typ.text
        for item in typ.attrib.items():
            print item[0], "=", item[1]
        # `HideType` (Optional 0..inf)
        #     Contains revision numbers of devices which should not be 
        #     displayed in configuration tools...
        for typ in device.findall("HideType"):
            dev.hide_type.append(typ.attrib.get("RevisionNo"))
        # `AlternativeType` (Optional 0..inf) (Vendor Specific)
        # `SubDevice` (Optional 0..inf)
        #     Used to display EtherCAT slaves built from more than one EtherCAT
        #     Slave Controller. Contains `ProductCode` and `RevisionNo` of the
        #     `SubDevice`'s
        # `Name` (Mandatory 1..inf)
        #     Detailed name of the device
        for name in device.findall("Name"):
            lc_id_val = name.get("LcId", "")
            lc_id = parse_location_id(lc_id_val)
            print "Name" + lc_id + " =", name.text
        # `Comment` (Optional 0..inf)
        # `URL` (Optional 0..inf)
        #    Url pointing to the vendor's homepage where the ESI may be downloaded
        for url in device.findall("URL"):
            lc_id_val = url.get("LcId", "")
            lc_id = parse_location_id(lc_id_val)
            print "Url" + lc_id + " =", url.text
        # `Info` (Optional 0..1)
        #    Additional information about the device
        info = device.find("Info")
            # `Mailbox`
                # `Timeout`
                    # `RequestTimeout`
        mbox_request_timeout = info.find("./Mailbox/Timeout/RequestTimeout")
        if mbox_request_timeout is not None:
            print "MailboxRequestTimeout =", mbox_request_timeout.text
                    # `ResponseTimeout`
        mbox_response_timeout = info.find("./Mailbox/Timeout/ResponseTimeout")
        if mbox_response_timeout is not None:
            print "MailboxResponseTimeout =", mbox_response_timeout.text
            # `Electrical`
            # `VendorSpecific`
            # `StateMachine`
                # `Timeout`
                    # `PreopTimeout`
                    # `SafeopOpTimeout`
                    # `BackToInitTimeout`
                    # `BackToSafeopTimeout`
        # `GroupType` (Mandatory 1)
        #     Reference to a group which this element should be assigned to.
        #     The reference is defined in the element `Groups`.
        group_type = device.find("GroupType")
        print "GroupType =", group_type.text
        # `Profile` (Optional 0..inf)
        #     Description of the used profile and object dictionary including
        #     the data type definitions.
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
        #     Definition of the FMMU usage.
        #     Allowed values:
        #         'Outputs'   -> used for RxPdo
        #         'Inputs'    -> used for TxPdo
        #         'MBoxState' -> used to poll the input Mailbox State (0x080D.0)
        for fmmu in device.findall("Fmmu"):
            print "FmmuTypeAvailable =", fmmu.text
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
        for sm in device.findall("Sm"):
            print "SmTypeAvailable =", sm.text
            for item in sm.items():
                print " |-", item[0], "=", item[1]
        # `Su` (Optional 0..inf) (Perhaps mandatory, see above)
        #     Defines a timing context by defining different datagrams, possibly
        #     in different frames, which are identified by this string.
        # `RxPdo` (Optional 0..inf)
        #     Description of the output process data.
        for rxp in device.findall("RxPdo"):
            print "RxPdo"
            rx = RxPdo()
            rx.fixed = rxp.get("Fixed", "0")
            rx.sm = rxp.get("Sm", "")
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
                rx.entry.append(ent)
            dev.rx_pdo.append(rx)
        # `TxPdo` (Optional 0..inf)
        #     Description of the input process data
        for txp in device.findall("TxPdo"):
            print "TxPdo"
            tx = TxPdo()
            for item in txp.items():
                print " |-", item[0], "=", item[1]
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
                tx.entry.append(ent)
            dev.tx_pdo.append(tx)
        # `Mailbox` (Optional 0..1)
        #     Description of available mailbox protocols
        mailbox = device.find("Mailbox")
        if mailbox is not None:
            dev.mailbox = Mailbox()
            # `CoE`
            mbox_coe = mailbox.find("CoE")
            if mbox_coe is not None:
                dev.mailbox.coe = mbox_coe.attrib
            # `FoE`
            mbox_foe = mailbox.find("FoE")
            if mbox_foe is not None:
                dev.mailbox.foe = mbox_foe.attrib
            # `AoE`
            mbox_aoe = mailbox.find("AoE")
            if mbox_aoe is not None:
                dev.mailbox.aoe = mbox_aoe.attrib
        # `Dc` (Optional 0..1)
        #     Description of the following synchronization modes if available:
        #     {Freerun | Synchronous w/ Sm Event | Distributed Clocks}
        dc = device.find("Dc")
        if dc is not None:
            dev.dc = Dc()
            # `OpMode`
            for item in dc.findall("OpMode"):
                opmode = DcOpMode()
                print "Dc -> OpMode"
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
                if dc_cyc_syn0 is not None:
                    opmode.cycle_time_sync_1 = dc_cyc_syn1.text
                # `ShiftTimeSync1`
                if dc_sft_snc1 is not None:
                    opmode.shift_time_sync_1 = dc_sft_snc1.text
                dev.dc.op_mode.append(opmode)
        # `Slots`
        #     Defines the combination of possibilities of the modules which may
        #     be used if the device supports Modular Device Profiles (ETG.5001)
        #     The modules are defined in the `Modules` element
        # `Eeprom` (Optional 0..1)
        if device.find("Eeprom") is not None:
            dev.eeprom = Eeprom()
            eeprom_bytesize = device.find("./Eeprom/ByteSize")
            eeprom_configdata = device.find("./Eeprom/ConfigData")
            eeprom_bootstrap = device.find("./Eeprom/BootStrap")
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
            # `Image16x14` (Optional 0..1)
            # `ImageFile16x14` (Optional 0..1)
            # `ImageData16x14` (Optional 0..1)
        # Add our device to the list of devices
        devices.append(dev)
    print len(devices)

if __name__ == "__main__":
    #parser_top_level("./file.xml")
    parser_top_level("./file1.xml")
