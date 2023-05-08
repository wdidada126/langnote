# UnSafe

java_unsafe.md

Java

Rust



```java
#
# A fatal error has been detected by the Java Runtime Environment:
#
#  SIGSEGV (0xb) at pc=0x0000000111385d73, pid=87177, tid=0x0000000000001003
#
# JRE version: Java(TM) SE Runtime Environment (8.0_211-b12) (build 1.8.0_211-b12)
# Java VM: Java HotSpot(TM) 64-Bit Server VM (25.211-b12 mixed mode bsd-amd64 compressed oops)
# Problematic frame:
# V  [libjvm.dylib+0x585d73]  Unsafe_SetNativeChar+0x4b
#
# Failed to write core dump. Core dumps have been disabled. To enable core dumping, try "ulimit -c unlimited" before starting Java again
#
# An error report file with more information is saved as:
# /Users/ibqo/development/IdeaProjects/testjdk8/hs_err_pid87177.log
#
# If you would like to submit a bug report, please visit:
#   http://bugreport.java.com/bugreport/crash.jsp
#

Process finished with exit code 134 (interrupted by signal 6: SIGABRT)
```