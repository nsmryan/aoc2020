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

#[derive(Clone, Debug)]
pub struct Problem {
    start: i64,
    departs: Vec<Option<i64>>,
}

impl Problem {
    pub fn new(start: i64, departs: Vec<Option<i64>>) -> Problem {
        return Problem { start, departs };
    }
}

pub fn parse_problem(lines: &Vec<String>) -> Problem {
    let starts = lines[0].parse::<i64>().unwrap();

    let departs = lines[1].split(',')
                       .map(|time| {
                           if time == "x" {
                               None
                           } else {
                               Some(time.parse::<i64>().unwrap())
                           }
                       })
                       .collect::<Vec<Option<i64>>>();

    return Problem::new(starts, departs);
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

    let problem = parse_problem(&lines);

    // PART 1
    let mut time = problem.start;
    let mut searching = true;
    while searching {
        for depart in problem.departs.iter() {
            if let Some(depart) = depart {
                if time % depart == 0 {
                    searching = false;
                    println!("{} * {} = {}", depart, time - problem.start, depart * (time - problem.start)); 
                    break;
                }
            }
        }

        time += 1;
    }
    println!("");

    // PART 2
    let mut start = 0;
    let mut cycle = 1;
    for (index, depart) in problem.departs.iter().enumerate() {
        if let Some(depart) = depart {
            println!("{} {}", start, cycle);
            for i in 1..=*depart {
                if (((start + (cycle * i)) % *depart) + index as i64) % *depart == 0 {
                    start += cycle * i;
                    cycle *= *depart;
                    break;
                }
            }
        }
    }
    println!("{} {}", start, cycle);
}

