# minio

minio存储

https://gitee.com/mirrors/minio

是的，MinIO 是目前最流行、功能最完整的 Amazon S3 开源替代方案。它是一个高性能、云原生的对象存储系统，完全兼容 Amazon S3 API。

MinIO 核心特性

1.  完全 S3 兼容
    ◦   这是其最大卖点。任何使用 AWS S3 SDK、CLI (aws s3命令) 或工具的应用程序，几乎无需修改代码即可直接对接 MinIO。

    ◦   支持 S3 的核心功能：存储桶管理、对象操作、分片上传、生命周期管理、版本控制等。

2.  高性能
    ◦   采用 Go 语言编写，设计简洁高效。

    ◦   在标准硬件上就能提供极高的吞吐量，官网宣称可达到每秒数十 GB 的吞吐。

3.  云原生架构
    ◦   天然支持容器化部署（Docker, Kubernetes），是 CNCF 的活跃项目。

    ◦   在 Kubernetes 中部署和管理非常方便，是云原生栈中对象存储的标准选择。

4.  可扩展性
    ◦   采用去中心化的无共享架构。通过添加新节点即可轻松横向扩展，形成单个命名空间。

    ◦   支持存储桶镜像，可实现跨数据中心的复制。

5.  企业级功能
    ◦   数据保护： 采用纠删码（Erasure Coding）而非多副本，在保证数据可靠性的同时，存储利用率更高（例如，4个数据块+2个校验块，可容忍任意2块磁盘失效）。

    ◦   加密： 支持服务端和客户端加密。

    ◦   监控： 集成 Prometheus 和 Grafana。

    ◦   身份管理： 集成 OpenID Connect、LDAP/AD 等。

6.  许可证
    ◦   核心产品采用 GNU AGPL v3 开源许可证。这要求任何直接修改 MinIO 并网络分发的行为都必须开源。

    ◦   提供商业许可证（MinIO Enterprise）和付费的 SUBNET 订阅（获得商业支持、企业功能和管理控制台）。

与 S3 的主要差异

特性 Amazon S3 MinIO

本质 托管的云服务（Serverless） 自托管的软件

成本模型 按使用量付费（存储、请求、流量） 前期硬件/云主机成本 + 运维成本。软件本身免费。

运维 全托管，无需运维基础设施 需要自行部署、维护、扩展和监控

全球分布 原生多区域复制，全球边缘站点 需要自行搭建多个集群并通过 Bucket Replication 功能配置

生态系统 与 AWS 上百项服务深度集成 主要是一个独立的存储层，需自行集成其他服务

极限规模 近乎无限扩展 受自建集群规模限制，但理论上也能扩展到 EB 级

主要应用场景

1.  混合云/私有云数据湖： 在企业内部搭建类似 S3 的数据湖底座，用于存放 AI/ML 数据、日志、备份、镜像等非结构化数据。
2.  开发测试环境： 在开发阶段模拟 S3，避免产生云服务费用，实现开发与生产环境的一致性。
3.  边缘存储： 由于其轻量和高效，适合在边缘计算节点部署。
4.  Kubernetes 原生应用持久化存储： 通过 CSI 驱动为运行在 K8s 中的有状态应用提供对象存储。
5.  S3 网关： MinIO 可以作为其他后端存储（如 NAS、HDFS）的 S3 兼容网关。

其他知名的 S3 开源替代（MinIO 的竞争者）

1.  Ceph (RADOS Gateway - RGW)
    ◦   特点： 一个统一的分布式存储系统，其对象存储网关（RGW）提供 S3 兼容 API。功能极其强大，但架构复杂，部署和运维门槛远高于 MinIO。

    ◦   适用场景： 需要同时提供块存储（RBD）、文件存储（CephFS）和对象存储（RGW） 三种服务的超大规模场景。

2.  OpenStack Swift
    ◦   特点： OpenStack 生态的原生对象存储项目，API 与 S3 不原生兼容（需要通过中间层转换）。与 OpenStack 其他组件绑定较深。

    ◦   适用场景： 以 OpenStack 为核心的私有云整体解决方案。

3.  Garage
    ◦   特点： 一个由法国社区主导的轻量级分布式对象存储，专注于地理分布式部署。设计比 MinIO 更简单，但生态和成熟度较低。

    ◦   适用场景： 小团队、对地理分布有特殊要求的边缘场景。

