use std::io::Read;
use std::fs::File;

use gumdrop::Options;


#[derive(Debug, Clone, Options)]
pub struct Opts {
    #[options(help = "input file name", short="f")]
    pub filename: Option<String>,

    #[options(help = "display help text")]
    pub help: bool,
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Ord, PartialOrd)]
pub enum Dir {
    N,
    S,
    E,
    W,
    R,
    L,
    F,
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Ord, PartialOrd)]
pub struct Instr {
    dir: Dir,
    arg: i32,
}

impl Instr {
    pub fn new(dir: Dir, arg: i32) -> Instr {
        return Instr { dir, arg };
    }

    pub fn from_str(line: &str) -> Instr {
        let amount = line[1..].parse::<i32>().unwrap();
        match line.chars().next().unwrap() {
            'N' => Instr::new(Dir::N, amount),
            'S' => Instr::new(Dir::S, amount),
            'E' => Instr::new(Dir::E, amount),
            'W' => Instr::new(Dir::W, amount),
            'R' => Instr::new(Dir::R, amount),
            'L' => Instr::new(Dir::L, amount),
            'F' => Instr::new(Dir::F, amount),
            _ => panic!(format!("Unexpected line {}", line)),
        }
    }
}

#[derive(Clone, Debug)]
pub struct Boat {
    waypoint: (i32, i32),
    pos: (i32, i32),
}

impl Boat {
    pub fn new() -> Boat {
        return Boat { waypoint: (10, 1), pos: (0, 0) };
    }

    pub fn apply(&mut self, instr: Instr) {
        match instr.dir {
            Dir::N => {
                self.waypoint.1 += instr.arg;
            }

            Dir::S => {
                self.waypoint.1 -= instr.arg;
            }

            Dir::E => {
                self.waypoint.0 += instr.arg;
            }

            Dir::W => {
                self.waypoint.0 -= instr.arg;
            }

            Dir::R => {
                if instr.arg == 90 {
                    let tmp = self.waypoint.0;
                    self.waypoint.0 = self.waypoint.1;
                    self.waypoint.1 = -tmp;
                } else if instr.arg == 180 {
                    self.waypoint.0 *= -1;
                    self.waypoint.1 *= -1;
                } else if instr.arg == 270 {
                    let tmp = self.waypoint.0;
                    self.waypoint.0 = self.waypoint.1;
                    self.waypoint.1 = -tmp;
                    self.waypoint.0 *= -1;
                    self.waypoint.1 *= -1;
                } else {
                    panic!();
                }
            }

            Dir::L => {
                if instr.arg == 90 {
                    let tmp = self.waypoint.0;
                    self.waypoint.0 = -self.waypoint.1;
                    self.waypoint.1 = tmp;
                } else if instr.arg == 180 {
                    self.waypoint.0 *= -1;
                    self.waypoint.1 *= -1;
                } else if instr.arg == 270 {
                    let tmp = self.waypoint.0;
                    self.waypoint.0 = -self.waypoint.1;
                    self.waypoint.1 = tmp;
                    self.waypoint.0 *= -1;
                    self.waypoint.1 *= -1;
                } else {
                    panic!();
                }
            }

            Dir::F => {
                self.pos.0 += instr.arg * self.waypoint.0;
                self.pos.1 += instr.arg * self.waypoint.1;
            }
        }
    }

    pub fn dist(&self) -> i32 {
        return self.pos.0.abs() + self.pos.1.abs();
    }
}

pub fn parse_instrs(lines: &Vec<String>) -> Vec<Instr> {
    return lines.iter()
                .map(|line| Instr::from_str(line))
                .collect::<Vec<Instr>>();
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
            None => "day12.txt".to_string(),
        };

    let lines = read_file(&name);

    let instrs = parse_instrs(&lines);

    let mut boat = Boat::new();
    for instr in instrs.iter() {
        boat.apply(*instr);
        println!("{:6?} {:4?} ({:3?} {:3})", boat.pos, boat.waypoint, instr.dir, instr.arg);
    }

    println!("dist = {}", boat.dist());
}

