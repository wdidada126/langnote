# visualstudio
vs下载utf8插件，强制编码为utf8

CMakeSettings.json 是 Visual Studio 特有的配置文件，用于管理 CMake 项目的构建配置。让我详细解释它的作用和与 CMakePresets.json 的区别：
1. CMakeSettings.json 的作用
1.1 主要功能
• Visual Studio 专用：只在 VS 中生效
• 配置管理：定义不同的构建配置（Debug/Release）
• 环境设置：设置环境变量、工具链等
• CMake 参数：传递参数给 CMake
1.2 典型结构
{
  "configurations": [
    {
      "name": "x64-Debug",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Debug",
      "buildRoot": "${projectDir}\\out\\build\\${name}",
      "installRoot": "${projectDir}\\out\\install\\${name}",
      "cmakeExecutable": "cmake.exe",
      "variables": [
        {
          "name": "LLVM_DIR",
          "value": "C:/LLVM/lib/cmake/llvm",
          "type": "PATH"
        }
      ]
    }
  ]
}


2. CMakeSettings.json vs CMakePresets.json
2.1 对比表格
特性 CMakeSettings.json CMakePresets.json
适用范围 Visual Studio 专用 跨平台（CMake 3.19+）
标准化 Microsoft 私有格式 CMake 官方标准
兼容性 只适用于 VS 适用于所有支持 CMake 的 IDE
功能 基础配置管理 完整的预设系统
2.2 实际使用场景
• 只用 Visual Studio：使用 CMakeSettings.json
• 多平台/多 IDE：使用 CMakePresets.json
• 混合环境：两者都可以有，但 CMakePresets.json 优先

3. CMakeSettings.json 详细配置
3.1 完整配置示例
{
  "configurations": [
    {
      "name": "x64-Debug",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Debug",
      "buildRoot": "${projectDir}\\out\\build\\${name}",
      "installRoot": "${projectDir}\\out\\install\\${name}",
      "cmakeExecutable": "cmake.exe",
      "inheritEnvironments": [ "msvc_x64_x64" ],
      "variables": [
        {
          "name": "CMAKE_BUILD_TYPE",
          "value": "Debug",
          "type": "STRING"
        },
        {
          "name": "LLVM_DIR",
          "value": "C:/LLVM/lib/cmake/llvm",
          "type": "PATH"
        },
        {
          "name": "CMAKE_TOOLCHAIN_FILE",
          "value": "D:/vcpkg/scripts/buildsystems/vcpkg.cmake",
          "type": "PATH"
        }
      ],
      "env": {
        "VCPKG_ROOT": "D:/vcpkg",
        "PATH": "C:/LLVM/bin;%PATH%"
      }
    },
    {
      "name": "x64-Release",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Release",
      "buildRoot": "${projectDir}\\out\\build\\${name}",
      "inheritEnvironments": [ "msvc_x64_x64" ],
      "variables": [
        {
          "name": "CMAKE_BUILD_TYPE",
          "value": "Release",
          "type": "STRING"
        }
      ]
    }
  ]
}
3.2 关键字段说明
{
  "configurations": [
    {
      "name": "配置名称",                    // 显示在 VS 下拉列表中
      "generator": "Visual Studio 版本",     // CMake 生成器
      "configurationType": "Debug/Release", // 构建类型
      "buildRoot": "构建目录路径",           // 构建产物目录
      "inheritEnvironments": ["环境名"],     // 继承 VS 环境
      "variables": [                        // CMake 变量
        {
          "name": "变量名",
          "value": "变量值", 
          "type": "STRING/PATH"
        }
      ],
      "env": {                             // 环境变量
        "变量名": "值"
      }
    }
  ]
}

4. 在 Visual Studio 中的使用
4.1 创建和编辑
1. 自动创建：在 VS 中打开 CMake 项目时自动生成
2. 手动创建：在项目根目录创建 CMakeSettings.json
3. 编辑方式：VS 提供图形化编辑器
4.2 图形化界面
在 Visual Studio 中：
1. 解决方案资源管理器 → 右键项目
2. CMake 设置 → 打开图形化编辑器
3. 添加配置 → 选择预设或自定义

