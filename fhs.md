# fhs

https://github.com/v2fly/fhs-install-v2ray


installed: /usr/local/bin/v2ray
installed: /usr/local/bin/v2ctl
installed: /usr/local/share/v2ray/geoip.dat
installed: /usr/local/share/v2ray/geosite.dat
installed: /usr/local/etc/v2ray/config.json
installed: /var/log/v2ray/
installed: /var/log/v2ray/access.log
installed: /var/log/v2ray/error.log
installed: /etc/systemd/system/v2ray.service
installed: /etc/systemd/system/v2ray@.service

bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)


 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--100 21647  100 21647    0     0   116k      0 --:--:-- --:--:-- --:--:--  117k
info: Installing V2Ray v4.45.2 for x86_64
Downloading V2Ray archive: https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 13.1M  100 13.1M    0     0  40.4M      0 --:--:-- --:--:-- --:--:-- 40.4M
Downloading verification file for V2Ray archive: https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip.dgst
info: Extract the V2Ray package to /tmp/tmp.QM0qs3LM48 and prepare it for installation.
info: Systemd service files have been installed successfully!
warning: The following are the actual parameters for the v2ray service startup.
warning: Please make sure the configuration file path is correctly set.
~~~~~~~~~~~~~~~~
[Unit]
Description=V2Ray Service
Documentation=https://www.v2fly.org/
After=network.target nss-lookup.target

[Service]
User=nobody
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/usr/local/bin/v2ray -config /usr/local/etc/v2ray/config.json
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
# In case you have a good reason to do so, duplicate this file in the same directory and make your customizes there.
# Or all changes you made will be lost!  # Refer: https://www.freedesktop.org/software/systemd/man/systemd.unit.html
[Service]
ExecStart=
ExecStart=/usr/local/bin/v2ray -config /usr/local/etc/v2ray/config.json
~~~~~~~~~~~~~~~~
warning: The systemd version on the current operating system is too low.
warning: Please consider to upgrade the systemd or the operating system.

installed: /usr/local/bin/v2ray
installed: /usr/local/bin/v2ctl
installed: /usr/local/share/v2ray/geoip.dat
installed: /usr/local/share/v2ray/geosite.dat
installed: /usr/local/etc/v2ray/config.json
installed: /var/log/v2ray/
installed: /var/log/v2ray/access.log
installed: /var/log/v2ray/error.log
installed: /etc/systemd/system/v2ray.service
installed: /etc/systemd/system/v2ray@.service
removed: /tmp/tmp.QM0qs3LM48
info: V2Ray v4.45.2 is installed.
You may need to execute a command to remove dependent software: apt purge curl unzip
Please execute the command: systemctl enable v2ray; systemctl start v2ray
root@67:~# systemctl start v2ray
root@67:~# systemctl enable v2ray
Created symlink from /etc/systemd/system/multi-user.target.wants/v2ray.service to /etc/systemd/system/v2ray.service.
root@67:~# systemctl status v2ray
● v2ray.service - V2Ray Service
   Loaded: loaded (/etc/systemd/system/v2ray.service; enabled)
  Drop-In: /etc/systemd/system/v2ray.service.d
           └─10-donot_touch_single_conf.conf
   Active: active (running) since Wed 2022-07-20 23:23:01 EDT; 39s ago
     Docs: https://www.v2fly.org/
 Main PID: 12644 (v2ray)
   CGroup: /system.slice/v2ray.service
           └─12644 /usr/local/bin/v2ray -config /usr/local/etc/v2ray/...

Jul 20 23:23:01 67.209.189.193 systemd[1]: [/etc/systemd/system/v2ray...
Jul 20 23:23:01 67.209.189.193 systemd[1]: Starting V2Ray Service...
Jul 20 23:23:01 67.209.189.193 systemd[1]: Started V2Ray Service.
Jul 20 23:23:01 67.209.189.193 v2ray[12644]: V2Ray 4.45.2 (V2Fly, a c...
Jul 20 23:23:01 67.209.189.193 v2ray[12644]: A unified platform for a...
Jul 20 23:23:01 67.209.189.193 v2ray[12644]: 2022/07/20 23:23:01 [Inf...
Jul 20 23:23:01 67.209.189.193 v2ray[12644]: 2022/07/20 23:23:01 [War...
Jul 20 23:23:29 67.209.189.193 systemd[1]: [/etc/systemd/system/v2ray...
Hint: Some lines were ellipsized, use -l to show in full.
root@67:~# 



https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard