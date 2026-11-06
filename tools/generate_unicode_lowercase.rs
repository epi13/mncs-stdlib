//! Generate MNCS lowercase tables from the Rust Unicode tables used by the
//! Language Service host. The generated MNCS path remains the runtime owner;
//! this tool is only the versioned data authoring step.

use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

const BEGIN: &str = "// BEGIN GENERATED UNICODE LOWERCASE";
const END: &str = "// END GENERATED UNICODE LOWERCASE";
const PAGE_SIZE: u32 = 512;
const SCALAR_BITS: u32 = 21;

struct TemporaryDirectory(PathBuf);

impl Drop for TemporaryDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

fn mappings() -> BTreeMap<u32, Vec<(u32, u64)>> {
    let mut pages: BTreeMap<u32, Vec<(u32, u64)>> = BTreeMap::new();
    for scalar in 0..=0x10ffff {
        let Some(character) = char::from_u32(scalar) else {
            continue;
        };
        let original = character.to_string();
        let lowered: String = character.to_lowercase().collect();
        if lowered == original {
            continue;
        }

        let outputs: Vec<u32> = lowered.chars().map(u32::from).collect();
        assert!(!outputs.is_empty() && outputs.len() <= 3);
        assert!(outputs
            .iter()
            .all(|output| *output != 0 && *output <= 0x10ffff));
        assert!(
            lowered.len() <= character.len_utf8() * 3,
            "a Unicode lowercase mapping exceeds the 3x output contract at U+{scalar:04X}"
        );
        let first = u64::from(outputs[0]);
        let second = outputs.get(1).copied().map(u64::from).unwrap_or(0);
        let third = outputs.get(2).copied().map(u64::from).unwrap_or(0);
        let packed = first | (second << SCALAR_BITS) | (third << (SCALAR_BITS * 2));
        pages
            .entry(scalar / PAGE_SIZE)
            .or_default()
            .push((scalar, packed));
    }
    assert!(
        pages.values().all(|entries| entries.len() <= 1024),
        "a Unicode lowercase page exceeds the bounded MNCS table size"
    );
    pages
}

fn case_properties() -> Vec<(u32, u32, u64)> {
    let helper = PathBuf::from("tools/generate_unicode_case_properties.rs");
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("system clock before Unix epoch")
        .as_nanos();
    let temporary = TemporaryDirectory(
        env::temp_dir().join(format!("mncs-unicode-case-{}-{unique}", std::process::id())),
    );
    fs::create_dir(&temporary.0).expect("create temporary Unicode property directory");
    let helper_binary = temporary.0.join("unicode-case-properties");
    let compiled = Command::new("rustc")
        .arg("--edition=2021")
        .arg(&helper)
        .arg("-o")
        .arg(&helper_binary)
        .env("RUSTC_BOOTSTRAP", "1")
        .output()
        .expect("compile Rust Unicode property helper");
    assert!(
        compiled.status.success(),
        "Rust Unicode property helper failed to compile:\n{}",
        String::from_utf8_lossy(&compiled.stderr)
    );
    let generated = Command::new(helper_binary)
        .output()
        .expect("run Rust Unicode property helper");
    assert!(
        generated.status.success(),
        "Rust Unicode property helper failed:\n{}",
        String::from_utf8_lossy(&generated.stderr)
    );

    let mut lines =
        String::from_utf8(generated.stdout).expect("Rust Unicode property output is UTF-8");
    let mut values = lines.lines();
    let version = values.next().expect("Unicode property version missing");
    let (major, minor, patch) = char::UNICODE_VERSION;
    assert_eq!(version, format!("version {major} {minor} {patch}"));

    let mut points: BTreeMap<u32, u64> = BTreeMap::new();
    for line in values {
        let mut fields = line.split_whitespace();
        let scalar: u32 = fields
            .next()
            .expect("property scalar missing")
            .parse()
            .expect("invalid property scalar");
        let flags: u64 = fields
            .next()
            .expect("property flags missing")
            .parse()
            .expect("invalid property flags");
        assert!(fields.next().is_none(), "unexpected Unicode property field");
        points.insert(scalar, flags);
    }
    lines.clear();
    let mut ranges = Vec::new();
    let mut entries = points.into_iter();
    let Some((first, first_flags)) = entries.next() else {
        return ranges;
    };
    let mut start = first;
    let mut previous = first;
    let mut flags = first_flags;
    for (scalar, next_flags) in entries {
        if scalar == previous + 1 && next_flags == flags {
            previous = scalar;
            continue;
        }
        ranges.push((start, previous, flags));
        start = scalar;
        previous = scalar;
        flags = next_flags;
    }
    ranges.push((start, previous, flags));
    assert!(
        ranges.len() <= 1024,
        "Unicode case-property ranges exceed the bounded MNCS table size"
    );
    ranges
}