4.  SeaweedFS
    ◦   特点： 最初是一个高性能的分布式文件系统，后来增加了 S3 兼容网关。其核心优势在于海量小文件场景性能极佳。

    ◦   适用场景： 需要存储数十亿个小文件（如图片、文档）的场景。

如何选择？

方案 推荐选择时机

MinIO 绝大多数情况下的首选。你需要一个开箱即用、运维相对简单、性能好、社区活跃、文档齐全的 S3 替代品。

Ceph 你需要一个“存储一切”的统一存储平台，且拥有专业的存储运维团队，对规模和企业级特性有极致要求。

Swift 你的技术栈完全建立在 OpenStack 之上。

SeaweedFS 你的工作负载是海量小文件（百万/千万级以上），这是它的专长。

Garage 你是一个小团队，需要极简的、地理分布式的对象存储。

结论

MinIO 是 Amazon S3 开源替代方案中平衡性最好、最易用、生态最完善的选择，已经成为了这个领域的事实标准。它让企业在自己的基础设施上享受到了与公有云 S3 类似的体验和能力，是构建私有云数据湖和现代化应用存储层的基石技术。

如果你正准备尝试，建议从 MinIO 的官方文档和 Docker 快速启动开始，你会立刻感受到它的简洁和强大。

## nas替换
MinIO对象存储和NAS（Network Attached Storage）在功能上有一些显著的区别：

1. 定位和存储架构不同：
   - NAS主要面向文件级存储，适用于家庭、中小企业等场景，采用传统的文件系统存储数据。
   - MinIO定位于对象存储，适用于大规模非结构化数据存储，如图片、视频、日志等。
2. 数据访问方式不同：
   - NAS支持多种文件共享协议，如SMB、NFS等，用户可以通过文件系统访问数据。
   - MinIO通过RESTful API访问数据，适用于应用程序。
3. 部署方式不同：
   - NAS通常是一个独立的设备，可以通过网络连接到计算机或服务器。
   - MinIO支持分布式部署，可轻松扩展存储容量。
4. 数据保护技术不同：
   - NAS采用RAID技术确保数据安全性和可靠性。
   - MinIO采用Erasure Coding技术，确保数据可靠性。
5. 性能和扩展性：
   - MinIO以其高性能和可扩展性为特点，适合存储大量非结构化数据。
   - NAS在高性能集群中可能面临协议开销高、带宽低、延迟大的问题。

关于安全性，MinIO和NAS都需要适当的安全措施来保护数据。NAS可能需要配置VPN、网络访问管理等来保护数据，而MinIO提供了诸如TLS加密、服务器端加密以及与KMS（Key Management Service）集成等功能来增强安全性。然而，任何存储解决方案的安全性都取决于其配置和维护。

至于是否可以将现有的NAS项目直接替换为MinIO对象存储，这取决于几个因素：
- 数据访问模式：如果您的应用主要通过文件共享协议访问数据，转向MinIO可能需要改变应用程序的接口。
- 性能需求：如果您需要高性能和可扩展性，MinIO可能是一个更好的选择。
- 成本和资源：MinIO运行在标准硬件上，可能在成本和资源利用上更有优势。
- 安全性：您需要评估MinIO的安全特性是否满足您的安全需求，并确保正确配置以保护数据。

总的来说，MinIO和NAS各有优势，是否替换需要根据具体的业务需求、性能要求和安全考量来决定。直接替换可能需要一定的迁移工作和可能的应用程序接口调整。


MinIO是一个开源的对象存储服务器，可以用于存储和检索任意类型的数据，包括文本文件、图片、视频等。

要使用MinIO进行存储，首先需要安装和配置MinIO服务器。你可以在MinIO的官方网站上下载适合你操作系统的安装包，并按照官方文档提供的指导进行安装和配置。

安装和配置完成后，你可以使用MinIO提供的客户端库或MinIO的REST API与MinIO服务器进行交互。以下是一些常见的操作示例：

