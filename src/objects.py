class DcOpMode(object):
    pass


class Eeprom(object):
    pass


class Fmmu(object):
    pass


class Mailbox(object):
    pass


class RxPdo(object):
    def __init__(self):
        self.fixed = ""
        self.sm = ""
        self.index = ""
        self.name = ""
        self.exclude = ""
        self.entry = []
    pass


class PdoEntry(object):
    def __init__(self):
        self.index = ""
        self.sub_index = ""
        self.bit_len = ""
        self.name = ""
        self.data_type = ""
    pass


class Device(object):
    def __init__(self):
        self.typ = ""
        self.vendor_id = ""
        self.product_code = ""
        self.revision_no = ""
        self.serial_no = ""
        self.check_product_code = ""
        self.group_type = ""
        self.mailbox = ""
        self.dc = ""
        self.name = []
        self.url = []
        self.hide_type = []
        self.fmmu = []
        self.sm = []
        self.rx_pdo = []
        self.tx_pdo = []
    pass


class TxPdo(object):
    def __init__(self):
        self.fixed = ""
        self.sm = ""
        self.index = ""
        self.name = ""
        self.exclude = ""
        self.entry = []
    pass


class Sm (object):
    pass


class Dc(object):
    def __init__(self):
        self.op_mode = []
    pass
