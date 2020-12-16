use std::io::Read;
use std::fs::File;
use std::collections::HashMap;
use std::collections::VecDeque;

use regex::Regex;
use gumdrop::Options;


#[derive(Debug, Clone, Options)]
pub struct Opts {
    #[options(help = "input file name", short="f")]
    pub filename: Option<String>,

    #[options(help = "display help text")]
    pub help: bool,
}

fn main() {
    let opts = Opts::parse_args_default_or_exit();

    //let nums: &[i32] = &[0, 3, 6];
    let nums: &[i32] = &[7,12,1,0,16,2];

    //let nums: &[i32] = &[1, 3, 2];
    let count = 30000000;

    let mut spoken = Vec::new();
    let mut lasts: HashMap<i32, VecDeque<usize>> = HashMap::new();

    for turn in 0..count {
        let spoke;
        if turn < nums.len() {
            spoke = nums[turn];
            let mut turns = VecDeque::new();
            turns.push_back(turn);
            lasts.insert(spoke, turns);
        } else {
            let last = spoken[turn - 1];

            if let Some(ref mut turns) = lasts.get_mut(&last) {
                turns.push_back(turn - 1);

                if turns.len() > 2 {
                    turns.pop_front();
                }

                //println!("{} ({}, {})", turn, turns[0], turns[1]);
                spoke = (turns[1] - turns[0]) as i32;
            } else {
                let mut turns = VecDeque::new();
                turns.push_back(turn - 1);
                lasts.insert(last, turns);
                spoke = 0;
            }
        }
        spoken.push(spoke);

        if turn % 100000 == 0 && turn != 0 {
            println!("turn hit: {}", turn);
        }
    }

    println!("answer {}", spoken[spoken.len() - 1]);
}

