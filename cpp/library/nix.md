# nix

https://github.com/NixOS

不支持windows

https://nixos.org/

Nix 是一个完全的软件包管理器，可进行独立的包升级而不会影响其他包，而且可以回滚到以前的版本。同一个软件允许同时存在多个版本。
Nixpkgs 包含了大量的软件包，可通过 Nix 包管理器进行安装。
NixOS 是一个基于 Nix 的 Linux 发行版，支持原子升级、回滚、多用户包管理，以及可轻松的在不同机器间同步配置。
Hydra 是一个基于 Nix 的持续构建系统。

https://github.com/NixOS

```shell
cd ~
wdidada@LAPTOP-wdidada:~$ sh <(curl -L https://nixos.org/nix/install) --daemon
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:10 --:--:--     0curl: (6) Could not resolve host: releases.nixos.org
wdidada@LAPTOP-wdidada:~$ sh <(curl -L https://nixos.org/nix/install) --daemon
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  4267  100  4267    0     0   2600      0  0:00:01  0:00:01 --:--:-- 4166k
downloading Nix 2.26.3 binary tarball for x86_64-linux from 'https://releases.nixos.org/nix/nix-2.26.3/nix-2.26.3-x86_64-linux.tar.xz' to '/tmp/nix-binary-tarball-unpack.40R8pcBYBf'...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 22.6M  100 22.6M    0     0   350k      0  0:01:06  0:01:06 --:--:--  423k
Note: a multi-user installation is possible. See https://nixos.org/manual/nix/stable/installation/installing-binary.html#multi-user-installation
Switching to the Multi-user Installer
Welcome to the Multi-User Nix Installation

This installation tool will set up your computer with the Nix package
manager. This will happen in a few stages:

1. Make sure your computer doesn't already have Nix. If it does, I
   will show you instructions on how to clean up your old install.

2. Show you what I am going to install and where. Then I will ask
   if you are ready to continue.

3. Create the system users (uids [30001..30032]) and groups (gid 30000)
   that the Nix daemon uses to run builds. To create system users
   in a different range, exit and run this tool again with
   NIX_FIRST_BUILD_UID set.

4. Perform the basic installation of the Nix files daemon.

5. Configure your shell to import special Nix Profile files, so you
   can use Nix.

6. Start the Nix daemon.

Would you like to see a more detailed list of what I will do?
[y/n] y


I will:

 - make sure your computer doesn't already have Nix files
   (if it does, I will tell you how to clean them up.)
 - create local users (see the list above for the users I'll make)
 - create a local group (nixbld)
 - install Nix in /nix
 - create a configuration file in /etc/nix
 - set up the "default profile" by creating some Nix-related files in
   /root
 - back up /etc/bash.bashrc to /etc/bash.bashrc.backup-before-nix
 - update /etc/bash.bashrc to include some Nix configuration
 - load and start a service (at /etc/systemd/system/nix-daemon.service
   and /etc/systemd/system/nix-daemon.socket) for nix-daemon

Ready to continue?
[y/n] y


---- let's talk about sudo -----------------------------------------------------
This script is going to call sudo a lot. Every time I do, it'll
output exactly what it'll do, and why.

Just like this:

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo echo

to demonstrate how our sudo prompts look


This might look scary, but everything can be undone by running just a
few commands. I used to ask you to confirm each time sudo ran, but it
was too many times. Instead, I'll just ask you this one time:

Can I use sudo?
[y/n] y

Yay! Thanks! Let's get going!

~~> Checking for artifacts of previous installs
Before I try to install, I'll check for signs Nix already is or has
been installed on this system.

---- Nix config report ---------------------------------------------------------
        Temp Dir:       /tmp/tmp.elgwxotxo1
        Nix Root:       /nix
     Build Users:       32
  Build Group ID:       30000
Build Group Name:       nixbld

build users:
    Username:   UID
     nixbld1:   30001
     nixbld2:   30002
     nixbld3:   30003
     nixbld4:   30004
     nixbld5:   30005
     nixbld6:   30006
     nixbld7:   30007
     nixbld8:   30008
     nixbld9:   30009
     nixbld10:  30010
     nixbld11:  30011
     nixbld12:  30012
     nixbld13:  30013
     nixbld14:  30014
     nixbld15:  30015
     nixbld16:  30016
     nixbld17:  30017
     nixbld18:  30018
     nixbld19:  30019
     nixbld20:  30020
     nixbld21:  30021
     nixbld22:  30022
     nixbld23:  30023
     nixbld24:  30024
     nixbld25:  30025
     nixbld26:  30026
     nixbld27:  30027
     nixbld28:  30028
     nixbld29:  30029
     nixbld30:  30030
     nixbld31:  30031
     nixbld32:  30032

Ready to continue?
[y/n] y


~~> Setting up the build group nixbld

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo groupadd -g 30000 --system nixbld

Create the Nix build group, nixbld

[sudo] password for wdidada:
            Created:    Yes

~~> Setting up the build user nixbld1

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 1 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30001 --password ! nixbld1

Creating the Nix build user, nixbld1

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 1
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld2

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 2 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30002 --password ! nixbld2

Creating the Nix build user, nixbld2

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 2
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld3

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 3 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30003 --password ! nixbld3

Creating the Nix build user, nixbld3

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 3
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld4

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 4 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30004 --password ! nixbld4

Creating the Nix build user, nixbld4

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 4
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld5

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 5 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30005 --password ! nixbld5

Creating the Nix build user, nixbld5

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 5
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld6

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 6 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30006 --password ! nixbld6

Creating the Nix build user, nixbld6

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 6
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld7

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 7 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30007 --password ! nixbld7

Creating the Nix build user, nixbld7

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 7
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld8

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 8 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30008 --password ! nixbld8

Creating the Nix build user, nixbld8

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 8
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld9

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 9 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30009 --password ! nixbld9

Creating the Nix build user, nixbld9

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 9
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld10

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 10 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30010 --password ! nixbld10

Creating the Nix build user, nixbld10

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 10
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld11

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 11 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30011 --password ! nixbld11

Creating the Nix build user, nixbld11

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 11
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld12

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 12 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30012 --password ! nixbld12

Creating the Nix build user, nixbld12

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 12
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld13

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 13 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30013 --password ! nixbld13

Creating the Nix build user, nixbld13

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 13
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld14

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 14 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30014 --password ! nixbld14

Creating the Nix build user, nixbld14

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 14
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld15

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 15 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30015 --password ! nixbld15

Creating the Nix build user, nixbld15

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 15
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld16

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 16 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30016 --password ! nixbld16

Creating the Nix build user, nixbld16

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 16
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld17

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 17 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30017 --password ! nixbld17

Creating the Nix build user, nixbld17

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 17
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld18

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 18 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30018 --password ! nixbld18

Creating the Nix build user, nixbld18

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 18
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld19

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 19 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30019 --password ! nixbld19

Creating the Nix build user, nixbld19

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 19
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld20

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 20 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30020 --password ! nixbld20

Creating the Nix build user, nixbld20

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 20
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld21

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 21 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30021 --password ! nixbld21

Creating the Nix build user, nixbld21

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 21
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld22

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 22 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30022 --password ! nixbld22

Creating the Nix build user, nixbld22

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 22
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld23

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 23 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30023 --password ! nixbld23

Creating the Nix build user, nixbld23

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 23
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld24

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 24 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30024 --password ! nixbld24

Creating the Nix build user, nixbld24

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 24
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld25

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 25 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30025 --password ! nixbld25

Creating the Nix build user, nixbld25

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 25
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld26

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 26 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30026 --password ! nixbld26

Creating the Nix build user, nixbld26

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 26
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld27

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 27 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30027 --password ! nixbld27

Creating the Nix build user, nixbld27

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 27
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld28

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 28 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30028 --password ! nixbld28

Creating the Nix build user, nixbld28

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 28
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld29

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 29 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30029 --password ! nixbld29

Creating the Nix build user, nixbld29

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 29
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld30

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 30 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30030 --password ! nixbld30

Creating the Nix build user, nixbld30

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 30
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld31

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 31 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30031 --password ! nixbld31

Creating the Nix build user, nixbld31

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 31
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the build user nixbld32

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo useradd --home-dir /var/empty --comment Nix build user 32 --gid 30000 --groups nixbld --no-user-group --system --shell /sbin/nologin --uid 30032 --password ! nixbld32

Creating the Nix build user, nixbld32

           Created:     Yes
            Hidden:     Yes
    Home Directory:     /var/empty
              Note:     Nix build user 32
   Logins Disabled:     Yes
  Member of nixbld:     Yes
    PrimaryGroupID:     30000

~~> Setting up the basic directory structure

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo install -dv -m 0755 /nix /nix/var /nix/var/log /nix/var/log/nix /nix/var/log/nix/drvs /nix/var/nix /nix/var/nix/db /nix/var/nix/gcroots /nix/var/nix/profiles /nix/var/nix/temproots /nix/var/nix/userpool /nix/var/nix/daemon-socket /nix/var/nix/gcroots/per-user /nix/var/nix/profiles/per-user

to make the basic directory structure of Nix (part 1)

install: creating directory '/nix'
install: creating directory '/nix/var'
install: creating directory '/nix/var/log'
install: creating directory '/nix/var/log/nix'
install: creating directory '/nix/var/log/nix/drvs'
install: creating directory '/nix/var/nix'
install: creating directory '/nix/var/nix/db'
install: creating directory '/nix/var/nix/gcroots'
install: creating directory '/nix/var/nix/profiles'
install: creating directory '/nix/var/nix/temproots'
install: creating directory '/nix/var/nix/userpool'
install: creating directory '/nix/var/nix/daemon-socket'
install: creating directory '/nix/var/nix/gcroots/per-user'
install: creating directory '/nix/var/nix/profiles/per-user'

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo install -dv -g nixbld -m 1775 /nix/store

to make the basic directory structure of Nix (part 2)

install: creating directory '/nix/store'

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo install -dv -m 0555 /etc/nix

to place the default nix daemon configuration (part 1)

install: creating directory '/etc/nix'

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo install -m 0644 /tmp/tmp.elgwxotxo1/.nix-channels /root/.nix-channels

to set up the default system channel (part 1)


~~> Installing Nix

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo cp -RPp ./store/12nvz309ps508h5f4z61ry590857gqmz-libgit2-1.8.4-lib ./store/1k1bnir265n7jpbmwinj8hiwygnwrw3s-aws-c-common-0.9.27 ./store/1n0b29iid3y0w9i91v9zqdiwnx3inak0-libssh2-1.11.1 ./store/20ky2306yw2ri5ki82bgllr4rwnril21-aws-c-s3-0.6.0 ./store/282klmpdw8vibm1k0qachsnzc7zq522z-libpsl-0.21.5 ./store/2d5spnl8j5r4n1s4bj1zmra7mwx0f1n8-xgcc-13.3.0-libgcc ./store/2r6hkd3p8c0sflhcvd1cy6f3mgy05fmg-aws-sdk-cpp-1.11.336 ./store/2vgwd43vqxm66grkgsy7z1d87z31nzph-brotli-1.1.0-lib ./store/3j0pj54x5299vfhr8r468ay6mjgi051l-boehm-gc-8.2.8 ./store/5ryzwb3h7jp375g30afn8b2gf39f2l1s-aws-c-sdkutils-0.1.16 ./store/6aypxg5iayqzb21sp67m429qhji36m3a-aws-c-auth-0.7.26 ./store/6pqgj71r0850b0cd95yxx0d52zax016i-libunistring-1.2 ./store/78mgbp4sp25zz61agaxnwflw6xi3mm3j-aws-c-compression-0.2.19 ./store/7w8flxyajz0pz0xkxm3fhi6wv0avss92-nix-store-2.26.3 ./store/8pys6a47askf0g75a1k73p3rx2wim7m6-zstd-1.5.6 ./store/acc43l1xnyl7jmx5m9d0h4h173vxlaab-busybox-static-x86_64-unknown-linux-musl-1.36.1 ./store/aygalfgrn7pvxcqc45jw53b9gc29hwzs-nghttp2-1.64.0-lib ./store/b8bl7ks2wfzyy3p7vbbk72jkrwf7c5y3-aws-c-io-0.14.18 ./store/bbd59cqw259149r2ddk4w1q0lr2fch8c-sqlite-3.46.1 ./store/bdpc1864983kf51r3cznbrvnlkv4d9ff-xz-5.6.3 ./store/bzk3q2l71qwhycsip23y6rl5n881la4n-zlib-1.3.1 ./store/f5zq1g323xw7pbl72vnc9i414zwmqbny-boost-1.81.0 ./store/g9hgzjcj9g7hw3c2pzgz271b1g1jgc4w-krb5-1.21.3-lib ./store/gkj66hn5cyi3d761nmcdpj35ngv7h8ph-pcre2-10.44 ./store/hl3iw85v12gh9mwgvr9yfgjgy0rk81hb-bzip2-1.0.8 ./store/ixq7chmml361204anwph16ll2njcf19d-curl-8.11.0 ./store/j8rzqx7farv0w3isp9z943zy437zk02f-gcc-13.3.0-libgcc ./store/k1dsk0zyq43pvi7f76is2rx6l4aphm5z-openssl-3.3.2 ./store/k1yk29dy22fjsa1d48kabkyb23gzjshw-aws-crt-cpp-0.26.12 ./store/kas89ckkzmp0hczkj30gv19awlki6hwr-aws-checksums-0.1.18 ./store/ki28jqabr02w1k3p4h2ky230vzh9k4n8-libsodium-1.0.20 ./store/lzay7jk6yk0h8silizlczd8464rj5ccv-aws-c-mqtt-0.10.5 ./store/m9bq0gx3r1vs7h7myyaffkid3qz4m31n-editline-1.17.1 ./store/mb8l4bdwb03n1s1zxwxi09x4bqprg6qi-lowdown-1.2.0-lib ./store/n0gxk0ys2zgqqz6zcsq8qlv6nv5k6fpj-libarchive-3.7.7-lib ./store/nhd2vp53l6m1xy20534yfpr2v1d9jlvm-aws-c-http-0.8.2 ./store/nmq6s9l9zlym3qjx76zzrqbp05a63y90-attr-2.5.2 ./store/nrl5m466dwdscvavf1nqzdnqhszjyy9n-acl-2.3.2 ./store/nz3rq7n23blcki6y9zk83k9fd86g9ln5-nix-fetchers-2.26.3 ./store/p6k7xp1lsfmbdd731mlglrdj2d66mr82-bash-5.2p37 ./store/pvm8zl5w1mx347cm7s4wp50gihckg89w-nix-main-2.26.3 ./store/pykh94qqyhllkv2wwfrdn0al6w2fzv52-aws-c-cal-0.6.15 ./store/qjfhf5gp6jwh6q0i00cggw0vghqdjww0-libseccomp-2.5.5-lib ./store/qpcddr0rq83g5mkwvxdddj2sgvb39m0x-nix-util-2.26.3 ./store/qwjjm4j652ck9izaid7bz63s4hd5bnha-libidn2-2.3.7 ./store/ryhnwgqzf4znxks9l8rs6hm0915d1d6q-nix-expr-2.26.3 ./store/shg1vgcjxghqxhl0sifwgr0g2zg6bbv7-libxml2-2.13.4 ./store/v0aspi2bg9q9hrf9qrh8qpl5y2wsshmf-nix-flake-2.26.3 ./store/vxhnb0j3kbghwr7xd6cmlhmj8wycrs0l-aws-c-event-stream-0.4.3 ./store/vy8sksf96sfvdnkga0761x2yxyxvbs5f-publicsuffix-list-0-unstable-2024-10-25 ./store/vyv7rca6liiwvz26v3d8b7n04a91p2nw-nix-cmd-2.26.3 ./store/wn7v2vhyyyi6clcyn0s9ixvl7d4d87ic-glibc-2.40-36 ./store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3 ./store/x5lxmydkpbkfwah1nyll7bf0fqhlhsg5-s2n-tls-1.5.5 ./store/x94kpcx52cs705iwlzan0y2h9m0mqqfb-libcpuid-0.7.0 ./store/y2zh06pccwcvz43xwgd8mr8pbqflkqww-nss-cacert-3.107 ./store/ybjcla5bhj8g1y84998pn4a2drfxybkv-gcc-13.3.0-lib ./store/ys6f20b4chzkmfh9ak0hjdp60l0g5abb-keyutils-1.6.3-lib /nix/store/

to copy the basic Nix files to the new store at /nix/store


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo chmod -R ugo-w /nix/store/

to make the new store non-writable at /nix/store

      Alright! We have our first nix at /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo HOME=/root /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3/bin/nix-store --load-db

to load data for the first time in to the Nix Database

      Just finished getting the nix database ready.

~~> Setting up shell profiles: /etc/bashrc /etc/profile.d/nix.sh /etc/zshrc /etc/bash.bashrc /etc/zsh/zshrc

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo touch /etc/bashrc

to create a stub /etc/bashrc which will be updated


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo tee -a /etc/bashrc

extend your /etc/bashrc with nix-daemon settings


# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo touch /etc/profile.d/nix.sh

to create a stub /etc/profile.d/nix.sh which will be updated


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo tee -a /etc/profile.d/nix.sh

extend your /etc/profile.d/nix.sh with nix-daemon settings


# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo touch /etc/zshrc

to create a stub /etc/zshrc which will be updated


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo tee -a /etc/zshrc

extend your /etc/zshrc with nix-daemon settings


# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo cp /etc/bash.bashrc /etc/bash.bashrc.backup-before-nix

to back up your current /etc/bash.bashrc to /etc/bash.bashrc.backup-before-nix


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo tee -a /etc/bash.bashrc

extend your /etc/bash.bashrc with nix-daemon settings


# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix


~~> Setting up shell profiles for Fish with conf.d/nix.fish inside /etc/fish /usr/local/etc/fish /opt/homebrew/etc/fish /opt/local/etc/fish

~~> Setting up the default profile

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo HOME=/root /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3/bin/nix-env -i /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3

to install a bootstrapping Nix in to the default profile

installing 'nix-2.26.3'
building '/nix/store/5afca9ydks0pp5szkwwhi7a6m2zmgk9g-user-environment.drv'...

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo HOME=/root /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3/bin/nix-env -i /nix/store/y2zh06pccwcvz43xwgd8mr8pbqflkqww-nss-cacert-3.107

to install a bootstrapping SSL certificate just for Nix in to the default profile

installing 'nss-cacert-3.107'
building '/nix/store/ilxzpc39hcw5jr229rmajjkyz1a0fym1-user-environment.drv'...

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo HOME=/root NIX_SSL_CERT_FILE=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt /nix/store/x3235311q3n51rppm2y2ycwd7nb3mgpn-nix-2.26.3/bin/nix-channel --update nixpkgs

to update the default channel in the default profile

warning: error: unable to download 'https://nixos.org/channels/nixpkgs-unstable': HTTP error 302 (curl error: Could not resolve hostname); retrying in 263 ms
unpacking 1 channels...

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo install -m 0644 /tmp/tmp.elgwxotxo1/nix.conf /etc/nix/nix.conf

to place the default nix daemon configuration (part 2)


~~> Setting up the nix-daemon systemd service

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo mkdir -p /etc/tmpfiles.d

to create parent of the nix-daemon tmpfiles config


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo ln -sfn /nix/var/nix/profiles/default/lib/tmpfiles.d/nix-daemon.conf /etc/tmpfiles.d/nix-daemon.conf

to create the nix-daemon tmpfiles config


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemd-tmpfiles --create --prefix=/nix/var/nix

to run systemd-tmpfiles once to pick that path up


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemctl link /nix/var/nix/profiles/default/lib/systemd/system/nix-daemon.service

to set up the nix-daemon service

Created symlink /etc/systemd/system/nix-daemon.service → /nix/var/nix/profiles/default/lib/systemd/system/nix-daemon.service.

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemctl enable /nix/var/nix/profiles/default/lib/systemd/system/nix-daemon.socket

to set up the nix-daemon socket service

Created symlink /etc/systemd/system/sockets.target.wants/nix-daemon.socket → /nix/var/nix/profiles/default/lib/systemd/system/nix-daemon.socket.
Created symlink /etc/systemd/system/nix-daemon.socket → /nix/var/nix/profiles/default/lib/systemd/system/nix-daemon.socket.

---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemctl daemon-reload

to load the systemd unit for nix-daemon


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemctl start nix-daemon.socket

to start the nix-daemon.socket


---- sudo execution ------------------------------------------------------------
I am executing:

    $ sudo systemctl restart nix-daemon.service

to start the nix-daemon.service

Alright! We're done!
Try it! Open a new terminal, and type:

  $ nix-shell -p nix-info --run "nix-info -m"

Thank you for using this installer. If you have any feedback or need
help, don't hesitate:

You can open an issue at
https://github.com/NixOS/nix/issues/new?labels=installer&template=installer.md

Or get in touch with the community: https://nixos.org/community

---- Reminders -----------------------------------------------------------------
[ 1 ]
Nix won't work in active shell sessions until you restart them.
```


