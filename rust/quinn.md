# quinn
https://crates.io/crates/quinn
quic
Quinn is a pure-Rust, async-compatible implementation of the IETF QUIC transport protocol. The project was founded by Dirkjan Ochtman and Benjamin Saunders as a side project in 2018, and has seen more than 30 releases since then. If you're using Quinn in a commercial setting, please consider sponsoring the project.

Features
Simultaneous client/server operation
Ordered and unordered stream reads for improved performance
Works on stable Rust, tested on Linux, macOS and Windows
Pluggable cryptography, with a standard implementation backed by rustls and ring
Application-layer datagrams for small, unreliable messages
Future-based async API
Minimum supported Rust version of 1.74.1
Overview
quinn: High-level async API based on tokio, see examples for usage. This will be used by most developers. (Basic benchmarks are included.)
quinn-proto: Deterministic state machine of the protocol which performs no I/O internally and is suitable for use with custom event loops (and potentially a C or C++ API).
quinn-udp: UDP sockets with ECN information tuned for the protocol.
bench: Benchmarks without any framework.
fuzz: Fuzz tests.

https://github.com/quinn-rs/quinn

https://docs.rs/quinn/0.11.9/quinn/