fn generate() -> String {
    let pages = mappings();
    let property_ranges = case_properties();
    let (major, minor, patch) = char::UNICODE_VERSION;
    let rustc_version = Command::new("rustc")
        .arg("--version")
        .output()
        .ok()
        .filter(|result| result.status.success())
        .map(|result| String::from_utf8_lossy(&result.stdout).trim().to_owned())
        .unwrap_or_else(|| "rustc version unavailable".to_owned());

    let mut output = format!(
        "{BEGIN}\n// Unicode {major}.{minor}.{patch}; generated from {rustc_version}.\n\
fn lowercase_unicode_data_version() -> (result: UnicodeDataVersion) {{\n\
    return UnicodeDataVersion {{ major: {major}, minor: {minor}, patch: {patch} }};\n\
}}\n\
fn lowercase_mapping(value: u64) -> (result: LowercaseScalar) {{\n\
    let packed: u64 = match value / {PAGE_SIZE} {{\n"
    );

    for page in pages.keys() {
        output.push_str(&format!(
            "        {page} => lowercase_mapping_page{page}(value),\n"
        ));
    }
    output.push_str(
        "        _ => value\n\
    };\n\
    let first: u64 = packed % 2097152;\n\
    let second: u64 = (packed / 2097152) % 2097152;\n\
    let third: u64 = packed / 4398046511104;\n\
    let count: u64 = select(second == 0, 1, select(third == 0, 2, 3));\n\
    return LowercaseScalar { first: first, second: second, third: third, count: count };\n\
}\n",
    );

    output.push_str(
        "fn unicode_case_property_lookup<N: Nat>(starts: [u64; up_to N], ends: [u64; up_to N], properties: [u64; up_to N], value: u64) -> (result: u64) {\n\
    let initial: UnicodeMappingSearch = UnicodeMappingSearch { low: 0, high: starts.len, found: false, mapped: 0 };\n\
    iterate step up_to 12 carrying state: UnicodeMappingSearch = initial {\n\
        let active: bool = state.low < state.high && !state.found;\n\
        let midpoint: u64 = select(active, (state.low + state.high) / 2, 0);\n\
        let start: u64 = starts[midpoint];\n\
        let updated: UnicodeMappingSearch = match select(active, 1, 0) {\n\
            0 => state,\n\
            _ => match select(value < start, 1, 0) {\n\
                1 => UnicodeMappingSearch { ..state, high: midpoint },\n\
                _ => UnicodeMappingSearch { ..state, low: midpoint + 1, mapped: midpoint + 1 }\n\
            }\n\
        };\n\
        next state = updated;\n\
    }\n\
    let has_candidate: bool = state.mapped > 0;\n\
    let candidate: u64 = select(has_candidate, state.mapped - 1, 0);\n\
    return select(has_candidate && value <= ends[candidate], properties[candidate], 0);\n\
}\n\
fn is_cased_scalar(value: u64) -> (result: bool) { return unicode_case_properties(value) % 2 == 1; }\n\
fn is_case_ignorable_scalar(value: u64) -> (result: bool) { return (unicode_case_properties(value) / 2) % 2 == 1; }\n"
    );

    output.push_str(&format!(
        "fn unicode_case_properties(value: u64) -> (result: u64) {{\n    let starts: [u64; {}] = [\n        ",
        property_ranges.len()
    ));
    for (index, (start, _, _)) in property_ranges.iter().enumerate() {
        if index > 0 {
            if index % 12 == 0 {
                output.push_str(",\n        ");
            } else {
                output.push_str(", ");
            }
        }
        output.push_str(&start.to_string());
    }
    output.push_str("\n    ];\n");
    output.push_str(&format!(
        "    let ends: [u64; {}] = [\n        ",
        property_ranges.len()
    ));
    for (index, (_, end, _)) in property_ranges.iter().enumerate() {
        if index > 0 {
            if index % 12 == 0 {
                output.push_str(",\n        ");
            } else {
                output.push_str(", ");
            }
        }
        output.push_str(&end.to_string());
    }
    output.push_str("\n    ];\n");
    output.push_str(&format!(
        "    let properties: [u64; {}] = [\n        ",
        property_ranges.len()
    ));
    for (index, (_, _, flags)) in property_ranges.iter().enumerate() {
        if index > 0 {
            if index % 16 == 0 {
                output.push_str(",\n        ");
            } else {
                output.push_str(", ");
            }
        }
        output.push_str(&flags.to_string());
    }
    output.push_str("\n    ];\n");
    output.push_str(&format!(
        "    return unicode_case_property_lookup<{}>(starts, ends, properties, value);\n}}\n",
        property_ranges.len()
    ));

    for (page, entries) in &pages {
        output.push_str(&format!(
            "fn lowercase_mapping_page{page}(value: u64) -> (result: u64) {{\n"
        ));
        output.push_str(&format!(
            "    let keys: [u64; {}] = [\n        ",
            entries.len()
        ));
        for (index, (scalar, _)) in entries.iter().enumerate() {
            if index > 0 {
                if index % 12 == 0 {
                    output.push_str(",\n        ");
                } else {
                    output.push_str(", ");
                }
            }
            output.push_str(&scalar.to_string());
        }
        output.push_str("\n    ];\n");

        output.push_str(&format!(
            "    let mapped: [u64; {}] = [\n        ",
            entries.len()
        ));
        for (index, (_, mapped)) in entries.iter().enumerate() {
            if index > 0 {
                if index % 8 == 0 {
                    output.push_str(",\n        ");
                } else {
                    output.push_str(", ");
                }
            }
            output.push_str(&mapped.to_string());
        }
        output.push_str("\n    ];\n");
        output.push_str(&format!(
            "    return unicode_mapping_lookup<{}>(keys, mapped, value);\n}}\n",
            entries.len()
        ));
    }
    output.push_str(END);
    output.push('\n');
    eprintln!(
        "generated {} Unicode lowercase scalar mappings and {} case-property ranges for Unicode {major}.{minor}.{patch}",
        pages.values().map(Vec::len).sum::<usize>(),
        property_ranges.len(),
    );
    output
}

fn main() {
    let mut args = env::args().skip(1);
    let mode = args.next().unwrap_or_else(|| "--write".to_owned());
    let path = PathBuf::from(
        args.next()
            .unwrap_or_else(|| "library/std/text_utf8.mncs".to_owned()),
    );
    if args.next().is_some() || !matches!(mode.as_str(), "--write" | "--check") {
        eprintln!("usage: generate_unicode_lowercase.rs [--write|--check] [text_utf8.mncs]");
        std::process::exit(2);
    }

    let current = fs::read_to_string(&path).expect("read MNCS text module");
    let begin = current
        .find(BEGIN)
        .expect("generated lowercase start marker missing");
    let end = current
        .find(END)
        .expect("generated lowercase end marker missing");
    assert!(begin < end, "generated lowercase markers are out of order");
    let generated = generate();
    let suffix = current[end + END.len()..].trim_start_matches('\n');
    let replacement = format!("{}{}\n{}", &current[..begin], generated, suffix);
    if mode == "--check" {
        if replacement != current {
            eprintln!("Unicode lowercase table differs from current Rust char::to_lowercase data");
            std::process::exit(1);
        }
    } else {
        fs::write(&path, replacement).expect("write generated MNCS text module");
    }
}
