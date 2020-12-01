use std::io::Read;
use std::io;
use std::fs::File;

use gumdrop::Options;


#[derive(Debug, Clone, Options)]
pub struct GameOptions {
    #[options(help = "some help text")]
    pub opt1: Option<String>,

    #[options(help = "some help text", short="s")]
    pub opt2: Option<String>,

    #[options(help = "display help text")]
    pub help: bool,
}

fn read_file(file_name: &str) -> Vec<String> {
    let mut file = File::open(file_name).unwrap();

    let mut string = String::new();
    file.read_to_string(&mut string).unwrap();

    let lines = string.lines();

    return lines.map(|s| s.to_string()).collect::<Vec<String>>();
}

fn main() {
    let opts = GameOptions::parse_args_default_or_exit();

    let name = "view.tcl";
    let lines = read_file(name);
}
