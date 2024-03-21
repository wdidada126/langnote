# Pingora

Cloudflare表示，多年来在NGINX的使用上遇到了很多限制，包括损害性能的架构，某些类型的功能难以添加等。在Rust编写的Pingora上使用，消耗的CPU和内存能减少约70%和67%，除了性能优势外，还很安全。



https://www.zhihu.com/answer/2683364208

就拿国内公司环境往国外公司硬套。Nginx 的问题文中说的很清楚了，无论是 request per worker 导致 CPU 负载不均衡的问题还是 tls cache miss 的问题都是业界有目共睹的，随便一搜就是各种相关提问，而 Nginx 的架构导致根本无法完全规避这些问题。

“在nginx已经足够强劲” 强劲还能省出 70% CPU 和 67% 内存的吗 

git clone https://github.com/cloudflare/pingora.git
cd pingora


env:
  BUILD_TYPE: Release
  CARGO_TERM_COLOR: always
