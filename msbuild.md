# msbuild

build工具，对比cmake ninja

https://blog.csdn.net/bklydxz/article/details/77933222

c#的项目

https://blog.csdn.net/lindexi_gd/article/details/86691492

[msbuild](https://github.com/microsoft/msbuild)

MSBuild是微软开发和维护的一个开源项目，它是Visual Studio中使用的构建工具。MSBuild可以用于编译、部署和生成各种应用程序，包括.NET Framework、.NET Core、ASP.NET、Windows应用程序、Web应用程序、服务和工具。

MSBuild的官方文档可以在微软官方网站上找到。您可以通过以下链接访问MSBuild的官方文档：

https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2022


MSBuild是Microsoft Build Engine的缩写，是微软的一个构建工具。MSBuild可以用来编译、构建、部署和测试应用程序。.csproj文件是C#项目的配置文件，它包含了项目的配置信息，如项目名称、版本号、输出路径等等。MSBuild读取.csproj文件来确定如何构建项目。 


C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\amd64\MSBuild.exe

clion配置msbuild失败，配置ninja可以

MSBuild可以构建C/C++项目的原因主要基于以下几个方面：

1. MSBuild的通用性和灵活性
MSBuild是Microsoft推出的一个编译平台，它是.NET Framework的一部分，但并不仅限于.NET项目的构建。MSBuild的设计初衷是为了提供一个灵活且强大的构建系统，能够支持多种编程语言和项目类型。通过XML格式的项目文件（如.vcxproj对于C/C++项目），MSBuild能够清晰地描述项目的结构和构建过程，包括源文件、编译选项、链接选项等。

2. 对C/C++项目的支持
MSBuild通过特定的项目文件类型（如.vcxproj）和相关的.targets、.props文件来支持C/C++项目的构建。这些文件定义了C/C++项目构建过程中所需的各种参数和步骤，包括预处理、编译、链接等。MSBuild在读取这些文件后，会根据其中的指令来执行相应的构建任务。

3. 与Visual Studio的集成
MSBuild是Visual Studio集成开发环境（IDE）中所有项目的本机生成系统，包括C/C++项目。在Visual Studio中创建C/C++项目时，IDE会自动生成相应的.vcxproj项目文件，并在构建项目时调用MSBuild来执行构建任务。这种集成使得MSBuild能够无缝地支持C/C++项目的构建，同时也为开发者提供了丰富的构建选项和配置能力。

4. 自定义任务和扩展性
MSBuild支持自定义任务和扩展，这意味着开发者可以根据需要编写自定义的构建逻辑，并将其集成到MSBuild构建过程中。这种自定义能力使得MSBuild能够灵活地适应各种复杂的构建需求，包括C/C++项目中可能遇到的各种特殊情况。

5. 官方文档和社区支持
Microsoft官方提供了详细的MSBuild文档和指南，帮助开发者了解如何使用MSBuild来构建C/C++项目。此外，社区中也存在大量的教程、示例和讨论，为开发者提供了丰富的资源和帮助。

综上所述，MSBuild之所以能够构建C/C++项目，是因为它具备通用性、灵活性、对C/C++项目的支持、与Visual Studio的集成、自定义任务和扩展性等特点。这些特点使得MSBuild成为了一个强大且可靠的构建工具，能够满足C/C++项目构建的各种需求。

在MSBuild中引入第三方库的头文件和库文件，通常涉及以下几个步骤，这些步骤主要通过修改项目文件（如.vcxproj文件）来实现：

1. 添加头文件目录
为了让编译器能够找到第三方库的头文件，你需要在项目文件的ClCompile项中添加<IncludeDirectories>元素。这告诉编译器在哪里查找.h或.hpp等头文件。

例如，如果第三方库的头文件位于C:\ThirdPartyLib\include，你可以在项目文件中添加如下内容（或修改现有内容）：

xml
<ClCompile>  
  <IncludeDirectories>$(IncludePath);C:\ThirdPartyLib\include</IncludeDirectories>  
  <!-- 其他编译选项 -->  
</ClCompile>
注意：$(IncludePath)是MSBuild中的一个宏，它通常包含了默认的包含目录。通过将其放在前面，可以确保不会覆盖默认的包含目录。

2. 添加库文件目录
为了链接器能够找到第三方库的库文件（.lib或.dll的导入库），你需要在项目文件的Link项中添加<AdditionalLibraryDirectories>元素。

例如，如果第三方库的库文件位于C:\ThirdPartyLib\lib，你可以添加如下内容：

xml
<Link>  
  <AdditionalLibraryDirectories>$(LibraryPath);C:\ThirdPartyLib\lib</AdditionalLibraryDirectories>  
  <!-- 其他链接选项 -->  
</Link>
同样地，$(LibraryPath)是一个包含默认库目录的宏。

3. 添加库文件引用
最后，你需要在链接器的输入中添加第三方库的库文件名。这可以通过在Link项中添加<AdditionalDependencies>元素来实现。

例如，如果第三方库名为ThirdPartyLib.lib，你可以添加如下内容：

xml
<Link>  
  <AdditionalDependencies>ThirdPartyLib.lib;%(AdditionalDependencies)</AdditionalDependencies>  
  <!-- 其他链接选项 -->  
</Link>
注意：使用%(AdditionalDependencies)是一个好习惯，它可以保留其他任何通过Visual Studio IDE或其他方式添加的依赖项。

4. （可选）添加动态链接库（DLL）的搜索路径
如果你的项目使用了第三方库的DLL版本，并且这些DLL不在系统的标准搜索路径中，你可能还需要在运行时指定这些DLL的搜索路径。这通常通过在应用程序的启动配置中设置环境变量PATH或在应用程序的manifest文件中指定来实现，而不是在MSBuild项目文件中。

总结
通过修改.vcxproj文件来引入第三方库的头文件和库文件是MSBuild构建C/C++项目时的常见做法。这涉及到添加包含目录、库目录和库文件依赖项等步骤。务必确保在正确的位置添加这些设置，并避免覆盖或忽略默认的包含和库路径。