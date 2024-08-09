# chocolatey

Extracting 64-bit C:\ProgramData\chocolatey\lib\curl\tools\curl-8.9.0_1-win64-mingw.zip to C:\ProgramData\chocolatey\lib\curl\tools...
C:\ProgramData\chocolatey\lib\curl\tools
 ShimGen has successfully created a shim for curl.exe
 The install of curl was successful.
  Software installed to 'C:\ProgramData\chocolatey\lib\curl\tools'

choco install bazel
ShimGen has successfully created a shim for bazel.exe
 The install of bazel was successful.
  Software installed to 'C:\ProgramData\chocolatey\lib\bazel'

必须在管理员权限下安装
choco install ninja

https://chocolatey.org/
## upgrade
choco upgrade chocolatey

## install

cmd.exe

```shell
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

powershell

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

## 卸载

## 安装的软件列表
choco search xxx

cmd
powershell
需要管理员权限


choco install graphviz 

```shell
PS C:\Windows\system32> choco install graphviz
Chocolatey v2.2.2
Installing the following packages:
graphviz
By installing, you accept licenses for the packages.
Progress: Downloading Graphviz 9.0.0... 100%

graphviz v9.0.0 [Approved]
graphviz package files install completed. Performing other installation steps.
The package graphviz wants to run 'chocolateyInstall.ps1'.
Note: If you don't run this script, the installation will fail.
Note: To confirm automatically next time, use '-y' or consider:
choco feature enable -n allowGlobalConfirmation
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): Y

Attempt to use original download file name failed for 'C:\ProgramData\chocolatey\lib\Graphviz\tools\graphviz-9.0.0 (64-bit) EXE installer.exe'.
Copying graphviz
  from 'C:\ProgramData\chocolatey\lib\Graphviz\tools\graphviz-9.0.0 (64-bit) EXE installer.exe'
Installing graphviz...
graphviz has been installed.
graphviz installed to 'C:\Program Files\Graphviz'
Added C:\ProgramData\chocolatey\bin\acyclic.exe shim pointed to 'c:\program files\graphviz\bin\acyclic.exe'.
Added C:\ProgramData\chocolatey\bin\bcomps.exe shim pointed to 'c:\program files\graphviz\bin\bcomps.exe'.
Added C:\ProgramData\chocolatey\bin\ccomps.exe shim pointed to 'c:\program files\graphviz\bin\ccomps.exe'.
Added C:\ProgramData\chocolatey\bin\circo.exe shim pointed to 'c:\program files\graphviz\bin\circo.exe'.
Added C:\ProgramData\chocolatey\bin\cluster.exe shim pointed to 'c:\program files\graphviz\bin\cluster.exe'.
Added C:\ProgramData\chocolatey\bin\dijkstra.exe shim pointed to 'c:\program files\graphviz\bin\dijkstra.exe'.
Added C:\ProgramData\chocolatey\bin\dot.exe shim pointed to 'c:\program files\graphviz\bin\dot.exe'.
Added C:\ProgramData\chocolatey\bin\dot2gxl.exe shim pointed to 'c:\program files\graphviz\bin\dot2gxl.exe'.
Added C:\ProgramData\chocolatey\bin\dot_builtins.exe shim pointed to 'c:\program files\graphviz\bin\dot_builtins.exe'.
Added C:\ProgramData\chocolatey\bin\edgepaint.exe shim pointed to 'c:\program files\graphviz\bin\edgepaint.exe'.
Added C:\ProgramData\chocolatey\bin\fdp.exe shim pointed to 'c:\program files\graphviz\bin\fdp.exe'.
Added C:\ProgramData\chocolatey\bin\gc.exe shim pointed to 'c:\program files\graphviz\bin\gc.exe'.
Added C:\ProgramData\chocolatey\bin\gml2gv.exe shim pointed to 'c:\program files\graphviz\bin\gml2gv.exe'.
Added C:\ProgramData\chocolatey\bin\graphml2gv.exe shim pointed to 'c:\program files\graphviz\bin\graphml2gv.exe'.
Added C:\ProgramData\chocolatey\bin\gv2gml.exe shim pointed to 'c:\program files\graphviz\bin\gv2gml.exe'.
Added C:\ProgramData\chocolatey\bin\gv2gxl.exe shim pointed to 'c:\program files\graphviz\bin\gv2gxl.exe'.
Added C:\ProgramData\chocolatey\bin\gvcolor.exe shim pointed to 'c:\program files\graphviz\bin\gvcolor.exe'.
Added C:\ProgramData\chocolatey\bin\gvgen.exe shim pointed to 'c:\program files\graphviz\bin\gvgen.exe'.
Added C:\ProgramData\chocolatey\bin\gvmap.exe shim pointed to 'c:\program files\graphviz\bin\gvmap.exe'.
Added C:\ProgramData\chocolatey\bin\gvpack.exe shim pointed to 'c:\program files\graphviz\bin\gvpack.exe'.
Added C:\ProgramData\chocolatey\bin\gvpr.exe shim pointed to 'c:\program files\graphviz\bin\gvpr.exe'.
Added C:\ProgramData\chocolatey\bin\gxl2dot.exe shim pointed to 'c:\program files\graphviz\bin\gxl2dot.exe'.
Added C:\ProgramData\chocolatey\bin\gxl2gv.exe shim pointed to 'c:\program files\graphviz\bin\gxl2gv.exe'.
Added C:\ProgramData\chocolatey\bin\mm2gv.exe shim pointed to 'c:\program files\graphviz\bin\mm2gv.exe'.
Added C:\ProgramData\chocolatey\bin\neato.exe shim pointed to 'c:\program files\graphviz\bin\neato.exe'.
Added C:\ProgramData\chocolatey\bin\nop.exe shim pointed to 'c:\program files\graphviz\bin\nop.exe'.
Added C:\ProgramData\chocolatey\bin\osage.exe shim pointed to 'c:\program files\graphviz\bin\osage.exe'.
Added C:\ProgramData\chocolatey\bin\patchwork.exe shim pointed to 'c:\program files\graphviz\bin\patchwork.exe'.
Added C:\ProgramData\chocolatey\bin\prune.exe shim pointed to 'c:\program files\graphviz\bin\prune.exe'.
Added C:\ProgramData\chocolatey\bin\sccmap.exe shim pointed to 'c:\program files\graphviz\bin\sccmap.exe'.
Added C:\ProgramData\chocolatey\bin\sfdp.exe shim pointed to 'c:\program files\graphviz\bin\sfdp.exe'.
Added C:\ProgramData\chocolatey\bin\tred.exe shim pointed to 'c:\program files\graphviz\bin\tred.exe'.
Added C:\ProgramData\chocolatey\bin\twopi.exe shim pointed to 'c:\program files\graphviz\bin\twopi.exe'.
Added C:\ProgramData\chocolatey\bin\unflatten.exe shim pointed to 'c:\program files\graphviz\bin\unflatten.exe'.
  graphviz may be able to be automatically uninstalled.
