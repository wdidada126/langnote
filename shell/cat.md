# cat

# 创建 plist 文件
cat > ~/Library/LaunchAgents/com.github.podman.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.github.podman</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/opt/podman/bin/podman</string>
        <string>system</string>
        <string>service</string>
        <string>--time=0</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/podman.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/podman-error.log</string>
</dict>
</plist>
EOF
