use clap::Parser;
use guess_rs::{
    self as guessr,
    config::{Args, Config},
    Location,
};

fn main() {
    let args = Args::parse();

    match guessr::guess_address(
        &args.street,
        Location::from_args(&args),
        Config::from_args(&args),
    ) {
        Ok(address) => match address.1 {
            Location::Empty => println!("{}", address.0.sequence),
            location => println!("{}, {}", location.to_string(), address.0.sequence),
        },
        Err(err) => eprintln!("Address not found: {}", err),
    }
}