5. 实际项目示例
5.1 LLVM项目配置
{
  "configurations": [
    {
      "name": "Windows-LLVM-Debug",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Debug",
      "buildRoot": "${projectDir}\\build\\debug",
      "inheritEnvironments": [ "msvc_x64_x64" ],
      "variables": [
        {
          "name": "LLVM_DIR",
          "value": "C:/LLVM/lib/cmake/llvm",
          "type": "PATH"
        },
        {
          "name": "CMAKE_TOOLCHAIN_FILE",
          "value": "D:/vcpkg/scripts/buildsystems/vcpkg.cmake",
          "type": "PATH"
        }
      ],
      "cmakeCommandArgs": "-DCMAKE_CXX_STANDARD=17",
      "buildCommandArgs": "--config Debug",
      "ctestCommandArgs": ""
    },
    {
      "name": "Windows-LLVM-Release",
      "generator": "Visual Studio 17 2022", 
      "configurationType": "Release",
      "buildRoot": "${projectDir}\\build\\release",
      "inheritEnvironments": [ "msvc_x64_x64" ],
      "variables": [
        {
          "name": "LLVM_DIR",
          "value": "C:/LLVM/lib/cmake/llvm",
          "type": "PATH"
        }
      ]
    }
  ]
}

5.2 多配置项目
{
  "configurations": [
    {
      "name": "MSVC-Debug",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Debug",
      "buildRoot": "${projectDir}\\build\\msvc-debug"
    },
    {
      "name": "MSVC-Release", 
      "generator": "Visual Studio 17 2022",
      "configurationType": "Release",
      "buildRoot": "${projectDir}\\build\\msvc-release"
    },
    {
      "name": "Clang-Debug",
      "generator": "Ninja",
      "configurationType": "Debug", 
      "buildRoot": "${projectDir}\\build\\clang-debug",
      "variables": [
        {
          "name": "CMAKE_C_COMPILER",
          "value": "clang",
          "type": "STRING"
        },
        {
          "name": "CMAKE_CXX_COMPILER", 
          "value": "clang++",
          "type": "STRING"
        }
      ]
    }
  ]
}

6. 与 CMakePresets.json 的转换
6.1 等效配置对比
CMakeSettings.json:
{
  "configurations": [
    {
      "name": "x64-Debug",
      "generator": "Visual Studio 17 2022",
      "configurationType": "Debug",
      "buildRoot": "${projectDir}\\build\\debug"
    }
  ]
}
等效的 CMakePresets.json:
{
  "version": 3,
  "configurePresets": [
    {
      "name": "x64-debug",
      "displayName": "x64 Debug",
      "generator": "Visual Studio 17 2022",
      "binaryDir": "${sourceDir}/build/debug",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    }
  ]
}

6.2 迁移指南
如果要迁移到 CMakePresets.json：
1. 重命名字段：
   • buildRoot → binaryDir
   • configurationType → cacheVariables.CMAKE_BUILD_TYPE
2. 转换变量：
   // CMakeSettings.json
   "variables": [
     { "name": "LLVM_DIR", "value": "C:/LLVM/lib/cmake/llvm" }
   ]
   // CMakePresets.json  
   "cacheVariables": {
     "LLVM_DIR": "C:/LLVM/lib/cmake/llvm"
   }
   
7. 实际使用建议
7.1 何时使用 CMakeSettings.json
• 纯 Visual Studio 环境
• 简单的项目配置
• 需要图形化配置界面
7.2 何时使用 CMakePresets.json
• 跨平台开发
• 多 IDE 支持（CLion、VS Code、VS）
• 复杂的配置需求
• 团队协作项目

