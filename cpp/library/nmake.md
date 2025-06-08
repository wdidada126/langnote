# nmake

https://learn.microsoft.com/zh-cn/cpp/build/reference/nmake-reference?view=msvc-170

Microsoft程序维护实用工具(NMAKE.EXE)是Visual Studio随附的命令行工具。它基于一个描述文件中包含的命令生成项目，该文件通常称为“生成文件”。

NMAKE必须在“开发人员命令提示”窗口中运行。开发人员命令提示窗口具有为工具、库设置的环境变量，并且包括在命令行上生成所需的文件路径。有关如何打开“开发人员命令提示”窗口的详细信息，请参阅通过命令行使用MSVC工具集。

命令文件	主机和目标体系结构
vcvars32.bat	使用32位x86本机工具生成32位x86代码。
vcvars64.bat	使用64位x64本机工具生成64位x64代码。
vcvarsx86_amd64.bat	使用32位x86本机兼容工具生成64位x64代码。
vcvarsamd64_x86.bat	使用64位x64本机兼容工具生成32位x86代码。
vcvarsx86_arm.bat	使用32位x86本机兼容工具生成ARM代码。
vcvarsamd64_arm.bat	使用64位x64本机兼容工具生成ARM代码。
vcvarsx86_arm64.bat	使用32位x86本机兼容工具生成ARM64代码。
vcvarsamd64_arm64.bat	使用64位x64本机兼容工具生成ARM64代码。
vcvarsall.bat	使用参数指定主机和目标体系结构、WindowsSDK和平台选项。有关支持的选项列表，请使用/help参数进行调用。

若要在命令提示符处生成C/C++项目，可使用Visual Studio提供的以下命令行工具：

CL
使用编译器(cl.exe)可编译源代码文件，并将其链接到应用、库和DLL中。

Link
使用链接器(link.exe)可将已编译的对象文件和库链接到应用和DLL中。

MSBuild
使用MSBuild(msbuild.exe)和项目文件(.vcxproj)来配置生成并调用工具集，而无需加载Visual Studio IDE。这相当于在Visual Studio IDE 中运行“生成”项目或“生成解决方案”命令。当你在命令行进行生成时，MSBuild比IDE更具优势。你无需在所有的生成服务器和生成管道上安装完整的IDE。这可避免IDE的额外开销。MSBuild在容器化生成环境中运行，并支持二进制记录器。

DEVENV
将DEVENV(devenv.exe)与命令行开关（例如，/Build或/Clean）结合使用，可在不显示Visual Studio IDE 的情况下执行某些生成命令。

CMake
CMake(cmake.exe)是一种跨平台开源工具，用于定义在多个平台上运行的生成过程。CMake可以为它支持的平台（例如MSBuild和Make）配置和控制本机生成工具。有关CMake的详细信息，请参阅CMake文档。

NMAKE
使用NMAKE(nmake.exe)来通过使用传统的生成文件以生成C++项目。

VC6通过什么组织代码的？
VC6（Visual C++ 6.0）通过项目（Project）来组织代码。在VC6中，开发一个C或C++程序时，首先需要创建一个项目，然后在该项目中添加源文件（如.c或.cpp文件）。项目文件（如.dsp和.dsw文件）用于保存当前工程的信息，包括编译参数、包含的源文件等。通过这种方式，VC6能够管理多个源文件，以及它们之间的依赖关系，从而方便地进行编译、链接和调试。

具体来说，项目的创建和管理涉及以下几个步骤：

新建项目：通过“文件”菜单选择“新建”，然后选择“Win32 Console Application”等项目类型，填写项目名称和路径，创建项目。
添加源文件：在项目创建后，可以通过“文件”菜单选择“新建”来添加新的源文件（如.c或.cpp文件），并将其添加到项目中。
编写代码：在源文件中编写C或C++代码。
编译和链接：使用VC6的编译和链接功能，将源代码编译成目标代码，并将目标代码与必要的库文件链接，生成可执行文件（.exe）。
调试和运行：使用VC6的调试工具来查找和修复代码中的错误，然后运行程序查看结果。
MSBuild和nmake是什么背景下产生的？
MSBuild（Microsoft Build Engine）是Microsoft推出的一个编译平台，它是.NET Framework的一部分，用于自动化构建应用程序和库。MSBuild的引入主要是为了解决早期构建工具（如nmake）在.NET环境下的不足，提供一个更加灵活和强大的构建系统。MSBuild使用XML格式的项目文件（如.csproj、.vbproj等），能够更清晰地描述项目的结构和构建过程，支持复杂的依赖关系和自定义任务。

nmake是Microsoft早期推出的一个命令行工具，用于根据makefile文件中的指令来自动化构建过程。Makefile文件是一种文本文件，其中包含了一系列的规则和依赖关系，告诉nmake如何编译和链接程序。然而，随着软件项目规模的扩大和复杂度的增加，makefile文件的编写和维护变得越来越困难。此外，makefile的语法和规则也相对固定，难以适应不同的构建需求。因此，Microsoft推出了MSBuild作为nmake的替代品，以提供更加灵活和强大的构建能力。

综上所述，MSBuild和nmake都是在不同的背景下产生的构建工具，它们各自具有不同的特点和优势。随着软件开发技术的不断发展，构建工具也在不断演进和完善。
