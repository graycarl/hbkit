use clap::{Parser, Subcommand};

use cmd::Command;
mod cmd;

/// Personal toolkit
#[derive(Parser)]
#[clap(author, version, about, long_about=None)]
struct Args {  // See: rustc --explain E0446
    /// Verbose mode
    #[clap(short, long, action)]
    pub verbose: bool,
    
    #[clap(subcommand)]
    command: Commands
}

#[derive(Subcommand)]
enum Commands {
    /// Generate random strings
    Random(cmd::Random),
}


fn main() {
    let args = Args::parse();
    let ctx = cmd::Context::new(&args);
    ctx.start();

    match args.command {
        Commands::Random(random) => {
            random.run(&ctx);
        }
    }
}
