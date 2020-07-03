# servo



`     Running `rustc --crate-name android_injected_glue /usr/local/cargo/registry/src/github.com-1ecc6299db9ec823/android_injected_glue-0.2.3/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi --crate-type lib --emit=dep-info,metadata,link -C debuginfo=2 -C metadata=ef8ae9b622025074 -C extra-filename=-ef8ae9b622025074 --out-dir /opt/atlassian/pipelines/agent/build/target/debug/deps -L dependency=/opt/atlassian/pipelines/agent/build/target/debug/deps --cap-lints allow``

```
   Compiling log v0.4.6
```

`     Running `rustc --crate-name log /usr/local/cargo/registry/src/github.com-1ecc6299db9ec823/log-0.4.6/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts --crate-type lib --emit=dep-info,metadata,link -C debuginfo=2 --cfg 'feature="release_max_level_info"' --cfg 'feature="std"' -C metadata=5f5b2e07f23de98d -C extra-filename=-5f5b2e07f23de98d --out-dir /opt/atlassian/pipelines/agent/build/target/debug/deps -L dependency=/opt/atlassian/pipelines/agent/build/target/debug/deps --extern cfg_if=/opt/atlassian/pipelines/agent/build/target/debug/deps/libcfg_if-3d348beeae311da9.rmeta --cap-lints allow``

`error[E0432]: unresolved import `this_platform_is_not_supported``

```shell
   --> /usr/local/cargo/registry/src/github.com-1ecc6299db9ec823/android_injected_glue-0.2.3/src/lib.rs:162:5
```