7.3 推荐策略
// 项目根目录结构
project/
├── CMakeLists.txt
├── CMakePresets.json          # 主要配置（跨平台）
└── CMakeSettings.json         # 可选（VS 特定优化）

8. 故障排除
8.1 常见问题
1. 配置不生效：检查 JSON 语法错误
2. 环境变量问题：使用 inheritEnvironments
3. 路径问题：使用 ${projectDir} 等变量
8.2 调试技巧
在 VS 中：
1. 输出窗口 → 查看 CMake 输出
2. CMake 缓存 → 查看实际使用的变量值
3. 重新生成缓存：删除 build 目录重新配置
总结
CMakeSettings.json 是 Visual Studio 的专属配置工具，适合：
• 简单的 VS 项目
• 图形化配置需求
• 单平台开发
对于现代 CMake 项目，推荐使用 CMakePresets.json，因为它：
• 是官方标准
• 支持跨平台
• 功能更强大
• 未来兼容性好

如果你的项目主要在 Visual Studio 中开发，两者都可以使用，但 CMakePresets.json 是更面向未来的选择。

vs 17.10.5
最好的IDE
Visual Studio 使用Cmake
https://github.com/edidada/VSCMakeProject

生成
compile_commands.json
对于 Visual Studio，你可以安装 "CMake Tools for Visual Studio" 扩展，然后在项目设置中启用 "Generate CMake options" 选项。这将在构建过程中自动生成compile_commands.json文件。

