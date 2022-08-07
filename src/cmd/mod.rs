use crate::Args;

#[derive(Debug)]
pub struct Context {
    verbose: bool
}

impl Context {
    // See: rustc --explain E0446
    pub(crate) fn new(args: &Args) -> Self {
        return Context {
            verbose: args.verbose
        };
    }

    pub fn start(&self) {
        if self.verbose {
            println!("Start in verbose mode");
        } else {
            println!("Start in normal mode");
        }
    }
}

pub trait Command {
    fn run(&self, ctx: &Context);
}

mod random;
pub use random::Random;
