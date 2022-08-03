use rand;
use rand::distributions::DistString;
use clap::Parser;
use hbkit::random::RandomDist;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about=None)]
struct Args {
    /// Random string length
    #[clap(short, long, value_parser, default_value_t = 12)]
    length: u8
}

fn main() {
    let args = Args::parse();
    let rd = RandomDist::new("naf").unwrap();
    let mut rng = rand::thread_rng();

    println!("Hello {}", rd.sample_string(&mut rng, args.length as usize));
}
