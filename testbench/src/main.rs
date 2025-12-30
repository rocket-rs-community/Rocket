mod config;
mod runner;
mod servers;

pub mod prelude {
    pub use rocket::fairing::*;
    pub use rocket::response::stream::*;
    pub use rocket::*;

    pub use crate::config::*;
    pub use crate::register;
    pub use testbench::{Error, Result, *};
}

pub use runner::Test;

fn main() -> std::process::ExitCode {
    runner::run()
}
