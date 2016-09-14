# Returns a string text for the Locale Id codes.
# NOTE: These codes are based on the Microsoft Locale Id codes.
def lookup_location_id(val):
    if val == "1033" or val == "3081" or val == "2057": # English
        return "EN"
    elif val == "1031" or val == "2055": # German
        return "DE"
    elif val == "1036" or val == "3084": # French
        return "Fr"
    elif val == "2052" or val == "3076": # Chinese
        return "Zh"
    elif val == "1041": # Japanese
        return "Jp"
    elif val == "1043": # Dutch
        return "Nl"
    elif val == "1040": # Italian
        return "It"
    elif val == "1027": # Catalan
        return "Ca"
    elif val == "1044" or val == "2068": # Norwegian
        return "No"
    elif val == "2070": # Portuguese
        return "Pt"
    elif val == "1053": # Swedish
        return "Sv"
    elif val == "1034": # Spanish
        return "Es"
    elif val == "1049": # Russian
        return "Ru"
    else:
        return "Unknown"

# parses the xml form of hex numerals (#x0000)
# and returns a C compatible version  (0x0000)
def strip_pound_hex(xml_hex):
    return xml_hex.replace('#', '0', 1)

# parses the data type value to add 'BDT_' to the beginning.
# This was added to help prevent datatype conflicts
def prepend_bdt(bdt_string):
    return "BDT_{}".format(bdt_string)
