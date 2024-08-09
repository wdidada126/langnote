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

