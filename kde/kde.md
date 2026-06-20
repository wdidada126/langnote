# kde

https://invent.kde.org/explore/groups?sort=name_asc

https://kde.org/zh-cn/

## krita
https://github.com/KDE/krita

以下是 KDE 项目的官方仓库和重要网址：

🌐 官方主站和仓库

KDE 官方网站

• 主网站: https://kde.org/

• 社区网站: https://community.kde.org/

• 开发者门户: https://develop.kde.org/

官方 Git 仓库

• 主 Git 仓库: https://invent.kde.org/

• GitHub Mirror: https://github.com/KDE/

📱 KDE 主要项目仓库

Plasma 桌面环境


# Plasma 桌面
https://invent.kde.org/plasma/plasma-desktop

# KWin 窗口管理器  
https://invent.kde.org/plasma/kwin

# System Settings
https://invent.kde.org/plasma/systemsettings


KDE Frameworks (核心库)


# Frameworks 总览
https://invent.kde.org/frameworks

# 常用框架示例：
- KCoreAddons: https://invent.kde.org/frameworks/kcoreaddons
- KI18n: https://invent.kde.org/frameworks/ki18n  
- KConfig: https://invent.kde.org/frameworks/kconfig
- KWidgetsAddons: https://invent.kde.org/frameworks/kwidgetsaddons


KDE Applications (应用程序)


# 应用程序总览
https://invent.kde.org/utilities/
https://invent.kde.org/graphics/
https://invent.kde.org/multimedia/

# 知名应用示例：
- Dolphin 文件管理器: https://invent.kde.org/utilities/dolphin
- Kate 文本编辑器: https://invent.kde.org/utilities/kate  
- Okular 文档查看器: https://invent.kde.org/graphics/okular
- Kdenlive 视频编辑: https://invent.kde.org/multimedia/kdenlive


🔧 开发资源网站

开发文档

• API 文档: https://api.kde.org/

• 开发教程: https://develop.kde.org/docs/

• Frameworks 文档: https://api.kde.org/frameworks/

构建系统

• ECM (Extra CMake Modules): https://invent.kde.org/frameworks/extra-cmake-modules

• KDE Craft 构建工具: https://invent.kde.org/packaging/craft

持续集成

• KDE CI 系统: https://build.kde.org/

• Binary Factory (预编译包): https://binary-factory.kde.org/

🌍 社区和沟通平台

沟通渠道

• 论坛: https://forum.kde.org/

• 邮件列表: https://mail.kde.org/

• Matrix 聊天: https://kde.org/contact/chat.php

• Bug 追踪: https://bugs.kde.org/

贡献指南

• 首次贡献: https://community.kde.org/Get_Involved

• 开发指南: https://develop.kde.org/handbook/

• 代码风格: https://develop.kde.org/policies/frameworks-coding-style/

🚀 快速开始贡献

1. 克隆示例项目

# 克隆一个简单的 KDE 应用来学习
git clone https://invent.kde.org/utilities/kate.git
# 或
git clone https://github.com/KDE/kate.git


2. 浏览项目结构

cd kate
ls -la
# 查看典型的 KDE 项目结构：
# - src/ 源代码
# - CMakeLists.txt 构建配置
# - po/ 翻译文件
# - autotests/ 测试代码


3. 构建说明

大多数 KDE 项目使用标准构建流程：
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)


📊 仓库统计

• 总仓库数: 1000+ (分布在 invent.kde.org)

• 活跃项目: 300+ 

• 主要分类: Frameworks, Plasma, Applications, PIM, Gear

• 开发语言: 主要是 C++ (Qt), 也有 QML, Python 等

💡 搜索技巧

在 invent.kde.org 中搜索


# 搜索文件管理器相关项目
https://invent.kde.org/explore/projects?search=file+manager

# 搜索特定技术的项目
https://invent.kde.org/explore/projects?search=qtquick


使用 KDE Projects 网站

• 项目列表: https://projects.kde.org/

• 按分类浏览: https://apps.kde.org/

这些网址应该能帮你找到任何 KDE 相关的代码和资源！你想了解某个特定项目的详细信息吗？

KDE 的资金来源非常多元化，主要依靠社区支持和战略合作。以下是详细分析：

💰 KDE 资金主要来源

