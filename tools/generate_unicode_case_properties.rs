#![feature(titlecase, case_ignorable)]

use std::io::{self, Write};

fn main() {
    let (major, minor, patch) = char::UNICODE_VERSION;
    let stdout = io::stdout();
    let mut output = io::BufWriter::new(stdout.lock());
    writeln!(output, "version {major} {minor} {patch}").unwrap();

    for scalar in 0..=0x10ffff {
        let Some(character) = char::from_u32(scalar) else {
            continue;
        };
        let flags =
            u64::from(character.is_cased()) | (u64::from(character.is_case_ignorable()) << 1);
        if flags != 0 {
            writeln!(output, "{scalar} {flags}").unwrap();
        }
    }
}
