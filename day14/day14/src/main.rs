use std::io::Read;
use std::fs::File;
use std::collections::HashMap;

use regex::Regex;
use gumdrop::Options;


#[derive(Debug, Clone, Options)]
pub struct Opts {
    #[options(help = "input file name", short="f")]
    pub filename: Option<String>,

    #[options(help = "display help text")]
    pub help: bool,
}

#[derive(Clone, Copy, Debug, PartialOrd, PartialEq, Ord, Eq)]
pub enum Instr {
    Mask { mask: u64, value: u64 },
    Mem { loc: u64, value: u64 },
}

impl Instr {
    pub fn from_str(line: &str) -> Instr {
        if line.starts_with("mem") {
            let re = Regex::new(r"mem\[(\d+)\] = (\d+)").unwrap();
            let caps = re.captures(line).unwrap();
            let loc = caps.get(1).unwrap().as_str().parse::<u64>().unwrap();
            let value = caps.get(2).unwrap().as_str().parse::<u64>().unwrap();
            return Instr::Mem { loc, value };
        } else if line.starts_with("mask") {
            let re = Regex::new(r"mask = (.+)").unwrap();
            let caps = re.captures(line).unwrap();
            let bitmask = caps.get(1).unwrap().as_str();

            let mut mask = 0;
            let mut value = 0;
            let mut pos = 35;
            for chr in bitmask.chars() {
                if chr == '1' {
                    value |= 1 << pos;
                } 

                if chr != 'X' {
                    mask |= 1 << pos;
                }

                pos -= 1;
            }

            return Instr::Mask { mask, value };
        }
        panic!(format!("Could not parse '{}'!", line));
    }
}

#[derive(Clone, Debug)]
pub struct Computer {
    instrs: Vec<Instr>,
    mem: HashMap<usize, u64>,
    mask: u64,
    value: u64,
}

impl Computer {
    pub fn new(instrs: Vec<Instr>) -> Computer {
        //let mem_size = *instrs.iter().filter_map(|instr| {
        //    if let Instr::Mem { loc, value } = instr {
        //        return Some(loc);
        //    } 
        //    return None;
        //}).max().unwrap();
        //let mem = vec![0;1 + mem_size as usize];
        let mem = HashMap::new();
        return Computer { instrs, mem, mask: 0, value: 0 };
    }

    pub fn run(&mut self) {
        for instr in self.instrs.iter() {
            match instr {
                Instr::Mask { mask, value } => {
                    self.mask = *mask;
                    self.value = *value;
                }

                Instr::Mem { loc, value } => {
                    self.mem.insert(*loc as usize, (value & !self.mask) | self.value);
                }
            }
        }
    }

    pub fn run2(&mut self) {
        for instr in self.instrs.iter() {
            match instr {
                Instr::Mask { mask, value } => {
                    self.mask = *mask;
                    self.value = *value;
                    println!("mask {:X} = {}", mask, value);
                }

                Instr::Mem { loc, value } => {
                    println!("setting {:X} = {}", loc, value);
                    let mut width = 0;
                    let mut positions = Vec::new();
                    let mut loc = *loc;
                    for index in 0..36 {
                        if (self.mask & (1 << index)) == 0 {
                            width += 1;
                            positions.push(index);
                        }
                        if (self.value & (1 << index)) != 0 {
                            loc |= 1 << index;
                        }
                    }
                    //println!("now {:X}", loc);

                    if width == 0 {
                        self.mem.insert(loc as usize, *value);
                    } else {
                        println!("{}, and a {:?}", width, positions);
                        for bits in 0..(2u64.pow(width)) {
                            let mut addr = loc;
                            for (index, pos) in positions.iter().enumerate() {
                                let addr_cleared = addr & !(1 << pos);
                                let current_bit = (bits & (1 << index)) >> index;
                                addr = addr_cleared | (current_bit << pos);
                                //println!("{:X} {:X}, {}, {} >> {}", loc, addr, pos, current_bit, index);
                                self.mem.insert(addr as usize, *value);
                            }
                        }
                    }
                }
            }
        }
    }

    pub fn sum(&self) -> u64 {
        return self.mem.values().sum();
    }
}

pub fn parse_instrs(lines: &Vec<String>) -> Computer {
    let instrs =
        lines.iter().map(|line|
            Instr::from_str(line)
            ).collect::<Vec<Instr>>();
    let instrs = Computer::new(instrs);
    return instrs;
}

fn read_file(file_name: &str) -> Vec<String> {
    let mut file = File::open(file_name).unwrap();

    let mut string = String::new();
    file.read_to_string(&mut string).unwrap();

    let lines = string.lines();

    return lines.map(|s| s.to_string()).collect::<Vec<String>>();
}

fn main() {
    let opts = Opts::parse_args_default_or_exit();

    let name = 
        match opts.filename {
            Some(name) => name,
            None => "day13.txt".to_string(),
        };

    let lines = read_file(&name);

    let mut instrs = parse_instrs(&lines);
    println!("{:?}", instrs);

    instrs.run2();
    println!("sum is {}", instrs.sum());
}