1. 会员费和捐赠（主要来源）

• 个人会员费: 年费 30-500 欧元不等

• 企业会员费: 根据公司规模 1000-20000 欧元/年

• PayPal/信用卡捐赠

• Liberapay 定期捐赠

2. 基金会和企业赞助


# 白金赞助商 (年赞助 10,000+ 欧元)
- Blue Systems    - 德国 IT 服务公司
- Canonical       - Ubuntu 背后公司
- Google Open Source Programs

# 黄金赞助商 (5,000-10,000 欧元)  
- SUSE            - 开源解决方案提供商
- Qt Group        - Qt 框架公司

# 白银赞助商 (1,000-5,000 欧元)
- 多个中小型科技公司


3. 会议和活动收入

• Akademy 年会: 参会费、赞助商展位

• KDE 开发者冲刺: 企业赞助特定功能开发

• 地区性活动: KDE 印度、日本等地区会议

4. 项目专项资助

• Google Summer of Code: 每个项目约 6000 美元

• Outreachy 实习项目: 多样性促进资助

• 欧盟科研项目: 如 Horizon 2020 中的开源部分

🏢 KDE 资金管理结构

KDE e.V. (注册非营利组织)

• 地点: 德国柏林

• 法律形式: 注册协会 (eingetragener Verein)

• 税务状态: 慈善组织，捐赠可抵税

• 透明度: 年度财务报告公开

财务分配示例（估算）


基础设施维护:   35%   (服务器、带宽、开发硬件)
社区活动:       25%   (会议差旅、住宿、场地)
开发者支持:     20%   (代码冲刺、实习津贴)
宣传推广:       10%   (网站、材料、活动)
行政管理:       10%   (法律、会计、银行费用)


🌍 地区性资金模型

KDE 美国 (501(c)(3) 非营利)

• 接受美国公司的税收可抵扣捐赠

• 为美国开发者提供法律和财务支持

KDE 日本协会

• 本地企业赞助

• 日语本地化项目专项资金

KDE 印度社区

• IT 公司赞助

• 高校合作项目

📊 具体资金流向示例

基础设施成本

# 年度基础设施支出（估算）
服务器托管:     15,000 欧元
带宽费用:       8,000 欧元  
开发构建服务器: 12,000 欧元
代码审查系统:   5,000 欧元
总计约:        40,000 欧元/年


社区活动预算


Akademy 年会:   50,000-80,000 欧元
地区性冲刺:     10,000-20,000 欧元/次  
文档翻译冲刺:   5,000-10,000 欧元


🤝 企业合作模式

技术合作

• Qt Company: 提供 Qt 框架技术支持和许可证

• Blue Systems: 雇佣专职 KDE 开发者

• SUSE: 赞助 Plasma 桌面开发

战略合作

# Google 的多种支持方式
- Google Summer of Code: 资金 + 曝光度
- Google Code-in: 吸引学生贡献者  
- 直接资金赞助特定项目


硬件赞助

• Purism: 为 Librem 5 开发 KDE Plasma Mobile

• Pine64: PinePhone 的 KDE 移动版开发

• 各种硬件商: 测试设备捐赠

📈 资金增长策略

多元化收入流

1. 扩大企业会员基础
2. 增加定期捐赠计划
3. 开发增值服务
4. 寻求更多基金会资助

成本控制策略

• 志愿者驱动: 减少人力成本

• 开源协作: 共享基础设施成本

• 社区资源: 利用成员的专业服务

🔍 财务透明度

公开信息渠道

• 年度报告: https://ev.kde.org/reports/

• 会员大会记录: 向所有会员公开

• 预算讨论: 社区邮件列表公开进行

最近年度数据（示例）


2022年总收入: ~400,000 欧元
2022年总支出: ~380,000 欧元  
企业赞助占比: 45%
个人捐赠占比: 30%
其他收入: 25%


💡 与其它开源项目对比

项目 主要资金源 年度预算

KDE 会员费+企业赞助 ~40万欧元

GNOME 基金会+会议 ~50万美元

Apache 企业赞助 ~100万美元

Linux基金会 企业会费 数千万美元

KDE 的成功在于建立了可持续的社区资金模型，既保持独立性又获得企业支持。这种模式确保了项目的长期健康发展！