1. 创建存储桶（Bucket）：
```java
import io.minio.MinioClient;
import io.minio.errors.MinioException;

public class MinioExample {
    public static void main(String[] args) {
        try {
            // 创建MinIO客户端
            MinioClient minioClient = new MinioClient("http://minio-server:9000", "accessKey", "secretKey");
            
            // 创建存储桶
            minioClient.makeBucket("my-bucket");
            
            System.out.println("Bucket created successfully.");
        } catch (MinioException e) {
            System.out.println("Error occurred: " + e.getMessage());
        }
    }
}
```

2. 上传文件到存储桶：
```java
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.errors.MinioException;

public class MinioExample {
    public static void main(String[] args) {
        try {
            // 创建MinIO客户端
            MinioClient minioClient = new MinioClient("http://minio-server:9000", "accessKey", "secretKey");
            
            // 上传文件
            minioClient.putObject(
                PutObjectArgs.builder()
                    .bucket("my-bucket")
                    .object("my-object")
                    .filename("/path/to/local/file")
                    .build()
            );
            
            System.out.println("File uploaded successfully.");
        } catch (MinioException e) {
            System.out.println("Error occurred: " + e.getMessage());
        }
    }
}
```

3. 下载文件：
```java
import io.minio.MinioClient;
import io.minio.GetObjectArgs;
import io.minio.errors.MinioException;

public class MinioExample {
    public static void main(String[] args) {
        try {
            // 创建MinIO客户端
            MinioClient minioClient = new MinioClient("http://minio-server:9000", "accessKey", "secretKey");
            
            // 下载文件
            minioClient.getObject(
                GetObjectArgs.builder()
                    .bucket("my-bucket")
                    .object("my-object")
                    .filename("/path/to/local/file")
                    .build()
            );
            
            System.out.println("File downloaded successfully.");
        } catch (MinioException e) {
            System.out.println("Error occurred: " + e.getMessage());
        }
    }
}
```

以上示例仅为基本操作示例，你可以根据具体需求使用MinIO提供的更多功能和API进行存储和检索操作。请参考MinIO的官方文档获取更详细的使用说明和示例代码。

## source code
https://github.com/minio/minio

go/minio/2025_09_07
git clone https://github.com/minio/minio.git
cd minio
git checkout RELEASE.2025-09-07T16-13-09Z

go install github.com/minio/minio@latest

## 编程语言
Go写的
å
https://min.io/download

## 能力地图与运维要点

MinIO 的能力可以按四条线理解：

1. **身份与访问控制**：IAM、OIDC、LDAP/AD、STS。
2. **传输与静态数据保护**：TLS、mTLS、SSE、KMS、审计。
3. **单集群可靠性与扩展**：分布式部署、纠删码、池扩容、再平衡、自愈。
4. **跨集群与对象生命周期**：站点复制、桶复制、生命周期、分层、事件通知。

### 1. IAM、OIDC 与 STS

#### IAM

MinIO IAM 的核心对象是：

| 对象 | 作用 |
| --- | --- |
| User / Access Key | 访问 S3 API 的身份。长期凭据应限制权限并定期轮换。 |
| Group | 将多个用户绑定到一组策略。 |
| Policy | JSON 格式的允许/拒绝规则，通常按 `Action`、`Resource` 和条件限制权限。 |
| Service Account | 从用户或外部身份派生的应用凭据，适合服务间访问。 |
| Root/Superuser | 集群级管理身份，不应直接交给业务程序使用。 |

权限设计应遵循最小权限原则：应用只授予目标 bucket 和必要的 `s3:GetObject`、`s3:PutObject` 等动作；备份、复制、生命周期管理和管理员操作使用独立身份。`Deny` 规则优先于 `Allow`，不能仅靠隐藏 bucket 名称实现安全隔离。

#### OIDC

OIDC 让 MinIO 委托外部身份提供商完成登录和身份声明，例如 Keycloak、Okta、Entra ID 或其他兼容 OIDC 的 IdP。典型流程是：

```text
用户/应用 -> IdP 登录并取得 ID Token
        -> MinIO 校验 issuer、client、签名和 token 有效期
        -> 根据 claim 映射 MinIO policy
        -> 使用 S3 API 访问对象
```

生产配置需要明确：issuer URL、client ID、client secret、claim 中的用户名/组字段、默认策略、token 过期和撤销策略。OIDC 负责认证，不会自动替代 MinIO policy；用户登录成功后仍必须映射到实际权限。