```
## 源代码

## 编译

 C:\ProgramData\chocolatey

ChocolateyInstall
ChocolateyToolsLocation
ChocolateyLastPathUpdate
PATH (will need updated to remove)


 * apikey - retrieves, saves or deletes an API key for a particular source
 * cache - Manage the local HTTP caches used to store queries (v2.1.0+)
 * config - Retrieve and configure config file settings
 * export - exports list of currently installed packages
 * feature - view and configure choco features
 * features - view and configure choco features (alias for feature)
 * find - searches remote packages (alias for search)
 * help - displays top level help information for choco
 * info - retrieves package information. Shorthand for choco search pkgname --exact --verbose
 * install - installs packages using configured sources
 * list - lists local packages
 * new - creates template files for creating a new Chocolatey package
 * outdated - retrieves information about packages that are outdated. Similar to upgrade all --noop
 * pack - packages nuspec, scripts, and other Chocolatey package resources into a nupkg file
 * pin - suppress upgrades for a package
 * push - pushes a compiled nupkg to a source
 * search - searches remote packages
 * setapikey - retrieves, saves or deletes an API key for a particular source (alias for apikey)
 * source - view and configure default sources
 * sources - view and configure default sources (alias for source)
 * template - get information about installed templates
 * templates - get information about installed templates (alias for template)
 * uninstall - uninstalls a package
 * unpackself - re-installs Chocolatey base files
 * upgrade - upgrades packages from various sources
 

choco search -h
Chocolatey v2.2.2
Search Command

Chocolatey will perform a search for a package local or remote.

Usage

    choco find <filter> [<options/switches>]
    choco search <filter> [<options/switches>]

Examples

    choco search git
    choco search git --source="'https://somewhere/out/there'"
    choco search bob -s "'https://somewhere/protected'" -u user -p pass
    choco search --page=0 --page-size=25
    choco search 7zip --all-versions --exact