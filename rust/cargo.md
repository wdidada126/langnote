# cargo

cargo
Rust's package manager

USAGE:
    cargo [OPTIONS] [SUBCOMMAND]

OPTIONS:
    -V, --version                  Print version info and exit
        --list                     List installed commands
        --explain <CODE>           Run `rustc --explain CODE`
    -v, --verbose                  Use verbose output (-vv very verbose/build.rs output)
    -q, --quiet                    Do not print cargo log messages
        --color <WHEN>             Coloring: auto, always, never
        --frozen                   Require Cargo.lock and cache are up to date
        --locked                   Require Cargo.lock is up to date
        --offline                  Run without accessing the network
        --config <KEY=VALUE>...    Override a configuration value (unstable)
    -Z <FLAG>...                   Unstable (nightly-only) flags to Cargo, see 'cargo -Z help' for details
    -h, --help                     Prints help information

Some common cargo commands are (see all commands with --list):
    build, b    Compile the current package
    check, c    Analyze the current package and report errors, but don't build object files
    clean       Remove the target directory
    doc, d      Build this package's and its dependencies' documentation
    new         Create a new cargo package
    init        Create a new cargo package in an existing directory
    run, r      Run a binary or example of the local package
    test, t     Run the tests
    bench       Run the benchmarks
    update      Update dependencies listed in Cargo.lock
    search      Search registry for crates
    publish     Package and upload this package to the registry
    install     Install a Rust binary. Default location is $HOME/.cargo/bin
    uninstall   Uninstall a Rust binary

版本号是范围

cargo --version
cargo 1.87.0 (99624be96 2025-05-06)

## 设置cargo版本
zed某个提交的代码
限定cargo

cargo run --release
info: syncing channel updates for '1.85-x86_64-unknown-linux-gnu'
info: latest update on 2025-03-18, rust version 1.85.1 (4eb161250 2025-03-15)
info: downloading component 'cargo'
