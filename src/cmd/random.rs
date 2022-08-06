use clap::Args;
use rand::distributions::DistString;
use hbkit::random::RandomDist;

#[derive(Args)]
pub struct Random {
    /// String length
    #[clap(value_parser, default_value_t=16)]
    length: u8,
    /// Quite mode
    #[clap(short, long, action)]
    quite: bool
}

const TYPES: [&str; 5] = ["n", "na", "nau", "nauf", "x"];

impl super::Command for Random {
    fn run(&self, _ctx: &super::Context) {
        let mut rng = rand::thread_rng();

        for flags in TYPES {
            let rd = RandomDist::new(flags).unwrap();
            let out = rd.sample_string(&mut rng, self.length as usize);
            if self.quite {
                println!("{out}");
            } else {
                println!("{flags:8}: {out}");
            }
        }
    }
}