#### STS

STS（Security Token Service）签发有期限的临时访问凭据，适合工作负载、CI/CD、跨账号访问和短期授权。常见的身份交换方式包括：

- `AssumeRoleWithWebIdentity`：使用 OIDC/Web Identity token 换取临时凭据。
- LDAP/AD 或外部身份登录后换取临时凭据。
- 使用服务账号或父身份创建受限的临时访问权限。

临时凭据包含 access key、secret key 和 session token，应用不应把它们写入镜像或长期配置文件。STS 的安全边界仍由映射后的 policy 决定；缩短有效期、限制 bucket/prefix、绑定条件和及时撤销上游身份，通常比发放长期 root key 更安全。

### 2. KMS、SSE、TLS 与审计

#### SSE 的层次

服务端加密（SSE）是在 MinIO 写入磁盘前加密对象数据。常见模式如下：

| 模式 | 密钥由谁提供 | 适用场景 |
| --- | --- | --- |
| SSE-S3 | MinIO/KMS 管理默认密钥 | 希望透明加密，应用无需管理密钥。 |
| SSE-KMS | 外部 KMS/KES 或 MinIO KMS 管理密钥 | 需要密钥轮换、审计、权限分离和集中管理。 |
| SSE-C | 客户端在每次请求中提供密钥 | 客户端控制密钥，但密钥遗失通常意味着对象无法解密。 |
| 客户端加密 | 应用在上传前自行加密 | MinIO 只保存密文，适用于端到端加密要求。 |

KMS 保存或生成密钥材料，MinIO 保存对象密文及必要的加密元数据；KMS 不等于备份，也不替代 IAM。应单独保护 KMS、备份密钥和恢复流程，避免“数据有备份但密钥丢失”的不可恢复事故。跨站点复制启用加密时，目标站点必须能够解密源站点复制过来的数据，或者配置目标站点重新加密的策略。

#### TLS 与 mTLS

- **TLS**：保护客户端到 MinIO 的 S3/API、Console 和节点间通信，生产环境应使用可信 CA 签发的证书，并关闭明文 HTTP。
- **mTLS**：除校验服务端证书外，还要求客户端出示证书。适合高信任边界的服务间访问、KMS/KES 通信和管理网络。
- 证书的 SAN 必须覆盖客户端实际访问的域名；集群节点、负载均衡器、KMS 和复制对端的证书链应分别验证。
- 证书轮换要验证不中断行为、私钥权限、CA 信任链和所有节点配置一致性。

TLS/mTLS 解决“谁能建立可信连接”，IAM/OIDC/STS 解决“连接建立后能做什么”，二者不能互相替代。

#### 审计与运行日志

普通运行日志用于定位启动、网络、磁盘、纠删码和复制问题；审计日志则回答“谁在什么时间从哪里对哪个 bucket/object 做了什么操作，结果如何”。审计日志应发送到独立的 HTTP webhook、Kafka、NATS、Elasticsearch 或日志平台，并做到：

- 记录身份、来源 IP、请求动作、bucket/object、状态码、错误和 request ID。
- 日志目标与 MinIO 分离，避免集群故障时审计记录也不可用。
- 限制审计日志的读取权限，配置保留、归档和不可篡改策略。
- 对 `PutBucketPolicy`、删除对象、密钥配置、用户/策略变更和复制配置变更设置告警。

### 3. 分布式部署、纠删码、自愈

分布式 MinIO 由多个节点和磁盘组成一个 S3 命名空间。对象不会简单地只放在某个节点，而是按纠删码切分为数据分片和校验分片，分散到 erasure set 的多个磁盘上。`EC:M` 中的 `M` 表示校验分片数量；可用性取决于具体 erasure set 是否仍满足读/写 quorum，而不是只看“集群还有多少台机器”。

部署时重点关注：

- 节点、磁盘和网络的故障域；不要把所有副本集中在同一机架或同一可用区。
- 同一池内磁盘容量、类型、性能和拓扑尽量一致。
- 使用稳定的节点域名或服务发现地址，避免把短期 IP 写入集群配置。
- 通过负载均衡将客户端请求分散到任意节点；节点之间必须双向可达。
- 监控磁盘健康、读写 quorum、延迟、网络带宽、heal 队列和对象扫描进度。

