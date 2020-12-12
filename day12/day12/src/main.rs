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
pub enum Orient {
    N,
    S,
    E,
    W,
}

impl Orient {
    pub fn from_degrees(degrees: i32) -> Orient {
        let mut deg = degrees;
        if degrees < 0 {
            deg = 360 + degrees;
        } else if degrees >= 360 {
            deg = degrees % 360;
        }

        match deg {
            270 => Orient::N,
            90 => Orient::S,
            0 => Orient::E,
            180 => Orient::W,
            _ => panic!(format!("Degrees {} invalid (was {})!", deg, degrees)),
        }
    }

    pub fn to_degrees(self) -> i32 {
        match self {
            Orient::N => 270,
            Orient::S => 90,
            Orient::E => 0,
            Orient::W => 180,
        }
    }

    pub fn right(&self, degrees: i32) -> Orient {
        return Orient::from_degrees(self.to_degrees() + degrees)
    }

    pub fn left(&self, degrees: i32) -> Orient {
        return Orient::from_degrees(self.to_degrees() - degrees)
    }
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
    orientation: Orient,
    x: i32,
    y: i32,
}

impl Boat {
    pub fn new() -> Boat {
        return Boat { orientation: Orient::E, x: 0, y: 0 };
    }

    pub fn apply(&mut self, instr: Instr) {
        match instr.dir {
            Dir::N => {
                self.y += instr.arg;
            }

            Dir::S => {
                self.y -= instr.arg;
            }

            Dir::E => {
                self.x += instr.arg;
            }

            Dir::W => {
                self.x -= instr.arg;
            }

            Dir::R => {
                self.orientation = self.orientation.right(instr.arg);
            }

            Dir::L => {
                self.orientation = self.orientation.left(instr.arg);
            }

            Dir::F => {
                match self.orientation {
                    Orient::N => self.y += instr.arg,
                    Orient::E => self.x += instr.arg,
                    Orient::S => self.y -= instr.arg,
                    Orient::W => self.x -= instr.arg,
                }
            }
        }
    }

    pub fn dist(&self) -> i32 {
        return self.x.abs() + self.y.abs();
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
            None => "day11.txt".to_string(),
        };

    let lines = read_file(&name);

    let instrs = parse_instrs(&lines);

    let mut boat = Boat::new();
    for instr in instrs.iter() {
        boat.apply(*instr);
        println!("({}, {}) {:?}", boat.x, boat.y, boat.orientation);
    }

    println!("dist = {}", boat.dist());
}

