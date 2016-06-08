extern crate xml;

use std::io::{Read, BufReader};
use std::fs::File;

use xml::ParserConfig;
use xml::reader::EventReader;
use xml::reader::XmlEvent::*;
use xml::attribute::OwnedAttribute;

fn main() {
    //let mut file;
    //let mut stdin;
    //let file = BufReader::new(file);
    //let source: &mut Read = match env::args().nth(1) {
    //    Some(file_name) => {
    //        file = File::open(file_name)
    //            .unwrap_or_else(|e| abort!(1, "Cannot open input file: {}", e));
    //        &mut file
    //    }
    //    None => {
    //        stdin = io::stdin();
    //        &mut stdin
    //    }
    //};

    let source = File::open("file.xml").unwrap();
    let mut reader = ParserConfig::new()
        .whitespace_to_characters(true)
        .ignore_comments(false)
        .coalesce_characters(true)
        .create_reader(BufReader::new(source));

    // Start parsing
    parse_top_level(&mut reader);
}


fn parse_top_level<R: Read>(reader: &mut EventReader<R>) -> () {
    loop {
        match reader.next() {
            Ok(StartElement{ name, attributes, .. }) => {
                    match name.local_name.as_str() {
                        "Device" => {
                            println!("\nStart device");
                            parse_device(reader, attributes)
                        }
                        _ => ()
                    }
            },
            Ok(EndDocument) => { break; }
            Ok(_) => {},
            Err(error) => {println!("{}", error);}
        }
    }
}

fn parse_device<R: Read>(reader: &mut EventReader<R>, _attr: Vec<OwnedAttribute>) -> () {
    loop {
        match reader.next() {
            Ok(StartElement{ name, attributes, .. }) => {
                match name.local_name.as_str() {
                    "Type" => {
                        for a in attributes {
                            println!("{}:{}", a.name.local_name, a.value);
                        }
                        match reader.next() {
                            Ok(Characters(c)) => {
                                println!("Type:{}", c);
                            },
                            _ => { panic!("Type name not found") }
                        }
                    },
                    "Name" => {
                        let typ = match attributes.get(0).unwrap()
                            .value.as_str() {
                            "1033" => "EN",
                            "1031" => "DE",
                            _ => "UNKNOWN",
                        };
                        match reader.next() {
                            Ok(CData(c)) => {
                                println!("Name{}:{}",  typ,c);
                            },
                            Ok(Characters(c)) => {
                                println!("Name{}:{}", typ, c);
                            },
                            element => {
                                println!("{:?}", element);
                                panic!("CData not found")
                            }
                        }
                    }
                    "Fmmu" => {
                        match reader.next() {
                            Ok(Characters(c)) => {
                                match c.as_str() {
                                    "Outputs" => {
                                        println!("FmmuOut: true");
                                    },
                                    "Inputs" => {
                                        println!("FmmuIn : true");
                                    },
                                    "MBoxState" => {
                                        println!("MBoxState: true");
                                    },
                                    typ => {
                                        panic!("Unexpected Fmmu type found: {}", typ);
                                    }
                                }
                            },
                            element => {
                                println!("{:?}", element );
                                panic!("Fmmu Type not found")
                            }
                        }
                    },
                    "Sm" => {
                        for attr in attributes {
                            match attr.name.local_name.as_str() {
                                "MinSize" => {
                                    println!("\tMinSize: {}", attr.value);
                                },
                                "MaxSize" => {
                                    println!("\tMaxSize: {}", attr.value);
                                },
                                "DefaultSize" => {
                                    println!("\tDefaultSize: {}", attr.value);
                                },
                                "StartAddress" => {
                                    println!("\tStartAddress: {}", attr.value);
                                },
                                "ControlByte" => {
                                    println!("\tControlByte: {}", attr.value);
                                },
                                "Enable" => {
                                    println!("\tEnable: {}", attr.value);
                                },
                                attr => { println!("\tUnknown Sm Attribute: {}", attr); }
                            }
                        }
                        // Read the type of the Sync-Manager.
                        // Note: this is actually somewhat of a reversed order of
                        //       how we need the information...
                        match reader.next() {
                            Ok(Characters(c)) => {
                                match c.as_str() {
                                    "Outputs" => {
                                        println!("SmType: Outputs");
                                    },
                                    "Inputs" => {
                                        println!("SmType: Inputs");
                                    },
                                    "MBoxOut" => {
                                        println!("SmType: MBoxOut");
                                    },
                                    "MBoxIn" => {
                                        println!("SmType: MBoxIn");
                                    },
                                    typ => {
                                        panic!("Unexpected Fmmu type found: {}", typ);
                                    }
                                }
                            },
                            element => {
                                println!("{:?}", element );
                                panic!("Fmmu Type not found")
                            }
                        }
                    },
                    "Mailbox" => {
                        // AoE
                        // CoE
                        // FoE
                    },
                    "Eeprom" => {
                        println!("Start Eeprom");
                        parse_eeprom(reader);
                    },
                    "Profile" => {
                        println!("Start Profile");
                        parse_profile(reader, attributes);
                    }
                    "Slots" => {
                        println!("Start Slots");
                        parse_slots(reader, attributes);
                    }
                    _ => {}
                }
            },
            Ok(EndElement{ name }) => {
                match name.local_name.as_str() {
                    "Device" =>  {
                        println!("End device");
                        return
                    },
                    _ => ()
                }
            },
            Ok(_) => (),
            Err(error) => {println!("{}", error);}
        }
    }
}

fn parse_profile<R: Read>(reader: &mut EventReader<R>, _attr: Vec<OwnedAttribute>) -> () {
    loop {
        match reader.next() {
            Ok(EndElement{ name }) => {
                match name.local_name.as_str() {
                    "Profile" =>  {
                        println!("End Profile");
                        return
                    },
                    _ => ()
               }
            },
            Ok(_) => (),
            Err(error) => {println!("{}", error);}
        }
    }
}

fn parse_slots<R: Read>(reader: &mut EventReader<R>, _attr: Vec<OwnedAttribute>) -> () {
    loop {
        match reader.next() {
            Ok(EndElement{ name }) => {
                match name.local_name.as_str() {
                    "Slots" =>  {
                        println!("End Slots");
                        return
                    },
1                    _ => ()
                }
            },
            Ok(_) => (),
            Err(error) => {println!("{}", error);}
        }
    }
}

fn parse_eeprom<R: Read>(reader: &mut EventReader<R>) -> () {
    loop {
        match reader.next() {
            Ok(StartElement{ name, attributes, .. }) => {
                match name.local_name.as_str() {
                    "ByteSize" =>  {
                        println!("ByteSize: {}", );
                    },
                    "ConfigData" =>  {
                        println!("ConfigData: {}", 0);
                    },
                    "BootStrap" =>  {
                        println!("BootStrap: {}", 0);
                    },
                    typ => {
                        println!("Unknown Eeprom data: {}", typ);
                    }
                }
            }
            Ok(EndElement{ name }) => {
                match name.local_name.as_str() {
                    "Eeprom" =>  {
                        println!("End Eeprom");
                        return
                    },
                    _ => ()
                }
            },
            Ok(_) => (),
            Err(error) => {println!("{}", error);}
        }
    }
}