#### 自愈（Healing）

当磁盘或节点临时失联、分片损坏或更换磁盘后，MinIO 可以利用剩余数据分片和校验分片重建缺失分片。自愈不是备份：

- 它主要解决 erasure set 内的介质或节点故障。
- 当可用分片少于恢复所需的 quorum 时，纠删码无法恢复对象。
- 自愈期间会消耗磁盘 I/O、CPU 和网络，应监控对前台业务的影响。
- 更换磁盘前先确认故障范围、集群 quorum 和数据恢复能力，不能直接格式化疑似仍含有唯一分片的磁盘。

常用检查命令示例：

```bash
mc admin info ALIAS
mc ready ALIAS
mc admin heal -r ALIAS/BUCKET
mc admin trace -v ALIAS
```

### 4. 池扩容、再平衡与缩容

MinIO 的容量扩展不是简单给现有节点挂一块盘。生产环境通常通过增加满足纠删码要求的 **server pool** 扩容：新池由一组新的节点和磁盘组成，加入后仍共享一个命名空间。

必须区分三件事：

| 操作 | 目的 | 对旧对象的影响 |
| --- | --- | --- |
| 增加 server pool | 增加可用容量和写入承载能力 | 新写入会按池空间等策略选择目标；旧对象不会自动均匀搬迁。 |
| Rebalance | 主动重新分布对象，使多池空间和负载更均衡 | 会产生大量内部读写和网络流量，需安排窗口并监控。 |
| Decommission pool | 下线旧池或淘汰硬件 | 对象迁移到剩余池，剩余容量必须足够；迁移完成前旧池不能销毁。 |

扩容前要校验新池满足现有纠删码和最小 stripe 要求，硬件配置尽量相近，更新所有节点的拓扑配置，并同步更新负载均衡器。扩容和缩容解决的是容量与硬件生命周期问题，不等于跨机房灾备；灾备应使用站点复制。

```bash
# 查看池、磁盘、纠删码和容量状态
mc admin info ALIAS

# 查看/启动/停止再平衡（具体参数以当前 mc 版本为准）
mc admin rebalance status ALIAS
mc admin rebalance start ALIAS
mc admin rebalance stop ALIAS
```

再平衡期间不要同时进行另一项拓扑变更；扩容前应确认没有正在运行的 rebalance。容量规划通常要预留故障恢复、自愈、版本对象、未完成分片上传和业务增长空间，不能把可用空间长期打到接近 100%。

### 5. 站点复制与桶复制

#### Site Replication

站点复制以部署为单位同步多个独立 MinIO 集群，适合业务连续性、灾备和跨地域部署。同步范围通常包括 IAM、bucket 配置、策略、对象及对象元数据；多个站点可以组成 peer sites，并在站点恢复后重新同步。

关键前提和风险：

- 对端站点应使用兼容的 MinIO 版本、身份提供商和复制配置。
- 通常需要版本控制；复制之前要明确删除标记、历史版本和对象锁的语义。
- 加密对象必须确保目标站点拥有可用的密钥，或明确目标重新加密策略。
- 跨地域高延迟会造成复制延迟；同步复制会放大写路径延迟，异步复制则需要接受 RPO。
- 站点复制和同一部署上的桶复制不能随意混用，迁移前应先清理冲突的桶复制规则。

站点复制关注“整个集群如何恢复”，不是简单的 `mc mirror`。恢复演练要验证 DNS/LB 切换、凭据、IAM、KMS、对象版本、删除语义和回切流程。

#### Bucket Replication

桶复制以 bucket 为粒度，在源桶和目标桶之间同步对象、版本和相关元数据，适合只复制部分数据、跨区域副本或 active-active 桶。它的范围比站点复制小，但配置更灵活。

要重点检查：

- 源桶启用版本控制，复制规则覆盖哪些 prefix、tag 和操作类型。
- 目标端是否允许写入；双向复制可能产生冲突和循环设计问题。
- `PENDING`、`FAILED`、`COMPLETED` 等复制状态，以及失败重试和 backlog resync。
- 目标端的 IAM、KMS、对象锁、保留期和删除标记是否满足合规要求。
- 复制延迟、带宽和目标端容量，不能把复制当作零成本备份。

