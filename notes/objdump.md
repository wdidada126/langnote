# objdump

objdump -p md5
```shell
Dynamic Section:
 NEEDED               libPocoUtil.so.31
 NEEDED               libPocoXML.so.31
 NEEDED               libPocoJSON.so.31
 NEEDED               libPocoMongoDB.so.31
 NEEDED               libPocoNet.so.31
 NEEDED               libPocoCrypto.so.31
 NEEDED               libPocoData.so.31
 NEEDED               libPocoDataSQLite.so.31
 NEEDED               libPocoZip.so.31
 NEEDED               libPocoFoundation.so.31
 NEEDED               libpthread.so.0
 NEEDED               libdl.so.2
 NEEDED               librt.so.1
 NEEDED               libssl.so.1.0.0
 NEEDED               libcrypto.so.1.0.0
 NEEDED               libstdc++.so.6
 NEEDED               libm.so.6
 NEEDED               libgcc_s.so.1
 NEEDED               libc.so.6
```
The llvm-objdump utility prints the contents of object files and final
       linked images named on the command line. If no file name is specified,
       llvm-objdump will attempt to read from a.out. If - is used as a file
       name, llvm-objdump will process a file on its standard input stream.

```
[root@10-23-29-39 ~]# objdump -x /usr/lib64/libprotobuf.so

/usr/lib64/libprotobuf.so:     file format elf64-x86-64
/usr/lib64/libprotobuf.so
architecture: i386:x86-64, flags 0x00000150:
HAS_SYMS, DYNAMIC, D_PAGED
start address 0x000000000004bc90

Program Header:
    LOAD off    0x0000000000000000 vaddr 0x0000000000000000 paddr 0x0000000000000000 align 2**21
         filesz 0x000000000010b898 memsz 0x000000000010b898 flags r-x
    LOAD off    0x000000000010bba8 vaddr 0x000000000030bba8 paddr 0x000000000030bba8 align 2**21
         filesz 0x00000000000055a4 memsz 0x00000000000059e8 flags rw-
 DYNAMIC off    0x000000000010e8c8 vaddr 0x000000000030e8c8 paddr 0x000000000030e8c8 align 2**3
         filesz 0x0000000000000220 memsz 0x0000000000000220 flags rw-
    NOTE off    0x00000000000001c8 vaddr 0x00000000000001c8 paddr 0x00000000000001c8 align 2**2
         filesz 0x0000000000000024 memsz 0x0000000000000024 flags r--
EH_FRAME off    0x00000000000e8428 vaddr 0x00000000000e8428 paddr 0x00000000000e8428 align 2**2
         filesz 0x000000000000362c memsz 0x000000000000362c flags r--
   STACK off    0x0000000000000000 vaddr 0x0000000000000000 paddr 0x0000000000000000 align 2**4
         filesz 0x0000000000000000 memsz 0x0000000000000000 flags rw-
   RELRO off    0x000000000010bba8 vaddr 0x000000000030bba8 paddr 0x000000000030bba8 align 2**0
         filesz 0x0000000000003458 memsz 0x0000000000003458 flags r--

Dynamic Section:
  NEEDED               libpthread.so.0
  NEEDED               libz.so.1
  NEEDED               libstdc++.so.6
  NEEDED               libm.so.6
  NEEDED               libc.so.6
  NEEDED               libgcc_s.so.1
  SONAME               libprotobuf.so.8
  INIT                 0x0000000000047a20
  FINI                 0x00000000000dd148
  INIT_ARRAY           0x000000000030bba8
  INIT_ARRAYSZ         0x0000000000000040
  FINI_ARRAY           0x000000000030bbe8
  FINI_ARRAYSZ         0x0000000000000008
  GNU_HASH             0x00000000000001f0
  STRTAB               0x0000000000012888
  SYMTAB               0x0000000000004ce0
  STRSZ                0x0000000000025d88
  SYMENT               0x0000000000000018
  PLTGOT               0x000000000030f000
  PLTRELSZ             0x0000000000006360
  PLTREL               0x0000000000000007
  JMPREL               0x00000000000416c0
  RELA                 0x0000000000039950
  RELASZ               0x0000000000007d70
  RELAENT              0x0000000000000018
  VERNEED              0x0000000000039860
  VERNEEDNUM           0x0000000000000005
  VERSYM               0x0000000000038610
  RELACOUNT            0x000000000000004a

Version References:
  required from libgcc_s.so.1:
    0x0b792650 0x00 10 GCC_3.0
  required from libm.so.6:
    0x09691a75 0x00 08 GLIBC_2.2.5
  required from libpthread.so.0:
    0x09691a75 0x00 04 GLIBC_2.2.5
  required from libc.so.6:
    0x06969194 0x00 11 GLIBC_2.14
    0x0d696914 0x00 07 GLIBC_2.4
    0x09691974 0x00 06 GLIBC_2.3.4
    0x09691a75 0x00 03 GLIBC_2.2.5
  required from libstdc++.so.6:
    0x0297f860 0x00 09 GLIBCXX_3.4.10
    0x056bafd3 0x00 05 CXXABI_1.3
    0x08922974 0x00 02 GLIBCXX_3.4

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .note.gnu.build-id 00000024  00000000000001c8  00000000000001c8  000001c8  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  1 .gnu.hash     00004af0  00000000000001f0  00000000000001f0  000001f0  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  2 .dynsym       0000dba8  0000000000004ce0  0000000000004ce0  00004ce0  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  3 .dynstr       00025d88  0000000000012888  0000000000012888  00012888  2**0
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  4 .gnu.version  0000124e  0000000000038610  0000000000038610  00038610  2**1
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  5 .gnu.version_r 000000f0  0000000000039860  0000000000039860  00039860  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  6 .rela.dyn     00007d70  0000000000039950  0000000000039950  00039950  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  7 .rela.plt     00006360  00000000000416c0  00000000000416c0  000416c0  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  8 .init         0000001a  0000000000047a20  0000000000047a20  00047a20  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
  9 .plt          00004250  0000000000047a40  0000000000047a40  00047a40  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
 10 .text         000914b8  000000000004bc90  000000000004bc90  0004bc90  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
 11 .fini         00000009  00000000000dd148  00000000000dd148  000dd148  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
 12 .rodata       0000b2c5  00000000000dd160  00000000000dd160  000dd160  2**5
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
 13 .eh_frame_hdr 0000362c  00000000000e8428  00000000000e8428  000e8428  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
 14 .eh_frame     0001694c  00000000000eba58  00000000000eba58  000eba58  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
 15 .gcc_except_table 000094f4  00000000001023a4  00000000001023a4  001023a4  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
 16 .init_array   00000040  000000000030bba8  000000000030bba8  0010bba8  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 17 .fini_array   00000008  000000000030bbe8  000000000030bbe8  0010bbe8  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 18 .jcr          00000008  000000000030bbf0  000000000030bbf0  0010bbf0  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 19 .data.rel.ro  00002cc8  000000000030bc00  000000000030bc00  0010bc00  2**5
                  CONTENTS, ALLOC, LOAD, DATA
 20 .dynamic      00000220  000000000030e8c8  000000000030e8c8  0010e8c8  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 21 .got          00000508  000000000030eae8  000000000030eae8  0010eae8  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 22 .got.plt      00002138  000000000030f000  000000000030f000  0010f000  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 23 .data         00000014  0000000000311138  0000000000311138  00111138  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 24 .bss          00000430  0000000000311160  0000000000311160  0011114c  2**5
                  ALLOC
 25 .gnu_debuglink 00000020  0000000000000000  0000000000000000  0011114c  2**2
                  CONTENTS, READONLY
 26 .gnu_debugdata 00000ef0  0000000000000000  0000000000000000  0011116c  2**0
                  CONTENTS, READONLY
SYMBOL TABLE:
no symbols
```

