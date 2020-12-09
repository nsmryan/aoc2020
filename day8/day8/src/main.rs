use std::io::Read;
use std::io;
use std::fs::File;
use std::collections::HashSet;

use gumdrop::Options;


#[derive(Debug, Clone, Options)]
pub struct Opts {
    #[options(help = "input file name", short="f")]
    pub filename: Option<String>,

    #[options(help = "display help text")]
    pub help: bool,
}

type Val = i64;

#[derive(Debug, Clone, Copy)]
pub enum Asm {
    Acc(Val),
    Jmp(Val),
    Nop(Val),
}

impl Asm {
    pub fn parse_line(line: &str) -> Asm {
        let mut parts = line.split(" ");
        let op = parts.next().unwrap();
        let val_str = parts.next().unwrap();

        let val = val_str.parse::<i64>().unwrap();

        if op.starts_with("jmp") {
            return Asm::Jmp(val);
        } else if op.starts_with("nop") {
            return Asm::Nop(val);
        } else if op.starts_with("acc") {
            return Asm::Acc(val);
        }

        panic!(format!("Instruction {} could not be parsed!", line));
    }
}

#[derive(Debug, Clone)]
pub struct Machine {
    accum: Val,
    ip: i64,
    asm: Vec<Asm>,
}

impl Machine {
    pub fn new() -> Machine {
        return Machine { accum: 0, ip: 0, asm: Vec::new() };
    }

    pub fn from_lines(lines: Vec<String>) -> Machine {
        let mut machine = Machine::new();

        for line in lines {
            machine.asm.push(Asm::parse_line(&line));
        }

        return machine;
    }

    pub fn step(&mut self) {
        match self.asm[self.ip as usize] {
            Asm::Acc(val) => {
                self.accum += val;
                self.ip += 1;
            },

            Asm::Jmp(val) => {
                self.ip += val;
            },

            Asm::Nop(val) => {
                self.ip += 1;
            },
        }
    }

    pub fn reset(&mut self) {
        self.ip = 0;
        self.accum = 0;
    }

    pub fn terminated(&self) -> bool {
        return self.ip == self.asm.len() as i64;
    }
}


fn read_file(file_name: &str) -> Vec<String> {
    let mut file = File::open(file_name).unwrap();

    let mut string = String::new();
    file.read_to_string(&mut string).unwrap();

    let lines = string.lines();

    return lines.map(|s| s.to_string()).collect::<Vec<String>>();
}

pub fn run(machine: &mut Machine) {
    let mut seen: HashSet<i64> = HashSet::new();

    machine.reset();

    while !machine.terminated() &&
          !seen.contains(&machine.ip) {
        seen.insert(machine.ip);
        machine.step();
    }
}

pub fn swapop(asm: Asm) -> Asm {
    match asm {
        Asm::Jmp(val) => Asm::Nop(val),
        Asm::Nop(val) => Asm::Jmp(val),
        Asm::Acc(val) => Asm::Acc(val),
    }
}

fn main() {
    let opts = Opts::parse_args_default_or_exit();

    let name = 
        match opts.filename {
            Some(name) => name,
            None => "day8.txt".to_string(),
        };

    let lines = read_file(&name);

    let mut machine = Machine::from_lines(lines);

    run(&mut machine);

    println!("accum = {}", machine.accum);

    for index in 0..machine.asm.len() {
        let oldasm = machine.asm[index];
        let newasm = swapop(oldasm);
        machine.asm[index] = newasm;
        run(&mut machine);
        machine.asm[index] = oldasm;

        if machine.terminated() {
            println!("terminated with accum {}", machine.accum);
            break;
        }
    }

    println!("finished!");
}