`mc mirror` 更适合一次性迁移、目录同步或只需要最新对象内容的备份；它不等价于带版本和元数据语义的桶复制，也不等价于完整站点灾备。

### 6. 生命周期、分层与对象锁

#### 生命周期管理（ILM）

生命周期规则按对象年龄、前缀、tag、版本状态等条件执行：

- 过期删除 current/non-current version 或 delete marker。
- 在对象达到指定天数后转移到远端 tier。
- 对版本桶分别配置当前版本和非当前版本规则，避免历史版本无限增长。
- 对未完成 multipart upload 设置清理规则，防止残留分片长期占用空间。

生命周期扫描通常是后台低优先级任务，规则达到时间后不代表对象会在同一秒删除或迁移。对象锁（Object Lock）、保留期和 Legal Hold 可能阻止删除；配置“自动删除”前要确认合规和恢复要求。

#### 分层（Tiering）

分层通过生命周期规则把较旧对象的数据迁移到远端 MinIO、S3、Azure 或 GCS 等存储。MinIO 保留对象元数据，并在读取时从远端取回数据。

分层不是复制：

- 远端 tier 的数据仍依赖源端元数据和远端访问凭据。
- 远端存储不可用时，读取已分层对象可能失败或变慢。
- 不要绕过 MinIO 直接修改远端 tier 的对象，否则可能破坏对象映射。
- 分层不能自动替代灾备；需要灾备时使用站点复制或桶复制。

### 7. 事件通知

Bucket Notification 可以在对象创建、删除、复制完成/失败等事件发生时向外部系统投递消息，常见目标包括 Kafka、RabbitMQ、NATS、Webhook、Elasticsearch 和数据库类系统。典型用途是触发转码、病毒扫描、索引构建、数据湖入 catalog 或异步工作流。

事件驱动设计应假设消息可能重复、乱序、延迟或投递失败：

- 消费者必须幂等，使用 bucket、object key、version ID、ETag 或事件 ID 去重。
- 事件只表示“发生了变化”，不能把通知当作对象内容本身；消费者需要再次通过 S3 API 校验对象。
- 配置 prefix/suffix 过滤，避免消费无关对象和触发自循环。
- 监控目标连接、队列堆积、失败重试和死信消息。
- 事件通知与审计日志用途不同：通知驱动业务，审计记录安全与操作事实。

### 8. 一套生产检查清单

- **身份**：关闭业务程序使用 root key，启用 IAM 最小权限和 STS；OIDC/LDAP 的 claim 映射经过验证。
- **网络**：S3、Console、节点间通信和 KMS 使用 TLS；高安全边界使用 mTLS；限制管理端口来源。
- **密钥**：明确 SSE-S3、SSE-KMS、SSE-C 的责任边界；演练密钥轮换、备份和恢复。
- **可靠性**：跨故障域部署，确认 erasure set 的 read/write quorum，定期检查 heal 和磁盘健康。
- **扩容**：新池满足纠删码要求；扩容、rebalance、decommission 分开执行并观察容量余量。
- **复制**：明确 RPO/RTO；区分 site、bucket、batch replication 和 `mc mirror`；定期做灾备恢复演练。
- **数据治理**：版本控制、Object Lock、生命周期、非当前版本和 multipart 清理规则相互校验。
- **可观测性**：Prometheus 指标、运行日志、审计日志、复制延迟、事件队列和告警链路完整。

官方资料：

- [MinIO/AIStor 核心概念](https://docs.min.io/aistor/operations/core-concepts/)
- [身份管理与访问控制](https://docs.min.io/aistor/administration/identity-access-management/)
- [KMS](https://docs.min.io/kms/)
- [扩容与 server pool](https://docs.min.io/aistor/operations/scaling/expansion/)
- [数据恢复与自愈](https://docs.min.io/aistor/operations/failure-and-recovery/)
- [站点复制](https://docs.min.io/aistor/administration/replication/site-replication/)
- [桶复制](https://docs.min.io/aistor/administration/replication/bucket-replication/)
- [生命周期管理](https://docs.min.io/aistor/administration/object-lifecycle-management/)
- [事件通知](https://docs.min.io/aistor/administration/notifications/)
