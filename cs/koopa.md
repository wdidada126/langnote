# koopa


    - name: Clone and build koopa
      run: |
        cd /tmp
        git clone --single-branch --depth 1 https://github.com/pku-minic/koopa.git
        cd koopa
        source $HOME/.cargo/env
        CARGO_PROFILE_RELEASE_PANIC=abort cargo build -r -p libkoopa

    - name: Install koopa to /usr/local
      run: |
        cd /tmp/koopa
        sudo mkdir -p /usr/local/lib/native
        sudo cp target/release/libkoopa.a /usr/local/lib/native/
        sudo mkdir -p /usr/local/include
        sudo cp -R libkoopa/include/* /usr/local/include/