# minio

minio 存储

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

go install github.com/minio/minio@latest

Go写的

https://min.io/download

