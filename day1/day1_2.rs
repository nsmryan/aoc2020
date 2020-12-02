use std::io::Read;
use std::io;
use std::fs::File;


fn read_file(file_name: &str) -> Vec<String> {
    let mut file = File::open(file_name).unwrap();

    let mut string = String::new();
    file.read_to_string(&mut string).unwrap();

    let lines = string.lines();

    return lines.map(|s| s.to_string()).collect::<Vec<String>>();
}

fn main() {
    let lines = read_file("day1.txt");

    let expenses = lines.iter()
                        .filter(|s| !s.is_empty())
                        .map(|s| s.parse::<i64>().unwrap())
                        .collect::<Vec<i64>>();

    for expense1 in expenses.iter() {
        for expense2 in expenses.iter() {
            for expense3 in expenses.iter() {
                if expense1 + expense2 + expense3 == 2020 {
                    println!("{}", expense1 * expense2 * expense3 );
                    return;
                }
            }
        }
    }
    println!("Something went wrong...");
}
