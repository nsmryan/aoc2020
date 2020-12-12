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
pub enum Tile {
    Empty,
    Seat,
    Occupied,
}

impl Tile {
    pub fn from_char(chr: char) -> Tile {
        match chr {
            '.' => Tile::Empty,
            'L' => Tile::Seat,
            '#' => Tile::Occupied,
            _ => panic!(format!("Unexpected char {}", chr)),
        }
    }
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Ord, PartialOrd)]
pub enum Rule {
    One,
    Two,
}

pub type Layout = Vec<Vec<Tile>>;

pub fn parse_layout(lines: &Vec<String>) -> Layout {
    let mut layout = Vec::new();
    for row_str in lines {
        let mut row = Vec::new();
        for ch in row_str.chars() {
            row.push(Tile::from_char(ch));
        }

        layout.push(row);
    }

    return layout;
}

pub fn rules(layout: &Layout, row_index: usize, col_index: usize) -> Tile {
    let offsets: &[(i32, i32)] = &[(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)];

    let mut count = 0;
    for offset in offsets {
        let pos = (offset.0 + row_index as i32, offset.1 + col_index as i32);

        if pos.0 < 0 || pos.0 >= layout.len() as i32 || pos.1 < 0 || pos.1 >= layout[0].len() as i32 {
            continue;
        }

        if layout[pos.0 as usize][pos.1 as usize] == Tile::Occupied {
            count += 1;
        }
    }

    match layout[row_index][col_index] {
        Tile::Empty => {
            return Tile::Empty;
        }

        Tile::Occupied => {
            if count >= 4 {
                return Tile::Seat;
            }
            return Tile::Occupied;
        }

        Tile::Seat => {
            if count == 0 {
                return Tile::Occupied;
            }
            return Tile::Seat;
        }
    }
}

pub fn rules2(layout: &Layout, row_index: usize, col_index: usize) -> Tile {
    let offsets: &[(i32, i32)] = &[(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)];

    let mut count = 0;
    for offset in offsets {
        let mut pos = (offset.0 + row_index as i32, offset.1 + col_index as i32);

        while pos.0 >= 0 && pos.0 < layout.len() as i32 && pos.1 >= 0 && pos.1 < layout[0].len() as i32 {

            let tile = layout[pos.0 as usize][pos.1 as usize];

            if tile == Tile::Occupied {
                count += 1;
            }

            if tile != Tile::Empty {
                break;
            }

            pos.0 += offset.0;
            pos.1 += offset.1;
        }
    }

    match layout[row_index][col_index] {
        Tile::Empty => {
            return Tile::Empty;
        }

        Tile::Occupied => {
            if count >= 5 {
                return Tile::Seat;
            }
            return Tile::Occupied;
        }

        Tile::Seat => {
            if count == 0 {
                return Tile::Occupied;
            }
            return Tile::Seat;
        }
    }
}

pub fn step(layout: &mut Layout, rule: Rule) -> bool {
    // NOTE cloning every step! for shame
    let old_layout = layout.clone();

    let mut changed = false;
    for row_index in 0..layout.len() {
        for col_index in 0..layout[row_index].len() {
            let tile = 
                match rule {
                    Rule::One => rules(&old_layout, row_index, col_index),
                    Rule::Two => rules2(&old_layout, row_index, col_index),
                };

            layout[row_index][col_index] = tile;

            if tile != old_layout[row_index][col_index] {
                changed = true;
            }
        }
    }

    return changed;
}

pub fn count_tiles(match_tile: Tile, layout: &Layout) -> usize {
    let mut count: usize = 0;
    for row in layout {
        for tile in row {
            if *tile == match_tile {
                count += 1;
            }
        }
    }

    return count;
}

pub fn print_layout(layout: &Layout) {
    for row in layout {
        for tile in row {
            match tile {
                Tile::Occupied => print!("#"),
                Tile::Empty => print!("."),
                Tile::Seat => print!("L"),
            }
        }
        println!("");
    }
    println!("");
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

    let mut layout = parse_layout(&lines);

    while step(&mut layout, Rule::One) { 
    }

    let count = count_tiles(Tile::Occupied, &layout);

    println!("count = {}", count);

    let mut layout = parse_layout(&lines);

    while step(&mut layout, Rule::Two) { 
    }

    let count = count_tiles(Tile::Occupied, &layout);

    println!("count = {}", count);
}

