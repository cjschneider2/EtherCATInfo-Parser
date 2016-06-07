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
                            foo => {
                                println!("{:?}", foo);
                                panic!("CData not found")
                            }
                        }
                    }
                    "Fmmu" => { },
                    "Sm" => { },
                    "Mailbox" => {
                        // AoE
                        // CoE
                        // FoE
                    },
                    "Eeprom" => { },
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
                    _ => ()
                }
            },
            Ok(_) => (),
            Err(error) => {println!("{}", error);}
        }
    }
}
