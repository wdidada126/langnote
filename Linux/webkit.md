webkit


git clone -b WebKit-7617.2.4.11.8 https://github.com/WebKit/WebKit.git WebKit
cd WebKit
cmake -DPORT=GTK -DCMAKE_BUILD_TYPE=RelWithDebInfo -GNinja
ninja
sudo ninja install
Tools/gtk/install-dependencies
Tools/Scripts/update-webkitgtk-libs
Tools/Scripts/build-webkit --gtk --debug

You need to install flatpak >= 1.4.4 to be able to use the '/home/runner/work/github_codespaces_compile/github_codespaces_compile/WebKit/Tools/Scripts/webkit-flatpak' script.

Flatpak 是一个用于打包、分发和运行应用程序的软件交付和管理系统。它提供了一种跨 Linux 发行版的通用应用程序打包格式，并提供了安全隔离的运行环境。Flatpak 的目标是解决 Linux 应用程序的依赖性和兼容性问题，使开发人员能够更轻松地为 Linux 用户提供应用程序。

Flatpak 使用一种称为 Flatpak 包（或 Flatpak 存储库）的打包格式。该格式允许将应用程序及其依赖项打包为一个独立的软件包，该软件包可以在各种 Linux 发行版上运行。这种打包格式使用了隔离技术，称为沙盒，以确保应用程序在运行时与系统和其他应用程序相互隔离，从而提供更高的安全性和稳定性。

Flatpak 还提供了一个中央存储库（Flathub），其中包含了许多常见的应用程序，用户可以从中下载和安装。此外，开发人员也可以创建自己的 Flatpak 存储库，以便分发他们自己的应用程序。

使用 Flatpak，用户可以在不同的 Linux 发行版之间轻松地安装和运行应用程序，而无需担心依赖关系或版本冲突。它提供了一种统一的方式来获取和管理应用程序，使得软件的安装和更新变得更加简单和可靠。