1> 环境设置:
1>     CommandPromptType=Native
1>     DevEnvDir=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\
1>     ExtensionSdkDir=C:\Program Files (x86)\Microsoft SDKs\Windows Kits\10\ExtensionSDKs
1>     EXTERNAL_INCLUDE=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\include;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\ATLMFC\include;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\VS\include;C:\Program Files (x86)\Windows Kits\10\include\10.0.22621.0\ucrt;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\um;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\shared;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\winrt;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\cppwinrt;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\include\um
1>     Framework40Version=v4.0
1>     FrameworkDir=C:\Windows\Microsoft.NET\Framework64\
1>     FrameworkDir64=C:\Windows\Microsoft.NET\Framework64\
1>     FrameworkVersion=v4.0.30319
1>     FrameworkVersion64=v4.0.30319
1>     FSHARPINSTALLDIR=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\FSharp\Tools
1>     INCLUDE=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\include;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\ATLMFC\include;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\VS\include;C:\Program Files (x86)\Windows Kits\10\include\10.0.22621.0\ucrt;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\um;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\shared;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\winrt;C:\Program Files (x86)\Windows Kits\10\\include\10.0.22621.0\\cppwinrt;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\include\um
1>     LIB=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\ATLMFC\lib\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\lib\x64;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\lib\um\x64;C:\Program Files (x86)\Windows Kits\10\lib\10.0.22621.0\ucrt\x64;C:\Program Files (x86)\Windows Kits\10\\lib\10.0.22621.0\\um\x64
1>     LIBPATH=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\ATLMFC\lib\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\lib\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\lib\x86\store\references;C:\Program Files (x86)\Windows Kits\10\UnionMetadata\10.0.22621.0;C:\Program Files (x86)\Windows Kits\10\References\10.0.22621.0;C:\Windows\Microsoft.NET\Framework64\v4.0.30319
1>     NETFXSDKDir=C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\
1>     Path=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\bin\HostX64\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VC\VCPackages;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\TestWindow;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\bin\Roslyn;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Team Tools\Performance Tools\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Team Tools\Performance Tools;C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\FSharp\Tools;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Team Tools\DiagnosticsHub\Collector;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\Extensions\Microsoft\CodeCoverage.Console;C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\\x64;C:\Program Files (x86)\Windows Kits\10\bin\\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\\MSBuild\Current\Bin\amd64;C:\Windows\Microsoft.NET\Framework64\v4.0.30319;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\;D:\dev_tools\Conan\conan;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;D:\apache-maven-3.6.1\bin;D:\Java\jdk-14.0.1\bin;C:\Program Files (x86)\NetSarang\Xshell 7\;C:\Program Files\Docker\Docker\resources\bin;D:\Program\ripgrep-12.1.0-x86_64-pc-windows-gnu;C:\Program Files\Intel\WiFi\bin\;C:\Program Files\Common Files\Intel\WirelessCommon\;D:\dev_tools\gradle-6.5\bin;C:\Program Files\Microsoft SQL Server\150\Tools\Binn\;C:\Python312\;C:\Python312\Scripts\;C:\Program Files\dotnet\;C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\;D:\git\github\vcpkg;D:\Program Files\CMake\bin;C:\Program Files\TortoiseGit\bin;C:\Program Files\GitHub CLI\;D:\dev_tools\bazelisk;D:\dev_tools\bazel;C:\Program Files\7-Zip;C:\Program Files\nodejs\;C:\ProgramData\chocolatey\bin;C:\Users\edida\AppData\Roaming\npm;C:\Users\edida\AppData\Local\Programs\CLion\bin\ninja\win\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\bin\Hostx64\x64;D:\dev_tools\mingw\bin;C:\Strawberry\c\bin;C:\Strawberry\perl\site\bin;C:\Strawberry\perl\bin;D:\dev_tools\privoxy_3.0.34;C:\Program Files\OpenSSH-Win64;C:\Program Files\Meld\;C:\Program Files\Graphviz\bin;C:\Users\edida\AppData\Roaming\Python\Python312\Scripts;E:\apache-ant-1.10.5\bin;C:\Program Files (x86)\WinMerge;C:\Program Files\Git\cmd;C:\Program Files\LLVM\bin;C:\Program Files\PowerShell\7\;C:\Program Files\CMake\bin;C:\Users\edida\scoop\shims;C:\Users\edida\.cargo\bin;C:\Program Files\Conan\conan;C:\Users\edida\AppData\Local\Microsoft\WindowsApps;C:\Users\edida\AppData\Local\Programs\Microsoft VS Code\bin;C:\Users\edida\.dotnet\tools;C:\Users\edida\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\edida\AppData\Local\gitkraken\bin;C:\Users\edida\xmake;C:\Users\edida\AppData\Local\Programs\oh-my-posh\bin;C:\Program Files\JetBrains\CLion 2024.1.5\bin;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VC\Linux\bin\ConnectionManagerExe;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\vcpkg
1>     PROMPT=$P$G
1>     UCRTVersion=10.0.22621.0
1>     UniversalCRTSdkDir=C:\Program Files (x86)\Windows Kits\10\
1>     VCIDEInstallDir=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VC\
1>     VCINSTALLDIR=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\
1>     VCPKG_ROOT=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\vcpkg
1>     VCToolsInstallDir=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\
1>     VCToolsRedistDir=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Redist\MSVC\14.38.33130\
1>     VCToolsVersion=14.38.33130
1>     VS170COMNTOOLS=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\
1>     VSCMD_ARG_app_plat=Desktop
1>     VSCMD_ARG_HOST_ARCH=x64
1>     VSCMD_ARG_no_logo=1
1>     VSCMD_ARG_TGT_ARCH=x64
1>     VSCMD_DEBUG=5 
1>     VSCMD_VER=17.8.2
1>     VSINSTALLDIR=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\
1>     WindowsLibPath=C:\Program Files (x86)\Windows Kits\10\UnionMetadata\10.0.22621.0;C:\Program Files (x86)\Windows Kits\10\References\10.0.22621.0
1>     WindowsSdkBinPath=C:\Program Files (x86)\Windows Kits\10\bin\
1>     WindowsSdkDir=C:\Program Files (x86)\Windows Kits\10\
1>     WindowsSDKLibVersion=10.0.22621.0\
1>     WindowsSdkVerBinPath=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\
1>     WindowsSDKVersion=10.0.22621.0\
1>     WindowsSDK_ExecutablePath_x64=C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\
1>     WindowsSDK_ExecutablePath_x86=C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\
1>     __DOTNET_ADD_64BIT=1
1>     __DOTNET_PREFERRED_BITNESS=64
1>     __VSCMD_PREINIT_PATH=D:\dev_tools\Conan\conan;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;D:\apache-maven-3.6.1\bin;D:\Java\jdk-14.0.1\bin;C:\Program Files (x86)\NetSarang\Xshell 7\;C:\Program Files\Docker\Docker\resources\bin;D:\Program\ripgrep-12.1.0-x86_64-pc-windows-gnu;C:\Program Files\Intel\WiFi\bin\;C:\Program Files\Common Files\Intel\WirelessCommon\;D:\dev_tools\gradle-6.5\bin;C:\Program Files\Microsoft SQL Server\150\Tools\Binn\;C:\Python312\;C:\Python312\Scripts\;C:\Program Files\dotnet\;C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\;D:\git\github\vcpkg;D:\Program Files\CMake\bin;C:\Program Files\TortoiseGit\bin;C:\Program Files\GitHub CLI\;D:\dev_tools\bazelisk;D:\dev_tools\bazel;C:\Program Files\7-Zip;C:\Program Files\nodejs\;C:\ProgramData\chocolatey\bin;C:\Users\edida\AppData\Roaming\npm;C:\Users\edida\AppData\Local\Programs\CLion\bin\ninja\win\x64;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\bin\Hostx64\x64;D:\dev_tools\mingw\bin;C:\Strawberry\c\bin;C:\Strawberry\perl\site\bin;C:\Strawberry\perl\bin;D:\dev_tools\privoxy_3.0.34;C:\Program Files\OpenSSH-Win64;C:\Program Files\Meld\;C:\Program Files\Graphviz\bin;C:\Users\edida\AppData\Roaming\Python\Python312\Scripts;E:\apache-ant-1.10.5\bin;C:\Program Files (x86)\WinMerge;C:\Program Files\Git\cmd;C:\Program Files\LLVM\bin;C:\Program Files\PowerShell\7\;C:\Program Files\CMake\bin;C:\Users\edida\scoop\shims;C:\Users\edida\.cargo\bin;C:\Program Files\Conan\conan;C:\Users\edida\AppData\Local\Microsoft\WindowsApps;C:\Users\edida\AppData\Local\Programs\Microsoft VS Code\bin;C:\Users\edida\.dotnet\tools;C:\Users\edida\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\edida\AppData\Local\gitkraken\bin;C:\Users\edida\xmake;C:\Users\edida\AppData\Local\Programs\oh-my-posh\bin;C:\Program Files\JetBrains\CLion 2024.1.5\bin
1>     SystemDrive=C:
1>     ProgramFiles(x86)=C:\Program Files (x86)
1>     ProgramW6432=C:\Program Files
1>     ChocolateyInstall=C:\ProgramData\chocolatey
1>     PROCESSOR_IDENTIFIER=Intel64 Family 6 Model 61 Stepping 4, GenuineIntel
1>     POWERSHELL_DISTRIBUTION_CHANNEL=MSI:Windows 10 Pro
1>     TMP=C:\Users\edida\AppData\Local\Temp
1>     ALLUSERSPROFILE=C:\ProgramData
1>     PkgDefApplicationConfigFile=C:\Users\edida\AppData\Local\Microsoft\VisualStudio\17.0_f2770245\devenv.exe.config
1>     USERPROFILE=C:\Users\edida
1>     PROCESSOR_REVISION=3d04
1>     ChocolateyLastPathUpdate=133509803318575862
1>     FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
1>     FPS_BROWSER_USER_PROFILE_STRING=Default
1>     LOGONSERVER=\\DESKTOP-DAF8ST0
1>     TEMP=C:\Users\edida\AppData\Local\Temp
1>     USERNAME=edida
1>     SystemRoot=C:\Windows
1>     VSSKUEDITION=Enterprise
1>     CWRSYNC_HOME=C:\ProgramData\chocolatey\lib\rsync\tools\cwrsync_6.2.0_x64_free
1>     OneDrive=C:\Users\edida\OneDrive
1>     PROCESSOR_ARCHITECTURE=AMD64
1>     VBOX_MSI_INSTALL_PATH=C:\Program Files\Oracle\VirtualBox\
1>     CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
1>     ProgramData=C:\ProgramData
1>     GRADLE_USER_HOME=G:\gradle\cache
1>     VSAPPIDDIR=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\
1>     HOMEPATH=\Users\edida
1>     GRADLE_HOME=D:\dev_tools\gradle-6.5
1>     COMPUTERNAME=DESKTOP-DAF8ST0
1>     ServiceHubLogSessionKey=B42E5B8F
1>     M2_HOME=D:\apache-maven-3.6.1
1>     POSH_INSTALLER=ws
1>     VS_Perf_Session_GCHeapCount=2
1>     ThreadedWaitDialogDpiContext=-4
1>     GCExpConfigUsedInSession=3
1>     CommonProgramFiles=C:\Program Files\Common Files
1>     VisualStudioDir=C:\Users\edida\Documents\Visual Studio 2022
1>     DriverData=C:\Windows\System32\Drivers\DriverData
1>     HOMEDRIVE=C:
1>     windir=C:\Windows
1>     NUMBER_OF_PROCESSORS=4
1>     OS=Windows_NT
1>     ProgramFiles=C:\Program Files
1>     ComSpec=C:\Windows\system32\cmd.exe
1>     PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW
1>     VSLANG=2052
1>     JAVA_HOME=D:\Java\jdk-11.0.4
1>     PSModulePath=%ProgramFiles%\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
1>     APPDATA=C:\Users\edida\AppData\Roaming
1>     USERDOMAIN=DESKTOP-DAF8ST0
1>     PROCESSOR_LEVEL=6
1>     LOCALAPPDATA=C:\Users\edida\AppData\Local
1>     VisualStudioVersion=17.0
1>     CommonProgramW6432=C:\Program Files\Common Files
1>     VisualStudioEdition=Microsoft Visual Studio Enterprise 2022
1>     POSH_THEMES_PATH=C:\Users\edida\AppData\Local\Programs\oh-my-posh\themes
1>     CLion=C:\Program Files\JetBrains\CLion 2024.1.5\bin;
1>     USERDOMAIN_ROAMINGPROFILE=DESKTOP-DAF8ST0
1>     PUBLIC=C:\Users\Public
1>     VSAPPIDNAME=devenv.exe
1>     MSBuildLoadMicrosoftTargetsReadOnly=true
1> 命令行: "C:\Windows\system32\cmd.exe" /c "%SYSTEMROOT%\System32\chcp.com 65001 >NUL && "c:\program files\microsoft visual studio\2022\enterprise\common7\ide\commonextensions\microsoft\cmake\CMake\bin\cmake.exe"  -G "Ninja"  -DCMAKE_C_COMPILER:STRING="cl.exe" -DCMAKE_CXX_COMPILER:STRING="cl.exe" -DCMAKE_BUILD_TYPE:STRING="Debug" -DCMAKE_INSTALL_PREFIX:PATH="D:/git/github/VSCMakeProject/out/install/x64-debug"   -DCMAKE_MAKE_PROGRAM="c:\program files\microsoft visual studio\2022\enterprise\common7\ide\commonextensions\microsoft\cmake\Ninja\ninja.exe" "D:\git\github\VSCMakeProject" 2>&1"
1> 工作目录: D:/git/github/VSCMakeProject/out/build/x64-debug
1> [CMake] -- Configuring done (0.2s)
1> [CMake] -- Generating done (0.0s)
1> [CMake] -- Build files have been written to: D:/git/github/VSCMakeProject/out/build/x64-debug