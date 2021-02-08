# centos rpm

rpm如何处理依赖
yum安装的时候，可以处理

rpm -ivh的时候，处理不了

RPM是RedHat Package Manager（RedHat软件包管理工具）类似Windows里面的“添加/删除程序”

`yum install rpmdevtools -y`

https://blog.csdn.net/mrbuffoon/article/details/82766664
rpmdev-setuptree这个命令就是安装rpmdevtools
rpmdev-setuptree这个命令就是安装rpmdevtools带来的。可以看到运行了这个命令之后，在$HOME家目录下多了一个叫做rpmbuild的文件夹，里边内容如下：


默认位置

宏代码

名称

用途

~/rpmbuild/SPECS

%_specdir

Spec 文件目录

保存 RPM 包配置（.spec）文件

~/rpmbuild/SOURCES

%_sourcedir

源代码目录

保存源码包（如 .tar 包）和所有 patch 补丁

~/rpmbuild/BUILD
%_builddir
构建目录
源码包被解压至此，并在该目录的子目录完成编译
~/rpmbuild/BUILDROOT
%_buildrootdir
最终安装目录
保存 %install 阶段安装的文件
~/rpmbuild/RPMS
%_rpmdir
标准 RPM 包目录
生成/保存二进制 RPM 包
~/rpmbuild/SRPMS
%_srcrpmdir
源代码 RPM 包目录
生成/保存源码 RPM 包(SRPM)



打rpm包。

        以从http://www.linuxfromscratch.org/blfs/view/svn/general/libpng.html下载的libpng-1.6.2为例，针对i386环境打包，编写好对应的libpng.spec文件后，再使用rmpbuild -ba libpng.spec执行第2步中编写的spec文件打包，假如在spec文件中的%package -n 描述有libpng-tools、libpng-runtime、libpng-devel三个包，那么执行完spec文件中的内容后可以在RPMS目录下看到对应的libpng-tools-1.6.2-1.i386.rpm、libpng-runtime-1.6.2-1.i386.rpm、libpng-devel-1.6.2-1.i386.rpm以及在SRPMS下生成libpng.src.rpm二进制源码包。

        5、最后可以使用rpm -ivh libpng-1.6.2-1.i386.rpm在自己的X86机器上安装对应的rpm包。

```shell
rpm -qa | grep mysql
mysql-community-client-5.6.40-2.el7.x86_64
mysql-community-release-el7-5.noarch
mysql-community-common-5.6.40-2.el7.x86_64
mysql-community-server-5.6.40-2.el7.x86_64
mysql-community-libs-5.6.40-2.el7.x86_64
```


rpm -qa
error: rpmdb: BDB0113 Thread/process 13171/140228881938496 failed: BDB1507 Thread died in Berkeley DB library
error: db5 error(-30973) from dbenv->failchk: BDB0087 DB_RUNRECOVERY: Fatal error, run database recovery
error: cannot open Packages index using db5 -  (-30973)
error: cannot open Packages database in /var/lib/rpm
error: rpmdb: BDB0113 Thread/process 13171/140228881938496 failed: BDB1507 Thread died in Berkeley DB library
error: db5 error(-30973) from dbenv->failchk: BDB0087 DB_RUNRECOVERY: Fatal error, run database recovery
error: cannot open Packages database in /var/lib/rpm
```

百度 搞定


rpm -ql mysql-community-server-5.7.32-1.el7.x86_64
/etc/logrotate.d/mysql
/etc/my.cnf
/etc/my.cnf.d
/usr/bin/innochecksum
/usr/bin/lz4_decompress
/usr/bin/my_print_defaults
/usr/bin/myisam_ftdump
/usr/bin/myisamchk
/usr/bin/myisamlog
/usr/bin/myisampack
/usr/bin/mysql_install_db
/usr/bin/mysql_plugin
/usr/bin/mysql_secure_installation
/usr/bin/mysql_ssl_rsa_setup
/usr/bin/mysql_tzinfo_to_sql
/usr/bin/mysql_upgrade
/usr/bin/mysqld_pre_systemd
/usr/bin/mysqldumpslow
/usr/bin/perror
/usr/bin/replace
/usr/bin/resolve_stack_dump
/usr/bin/resolveip
/usr/bin/zlib_decompress
/usr/lib/systemd/system/mysqld.service
/usr/lib/systemd/system/mysqld@.service
/usr/lib/tmpfiles.d/mysql.conf
/usr/lib64/mysql/mecab
/usr/lib64/mysql/mecab/dic
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/char.bin
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/dicrc
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/left-id.def
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/matrix.bin
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/pos-id.def
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/rewrite.def
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/right-id.def
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/sys.dic
/usr/lib64/mysql/mecab/dic/ipadic_euc-jp/unk.dic
/usr/lib64/mysql/mecab/dic/ipadic_sjis
/usr/lib64/mysql/mecab/dic/ipadic_sjis/char.bin
/usr/lib64/mysql/mecab/dic/ipadic_sjis/dicrc
/usr/lib64/mysql/mecab/dic/ipadic_sjis/left-id.def
/usr/lib64/mysql/mecab/dic/ipadic_sjis/matrix.bin
/usr/lib64/mysql/mecab/dic/ipadic_sjis/pos-id.def
/usr/lib64/mysql/mecab/dic/ipadic_sjis/rewrite.def
/usr/lib64/mysql/mecab/dic/ipadic_sjis/right-id.def
/usr/lib64/mysql/mecab/dic/ipadic_sjis/sys.dic
/usr/lib64/mysql/mecab/dic/ipadic_sjis/unk.dic
/usr/lib64/mysql/mecab/dic/ipadic_utf-8
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/char.bin
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/dicrc
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/left-id.def
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/matrix.bin
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/pos-id.def
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/rewrite.def
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/right-id.def
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/sys.dic
/usr/lib64/mysql/mecab/dic/ipadic_utf-8/unk.dic
/usr/lib64/mysql/mecab/etc
/usr/lib64/mysql/mecab/etc/mecabrc
/usr/lib64/mysql/plugin
/usr/lib64/mysql/plugin/adt_null.so
/usr/lib64/mysql/plugin/auth_socket.so
/usr/lib64/mysql/plugin/authentication_ldap_sasl_client.so
/usr/lib64/mysql/plugin/connection_control.so
/usr/lib64/mysql/plugin/debug
/usr/lib64/mysql/plugin/debug/adt_null.so
/usr/lib64/mysql/plugin/debug/auth_socket.so
/usr/lib64/mysql/plugin/debug/authentication_ldap_sasl_client.so
/usr/lib64/mysql/plugin/debug/connection_control.so
/usr/lib64/mysql/plugin/debug/group_replication.so
/usr/lib64/mysql/plugin/debug/ha_example.so
/usr/lib64/mysql/plugin/debug/innodb_engine.so
/usr/lib64/mysql/plugin/debug/keyring_file.so
/usr/lib64/mysql/plugin/debug/keyring_udf.so
/usr/lib64/mysql/plugin/debug/libmemcached.so
/usr/lib64/mysql/plugin/debug/libpluginmecab.so
/usr/lib64/mysql/plugin/debug/locking_service.so
/usr/lib64/mysql/plugin/debug/mypluglib.so
/usr/lib64/mysql/plugin/debug/mysql_no_login.so
/usr/lib64/mysql/plugin/debug/mysqlx.so
/usr/lib64/mysql/plugin/debug/rewrite_example.so
/usr/lib64/mysql/plugin/debug/rewriter.so
/usr/lib64/mysql/plugin/debug/semisync_master.so
/usr/lib64/mysql/plugin/debug/semisync_slave.so
/usr/lib64/mysql/plugin/debug/validate_password.so
/usr/lib64/mysql/plugin/debug/version_token.so
/usr/lib64/mysql/plugin/group_replication.so
/usr/lib64/mysql/plugin/ha_example.so
/usr/lib64/mysql/plugin/innodb_engine.so
/usr/lib64/mysql/plugin/keyring_file.so
/usr/lib64/mysql/plugin/keyring_udf.so
/usr/lib64/mysql/plugin/libmemcached.so
/usr/lib64/mysql/plugin/libpluginmecab.so
/usr/lib64/mysql/plugin/locking_service.so
/usr/lib64/mysql/plugin/mypluglib.so
/usr/lib64/mysql/plugin/mysql_no_login.so
/usr/lib64/mysql/plugin/mysqlx.so
/usr/lib64/mysql/plugin/rewrite_example.so
/usr/lib64/mysql/plugin/rewriter.so
/usr/lib64/mysql/plugin/semisync_master.so
/usr/lib64/mysql/plugin/semisync_slave.so
/usr/lib64/mysql/plugin/validate_password.so
/usr/lib64/mysql/plugin/version_token.so
/usr/sbin/mysqld
/usr/sbin/mysqld-debug
/usr/share/doc/mysql-community-server-5.7.32
/usr/share/doc/mysql-community-server-5.7.32/ChangeLog
/usr/share/doc/mysql-community-server-5.7.32/INFO_BIN
/usr/share/doc/mysql-community-server-5.7.32/INFO_SRC
/usr/share/doc/mysql-community-server-5.7.32/LICENSE
/usr/share/doc/mysql-community-server-5.7.32/README
/usr/share/man/man1/innochecksum.1.gz
/usr/share/man/man1/lz4_decompress.1.gz
/usr/share/man/man1/my_print_defaults.1.gz
/usr/share/man/man1/myisam_ftdump.1.gz
/usr/share/man/man1/myisamchk.1.gz
/usr/share/man/man1/myisamlog.1.gz
/usr/share/man/man1/myisampack.1.gz
/usr/share/man/man1/mysql.server.1.gz
/usr/share/man/man1/mysql_install_db.1.gz
/usr/share/man/man1/mysql_plugin.1.gz
/usr/share/man/man1/mysql_secure_installation.1.gz
/usr/share/man/man1/mysql_ssl_rsa_setup.1.gz
/usr/share/man/man1/mysql_tzinfo_to_sql.1.gz
/usr/share/man/man1/mysql_upgrade.1.gz
/usr/share/man/man1/mysqldumpslow.1.gz
/usr/share/man/man1/mysqlman.1.gz
/usr/share/man/man1/perror.1.gz
/usr/share/man/man1/replace.1.gz
/usr/share/man/man1/resolve_stack_dump.1.gz
/usr/share/man/man1/resolveip.1.gz
/usr/share/man/man1/zlib_decompress.1.gz
/usr/share/man/man8/mysqld.8.gz
/usr/share/mysql/dictionary.txt
/usr/share/mysql/fill_help_tables.sql
/usr/share/mysql/innodb_memcached_config.sql
/usr/share/mysql/install_rewriter.sql
/usr/share/mysql/magic
/usr/share/mysql/mysql-log-rotate
/usr/share/mysql/mysql_security_commands.sql
/usr/share/mysql/mysql_sys_schema.sql
/usr/share/mysql/mysql_system_tables.sql
/usr/share/mysql/mysql_system_tables_data.sql
/usr/share/mysql/mysql_test_data_timezone.sql
/usr/share/mysql/uninstall_rewriter.sql
/var/lib/mysql
/var/lib/mysql-files
/var/lib/mysql-keyring
/var/run/mysqld


rpm -qa | grep mysql
mysql-community-server-5.7.32-1.el7.x86_64
mysql57-community-release-el7-9.noarch
mysql-community-libs-compat-5.7.32-1.el7.x86_64
mysql-community-devel-5.7.32-1.el7.x86_64
mysql-community-libs-5.7.32-1.el7.x86_64
mysql-community-client-5.7.32-1.el7.x86_64
libodb-mysql-devel-2.3.0-1.el7.x86_64
libodb-mysql-2.3.0-1.el7.x86_64
mysql-community-common-5.7.32-1.el7.x86_64



rpm -ql mysql-community-devel-5.7.32-1.el7.x86_64
/usr/bin/mysql_config
/usr/bin/mysql_config-64
/usr/include/mysql
/usr/include/mysql/big_endian.h
/usr/include/mysql/binary_log_types.h
/usr/include/mysql/byte_order_generic.h
/usr/include/mysql/byte_order_generic_x86.h
/usr/include/mysql/decimal.h
/usr/include/mysql/errmsg.h
/usr/include/mysql/keycache.h
/usr/include/mysql/little_endian.h
/usr/include/mysql/m_ctype.h
/usr/include/mysql/m_string.h
/usr/include/mysql/my_alloc.h
/usr/include/mysql/my_byteorder.h
/usr/include/mysql/my_command.h
/usr/include/mysql/my_compiler.h
/usr/include/mysql/my_config.h
/usr/include/mysql/my_config_x86_64.h
/usr/include/mysql/my_dbug.h
/usr/include/mysql/my_dir.h
/usr/include/mysql/my_getopt.h
/usr/include/mysql/my_global.h
/usr/include/mysql/my_list.h
/usr/include/mysql/my_sys.h
/usr/include/mysql/my_thread.h
/usr/include/mysql/my_thread_local.h
/usr/include/mysql/my_xml.h
/usr/include/mysql/mysql
/usr/include/mysql/mysql.h
/usr/include/mysql/mysql/client_authentication.h
/usr/include/mysql/mysql/client_plugin.h
/usr/include/mysql/mysql/client_plugin.h.pp
/usr/include/mysql/mysql/com_data.h
/usr/include/mysql/mysql/get_password.h
/usr/include/mysql/mysql/group_replication_priv.h
/usr/include/mysql/mysql/innodb_priv.h
/usr/include/mysql/mysql/mysql_lex_string.h
/usr/include/mysql/mysql/plugin.h
/usr/include/mysql/mysql/plugin_audit.h
/usr/include/mysql/mysql/plugin_audit.h.pp
/usr/include/mysql/mysql/plugin_auth.h
/usr/include/mysql/mysql/plugin_auth.h.pp
/usr/include/mysql/mysql/plugin_auth_common.h
/usr/include/mysql/mysql/plugin_ftparser.h
/usr/include/mysql/mysql/plugin_ftparser.h.pp
/usr/include/mysql/mysql/plugin_group_replication.h
/usr/include/mysql/mysql/plugin_keyring.h
/usr/include/mysql/mysql/plugin_keyring.h.pp
/usr/include/mysql/mysql/plugin_trace.h
/usr/include/mysql/mysql/plugin_validate_password.h
/usr/include/mysql/mysql/psi
/usr/include/mysql/mysql/psi/mysql_file.h
/usr/include/mysql/mysql/psi/mysql_idle.h
/usr/include/mysql/mysql/psi/mysql_mdl.h
/usr/include/mysql/mysql/psi/mysql_memory.h
/usr/include/mysql/mysql/psi/mysql_ps.h
/usr/include/mysql/mysql/psi/mysql_socket.h
/usr/include/mysql/mysql/psi/mysql_sp.h
/usr/include/mysql/mysql/psi/mysql_stage.h
/usr/include/mysql/mysql/psi/mysql_statement.h
/usr/include/mysql/mysql/psi/mysql_table.h
/usr/include/mysql/mysql/psi/mysql_thread.h
/usr/include/mysql/mysql/psi/mysql_transaction.h
/usr/include/mysql/mysql/psi/psi.h
/usr/include/mysql/mysql/psi/psi_base.h
/usr/include/mysql/mysql/psi/psi_memory.h
/usr/include/mysql/mysql/service_command.h
/usr/include/mysql/mysql/service_locking.h
/usr/include/mysql/mysql/service_my_plugin_log.h
/usr/include/mysql/mysql/service_my_snprintf.h
/usr/include/mysql/mysql/service_mysql_alloc.h
/usr/include/mysql/mysql/service_mysql_keyring.h
/usr/include/mysql/mysql/service_mysql_password_policy.h
/usr/include/mysql/mysql/service_mysql_string.h
/usr/include/mysql/mysql/service_parser.h
/usr/include/mysql/mysql/service_rpl_transaction_ctx.h
/usr/include/mysql/mysql/service_rpl_transaction_write_set.h
/usr/include/mysql/mysql/service_rules_table.h
/usr/include/mysql/mysql/service_security_context.h
/usr/include/mysql/mysql/service_srv_session.h
/usr/include/mysql/mysql/service_srv_session_info.h
/usr/include/mysql/mysql/service_ssl_wrapper.h
/usr/include/mysql/mysql/service_thd_alloc.h
/usr/include/mysql/mysql/service_thd_engine_lock.h
/usr/include/mysql/mysql/service_thd_wait.h
/usr/include/mysql/mysql/service_thread_scheduler.h
/usr/include/mysql/mysql/services.h
/usr/include/mysql/mysql/services.h.pp
/usr/include/mysql/mysql/thread_pool_priv.h
/usr/include/mysql/mysql/thread_type.h
/usr/include/mysql/mysql_com.h
/usr/include/mysql/mysql_com_server.h
/usr/include/mysql/mysql_embed.h
/usr/include/mysql/mysql_time.h
/usr/include/mysql/mysql_version.h
/usr/include/mysql/mysqld_ername.h
/usr/include/mysql/mysqld_error.h
/usr/include/mysql/mysqlx_ername.h
/usr/include/mysql/mysqlx_error.h
/usr/include/mysql/mysqlx_version.h
/usr/include/mysql/plugin.h
/usr/include/mysql/plugin_audit.h
/usr/include/mysql/plugin_ftparser.h
/usr/include/mysql/plugin_group_replication.h
/usr/include/mysql/plugin_keyring.h
/usr/include/mysql/plugin_validate_password.h
/usr/include/mysql/sql_common.h
/usr/include/mysql/sql_state.h
/usr/include/mysql/sslopt-case.h
/usr/include/mysql/sslopt-longopts.h
/usr/include/mysql/sslopt-vars.h
/usr/include/mysql/thr_cond.h
/usr/include/mysql/thr_mutex.h
/usr/include/mysql/thr_rwlock.h
/usr/include/mysql/typelib.h
/usr/lib64/mysql/libmysqlclient.a
/usr/lib64/mysql/libmysqlclient.so
/usr/lib64/mysql/libmysqlservices.a
/usr/lib64/pkgconfig/mysqlclient.pc
/usr/share/aclocal/mysql.m4
/usr/share/doc/mysql-community-devel-5.7.32
/usr/share/doc/mysql-community-devel-5.7.32/LICENSE
/usr/share/doc/mysql-community-devel-5.7.32/README
/usr/share/man/man1/comp_err.1.gz
/usr/share/man/man1/mysql_config.1.gz
















rpm -ql mysql-community-server-5.6.40-2.el7.x86_64
/etc/logrotate.d/mysql
/etc/my.cnf
/etc/my.cnf.d
/usr/bin/innochecksum
/usr/bin/my_print_defaults
/usr/bin/myisam_ftdump
/usr/bin/myisamchk
/usr/bin/myisamlog
/usr/bin/myisampack
/usr/bin/mysql-systemd-start
/usr/bin/mysql_convert_table_format
/usr/bin/mysql_fix_extensions
/usr/bin/mysql_install_db
/usr/bin/mysql_plugin
/usr/bin/mysql_secure_installation
/usr/bin/mysql_tzinfo_to_sql
/usr/bin/mysql_upgrade
/usr/bin/mysql_zap
/usr/bin/mysqlbug
/usr/bin/mysqld_multi
/usr/bin/mysqld_safe
/usr/bin/mysqldumpslow
/usr/bin/mysqlhotcopy
/usr/bin/mysqltest
/usr/bin/perror
/usr/bin/replace
/usr/bin/resolve_stack_dump
/usr/bin/resolveip
/usr/lib/systemd/system/mysqld.service
/usr/lib/tmpfiles.d/mysql.conf
/usr/lib64/mysql/plugin
/usr/lib64/mysql/plugin/adt_null.so
/usr/lib64/mysql/plugin/auth.so
/usr/lib64/mysql/plugin/auth_socket.so
/usr/lib64/mysql/plugin/auth_test_plugin.so
/usr/lib64/mysql/plugin/connection_control.so
/usr/lib64/mysql/plugin/daemon_example.ini
/usr/lib64/mysql/plugin/debug
/usr/lib64/mysql/plugin/debug/adt_null.so
/usr/lib64/mysql/plugin/debug/auth.so
/usr/lib64/mysql/plugin/debug/auth_socket.so
/usr/lib64/mysql/plugin/debug/auth_test_plugin.so
/usr/lib64/mysql/plugin/debug/connection_control.so
/usr/lib64/mysql/plugin/debug/innodb_engine.so
/usr/lib64/mysql/plugin/debug/libdaemon_example.so
/usr/lib64/mysql/plugin/debug/libmemcached.so
/usr/lib64/mysql/plugin/debug/mypluglib.so
/usr/lib64/mysql/plugin/debug/mysql_no_login.so
/usr/lib64/mysql/plugin/debug/qa_auth_client.so
/usr/lib64/mysql/plugin/debug/qa_auth_interface.so
/usr/lib64/mysql/plugin/debug/qa_auth_server.so
/usr/lib64/mysql/plugin/debug/semisync_master.so
/usr/lib64/mysql/plugin/debug/semisync_slave.so
/usr/lib64/mysql/plugin/debug/test_udf_services.so
/usr/lib64/mysql/plugin/debug/validate_password.so
/usr/lib64/mysql/plugin/innodb_engine.so
/usr/lib64/mysql/plugin/libdaemon_example.so
/usr/lib64/mysql/plugin/libmemcached.so
/usr/lib64/mysql/plugin/mypluglib.so
/usr/lib64/mysql/plugin/mysql_no_login.so
/usr/lib64/mysql/plugin/qa_auth_client.so
/usr/lib64/mysql/plugin/qa_auth_interface.so
/usr/lib64/mysql/plugin/qa_auth_server.so
/usr/lib64/mysql/plugin/semisync_master.so
/usr/lib64/mysql/plugin/semisync_slave.so
/usr/lib64/mysql/plugin/test_udf_services.so
/usr/lib64/mysql/plugin/validate_password.so
/usr/sbin/mysqld
/usr/sbin/mysqld-debug
/usr/share/doc/mysql-community-server-5.6.40
/usr/share/doc/mysql-community-server-5.6.40/COPYING
/usr/share/doc/mysql-community-server-5.6.40/ChangeLog
/usr/share/doc/mysql-community-server-5.6.40/INFO_BIN
/usr/share/doc/mysql-community-server-5.6.40/INFO_SRC
/usr/share/doc/mysql-community-server-5.6.40/README
/usr/share/doc/mysql-community-server-5.6.40/my-default.cnf
/usr/share/man/man1/innochecksum.1.gz
/usr/share/man/man1/my_print_defaults.1.gz
/usr/share/man/man1/myisam_ftdump.1.gz
/usr/share/man/man1/myisamchk.1.gz
/usr/share/man/man1/myisamlog.1.gz
/usr/share/man/man1/myisampack.1.gz
/usr/share/man/man1/mysql.server.1.gz
/usr/share/man/man1/mysql_convert_table_format.1.gz
/usr/share/man/man1/mysql_fix_extensions.1.gz
/usr/share/man/man1/mysql_install_db.1.gz
/usr/share/man/man1/mysql_plugin.1.gz
/usr/share/man/man1/mysql_secure_installation.1.gz
/usr/share/man/man1/mysql_tzinfo_to_sql.1.gz
/usr/share/man/man1/mysql_upgrade.1.gz
/usr/share/man/man1/mysql_zap.1.gz
/usr/share/man/man1/mysqlbug.1.gz
/usr/share/man/man1/mysqld_multi.1.gz
/usr/share/man/man1/mysqld_safe.1.gz
/usr/share/man/man1/mysqldumpslow.1.gz
/usr/share/man/man1/mysqlhotcopy.1.gz
/usr/share/man/man1/mysqlman.1.gz
/usr/share/man/man1/perror.1.gz
/usr/share/man/man1/replace.1.gz
/usr/share/man/man1/resolve_stack_dump.1.gz
/usr/share/man/man1/resolveip.1.gz
/usr/share/man/man8/mysqld.8.gz
/usr/share/mysql/SELinux/RHEL4/mysql.fc
/usr/share/mysql/SELinux/RHEL4/mysql.te
/usr/share/mysql/dictionary.txt
/usr/share/mysql/fill_help_tables.sql
/usr/share/mysql/innodb_memcached_config.sql
/usr/share/mysql/magic
/usr/share/mysql/my-default.cnf
/usr/share/mysql/mysql-log-rotate
/usr/share/mysql/mysql_security_commands.sql
/usr/share/mysql/mysql_system_tables.sql
/usr/share/mysql/mysql_system_tables_data.sql
/usr/share/mysql/mysql_test_data_timezone.sql
/var/lib/mysql
/var/lib/mysql-files
/var/run/mysqld
```


rpm
包管理器
利用 Downloadonly 插件下载 RPM 软件包及其所有依赖包
我们可以通过 yum 命令的 Downloadonly 插件下载 RPM 软件包及其所有依赖包。
为了安装 Downloadonly 插件，以 root 身份运行以下命令。



使用 Yumdownloader 工具来下载 RPM 软件包及其所有依赖包
Yumdownloader是一款简单，但是却十分有用的命令行工具，它可以一次性下载任何 RPM 软件包及其所有依赖包。
以 root 身份运行如下命令安装 Yumdownloader 工具。
https://blog.csdn.net/beeworkshop/article/details/101591990



yum源默认安装路径

rpm -qa | grep XXXXX
之后根据这个名字
rpm -ql xxx | more
就找到安装位置了.





yum - Yellowdog Updater Modified



-devel 包 包括头文件

不带devel的，只有二进制文件



yum 检索有哪些版本呢 安装指定版本



```shell
rpm -ql glog-devel
/usr/include/glog
/usr/include/glog/log_severity.h
/usr/include/glog/logging.h
/usr/include/glog/raw_logging.h
/usr/include/glog/stl_logging.h
/usr/include/glog/vlog_is_on.h
/usr/lib64/libglog.so
/usr/lib64/pkgconfig/libglog.pc
/usr/share/doc/glog-devel-0.3.3
/usr/share/doc/glog-devel-0.3.3/designstyle.css
/usr/share/doc/glog-devel-0.3.3/glog.html
```



```shell
rpm -ql gflags-devel
/usr/include/gflags
/usr/include/gflags/gflags.h
/usr/include/gflags/gflags_completions.h
/usr/include/gflags/gflags_declare.h
/usr/lib64/cmake
/usr/lib64/cmake/gflags
/usr/lib64/cmake/gflags/gflags-config-version.cmake
/usr/lib64/cmake/gflags/gflags-config.cmake
/usr/lib64/cmake/gflags/gflags-export-noconfig.cmake
/usr/lib64/cmake/gflags/gflags-export.cmake
/usr/lib64/libgflags.so
/usr/lib64/libgflags_nothreads.so
/usr/share/doc/gflags-devel-2.1.1
/usr/share/doc/gflags-devel-2.1.1/designstyle.css
/usr/share/doc/gflags-devel-2.1.1/gflags.html
```

rpm是由红帽公司开发的软件包管理方式，使用rpm我们可以方便的进行软件的安装、查询、卸载、升级等工作。但是rpm软件包之间的依赖性问题往往会很繁琐,尤其是软件由多个rpm包组成时。

Yum（全称为 Yellow dog Updater, Modified）是一个在Fedora和RedHat以及SUSE中的Shell前端软件包管理器。基於RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软体包，无须繁琐地一次次下载、安装。

rpm 是linux的一种软件包名称，以.rmp结尾，安装的时候语法为：rpm -ivh，rpm包的安装有一个很大的缺点就是文件的关联性太大，有时候装一个软件要安装很多其他的软件包，很麻烦，所以为此RedHat小红帽开发了yum安装方法，他可以彻底解决这个关联性的问题，很方便，只要配置两个文件即可安装，安装方法是：yum -y install ，yum并不是一中包，而是安装包的软件。

简单点说, rpm 只能安装已经下载到本地机器上的rpm 包. yum能在线下载并安装rpm包,能更新系统,且还能自动处理包与包之间的依赖问题,这个是rpm 工具所不具备的。

yum与apt-get的相同点：

apt-get属于ubuntu、Debian的包管理工具

yum则属于Redhat、Centos包管理工具

明白了这两点，对于我们使用hadoop、openstack已经没有问题了。更详细参考：

一般来说著名的linux系统基本上分两大类：

1.RedHat系列：Redhat、Centos、Fedora等

2.Debian系列：Debian、Ubuntu等

RedHat 系列

1 常见的安装包格式 rpm包,安装rpm包的命令是“rpm -参数”

2 包管理工具 yum

3 支持tar包

Debian系列

1 常见的安装包格式 deb包,安装deb包的命令是“dpkg -参数”

2 包管理工具 apt-get

3 支持tar包

tar 只是一种压缩文件格式，所以，它只是把文件压缩打包而已。

rpm 相当于windows中的安装文件，它会自动处理软件包之间的依赖关系。

优缺点来说，rpm一般都是预先编译好的文件，它可能已经绑定到某种CPU或者发行版上面了。

tar一般包括编译脚本，你可以在你的环境下编译，所以具有通用性。

如果你的包不想开放源代码，你可以制作成rpm，如果开源，用tar更方便了。

tar一般都是源码打包的软件，需要自己解包，然后进行安装三部曲，./configure, make, make install.　来安装软件。

rpm是redhat公司的一种软件包管理机制，直接通过rpm命令进行安装删除等操作，最大的优点是自己内部自动处理了各种软件包可能的依赖关系。

------------------------------------------------------------------------------------------------------------------------------------

*.rpm形式的二进制软件包[centos]

　　安装：rpm -ivh *.rpm

　　卸载：rpm -e packgename

rpm -q nginx 查看是否已经安装

　升级：rpm -Uvh xxx

　查询：

查询所有安装的包： rpm -qa

查询某个包：rpm -qa | grep xxx

rpm -qi xxx

查询软件的安装路径：rpm -ql xxx

rpm -qc xxx

查询某个文件是哪个rpm包产生：rpm -qf /etc/yum.conf

rpm -qpi xxx

rpm -qa|grep php 查看已安装的RMP包

安装：rpm -ivh xxx

移除：rpm -e xxx

升级：rpm -Uvh xxx

查询：

查询所有安装的包： rpm -qa

查询某个包：rpm -qa | grep xxx

rpm -qi xxx

查询软件的安装路径：rpm -ql xxx

rpm -qc xxx

查询某个文件是那个rpm包产生：rpm -qf /etc/yum.conf

rpm -qpi xxx

------------------------------------------------------------------------------------------------------------------------------------

src.rpm 源代码分发软件包的安装与卸载

　　Linux软件的源代码分发是指提供了该软件所有程序源代码的发布形式，需要用户自己编译成可执行的二进制代码并进行安装，其优点是配置灵活，可以随意去掉或保留某些功能/模块，适应多种硬件/操作系统平台及编译环境，缺点是难度较大，一般不适合初学者使用。

　　1、*.src.rpm形式的源代码软件包

　　安装：rpm -rebuild *.src.rpm

　　cd /usr/src/dist/RPMS

　　rpm -ivh *.rpm

　　卸载：rpm -e packgename

　　说明：rpm –rebuild *.src.rpm命令将源代码编译并在/usr/src/dist/RPMS下生成二进制的rpm包，然后再安装该二进制包即可。packgename如前所述。

------------------------------------------------------------------------------------------------------------------------------------

dpkg【ubuntu】

dpkg -l | grep 'php' 使用dpkg -l 来查看已经安装了的软件

dpkg 是Debian[待宾] Package 的简写。为 Debian 专门开发的套件管理系统，方便软件的安装、更新及移除。所有源自Debian的Linux 发行版都使用 dpkg，例如 Ubuntu、Knoppix 等。

　　以下是一些 Dpkg 的普通用法：

　　1、dpkg -i <package.deb>

　　安装一个 Debian 软件包，如你手动下载的文件。

　　2、dpkg -c <package.deb>

　　列出 <package.deb> 的内容。

　　3、dpkg -I <package.deb>

　　从 <package.deb> 中提取包裹信息。

　　4、dpkg -r <package>

　　移除一个已安装的包裹。

　　5、dpkg -P <package>

　　完全清除一个已安装的包裹。和 remove 不同的是，remove 只是删掉数据和可执行文件，purge 另外还删除所有的配制文件。

　　6、dpkg -L <package>

　　列出 <package> 安装的所有文件清单。同时请看 dpkg -c 来检查一个 .deb 文件的内容。

　　7、dpkg -s <package>

　　显示已安装包裹的信息。同时请看 apt-cache 显示 Debian 存档中的包裹信息，以及 dpkg -I 来显示从一个 .deb 文件中提取的包裹信息。

　　8、dpkg-reconfigure <package>

　　重新配制一个已经安装的包裹，如果它使用的是 debconf (debconf 为包裹安装提供了一个统一的配制界面)。

------------------------------------------------------------------------------------------------------------------------------------

使用yum和apt-get。软件管理方法的升级.

yum的配置文件是/etc/yum.conf

1. 我们来先讲Redhat的yum 这种高级的包管理.

yum install gcc [centos]

更新：yum update

安装：yum install xxx

移除：yum remove xxx

清除已经安装过的档案（/var/cache/yum/）：yum clean all

搜寻：yum search xxx

列出所有档案：yum list

查询档案讯息：yum info xxx

#sudo -s

#LANG=C

#yum -y install gcc gcc-c autoconf libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libpng libpng-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel

用YUM安装软件包

yum -y <package_name>

命令：yum install <package_name>

用YUM删除软件包

命令：yum remove <package_name>

yum -y remove httpd*

命令：yum search <keyword>

列出所有可安装的软件包

命令：yum list

yum list php*

列出所有可更新的软件包

命令：yum list updates

列出所有已安装的软件包

命令：yum list installed

列出所有已安装但不在 Yum Repository 內的软件包

命令：yum list extras

列出所指定的软件包

命令：yum list <package_name>

yum = Yellow dog Updater, Modified

主要功能是更方便的添加/删除/更新RPM包.

它能自动解决包的倚赖性问题.

它能便于管理大量系统的更新问题

yum特点

可以同时配置多个资源库(Repository)

简洁的配置文件(/etc/yum.conf

自动解决增加或删除rpm包时遇到的倚赖性问题

使用方便

保持与RPM数据库的一致性

yum安装

CentOS 自带(yum-*.noarch.rpm)

#rpm -ivh yum-*.noarch.rpm

在第一次启用yum之前首先需要导入系统的RPM-GPG-KEY：

#rpm --import /usr/share/doc/centos-release-3(4)/RPM-GPG-KEY-CentOS-3(4)

yum指令

注:当第一次使用yum或yum资源库有更新时,yum会自动下载 所有所需的headers放置于/var/cache/yum目录下,所需时间可能较长.

rpm包的更新

检查可更新的rpm包

#yum check-update

更新所有的rpm包

#yum update

更新指定的rpm包,如更新kernel和kernel source

#yum update kernel kernel-source

大规模的版本升级,与yum update不同的是,连旧的淘汰的包也升级

#yum upgrade

rpm包的安装和删除

安装rpm包,如xmms-mp3

#yum install xmms-mp3

删除rpm包,包括与该包有倚赖性的包

#yum remove licq

注:同时会提示删除licq-gnome,licq-qt,licq-text


yum暂存(/var/cache/yum/)的相关参数

清除暂存中rpm包文件

#yum clean packages

清除暂存中rpm头文件

#yum clean headers

清除暂存中旧的rpm头文件

#yum clean oldheaders

清除暂存中旧的rpm头文件和包文件

#yum clean 或#yum clean all

注:相当于yum clean packages + yum clean oldheaders


包列表

列出资源库中所有可以安装或更新的rpm包

#yum list

列出资源库中特定的可以安装或更新以及已经安装的rpm包

#yum list mozilla#yum list mozilla*

注:可以在rpm包名中使用匹配符,如列出所有以mozilla开头的rpm包

列出资源库中所有可以更新的rpm包

#yum list updates

列出已经安装的所有的rpm包

#yum list installed

列出已经安装的但是不包含在资源库中的rpm包

#yum list extras

注:通过其它网站下载安装的rpm包


rpm包信息显示(info参数同list)

列出资源库中所有可以安装或更新的rpm包的信息

#yum info

列出资源库中特定的可以安装或更新以及已经安装的rpm包的信息

#yum info mozilla#yum info mozilla*

注:可以在rpm包名中使用匹配符,如列出所有以mozilla开头的rpm包的信息

列出资源库中所有可以更新的rpm包的信息

#yum info updates

列出已经安装的所有的rpm包的信息

#yum info installed

列出已经安装的但是不包含在资源库中的rpm包的信息

#yum info extras

注:通过其它网站下载安装的rpm包的信息


搜索rpm包

搜索匹配特定字符的rpm包

#yum search mozilla

注:在rpm包名,包描述等中搜索

搜索有包含特定文件名的rpm包

#yum provides realplay


增加资源库

例如:增加http://rpm.livna.org作为资源库

安装http://Livna.org rpms GPG key

#rpm --import http://rpm.livna.org/RPM-LIVNA-GPG-KEY

检查GPG Key

# rpm -qa gpg-pubkey*

显示Key信息

#rpm -qi gpg-pubkey-a109b1ec-3f6e28d5

(注:如果要删除Key,使用#rpm -e gpg-pubkey-a109b1ec-3f6e28d5)


yum常用的命令


# yum install xxx 安装xxx软件


# yum info xxx 查看xxx软件的信息


# yum remove xxx 删除软件包


# yum list 列出软件包


# yum clean 清除缓冲和就的包


# yum provides xxx 以xxx为关键字搜索包（提供的信息为关键字）


# yum search xxx 搜索软件包（以名字为关键字）


# yum groupupdate xxx


# yum grouplist xxx


# yum groupremove xxx


这三个都是一组为单位进行升级 列表和删除的操作。。比如 "Mysql Database"就是一个组会同时操作相关的所有软件包；


# yum update 系统升级


# yum list available 列出所有升级源上的包；


# yum list updates 列出所有升级源上的可以更新包；


# yum list installed 列出已经安装的包；


# yun update kernel 升级内核；


yum常用的源


1) 自动选择最快的源


由于yum中有的mirror速度是非常慢的，如果yum选择了这个mirror，这个时候yum就会非常慢，对此，可以下载fastestmirror插件，它会自动选择最快的mirror：


#yum install yum-fastestmirror


配置文件：（一般不用动）/etc/yum/pluginconf.d/fastestmirror.conf


你的yum镜像的速度测试记录文件：/var/cache/yum/timedhosts.txt


(2)使用图形界面的yum


如果觉得命令行的yum不方便，那么可以使用图形化的yumex，这个看起来更方便，因为可以自由地选择软件仓库：


#yum install yumex


然后在系统工具中就可以看到yum extender了。实际上系统自带的“添加/删除程序“也可以实现图形化的软件安装，但有些yumex的功能它没有。




2.讲讲Ubuntu中的高级包管理方法apt-get

配置文件/etc/apt/sources.list

对于Server版， 推荐使用aptitude来查看，安装、删除deb包

sudo apt-get install aptitude

然后执行 sudo aptitude 进入管 理

也可以使用命令：

aptitude update 更新可用的包列表

aptitude upgrade 升级可用的包

aptitude dist-upgrade 将系统升级到新的发行版

aptitude install pkgname 安装包

aptitude remove pkgname 删除包

aptitude purge pkgname 删除包及其配置文件

aptitude search string 搜索包

aptitude show pkgname 显示包的详细信息

aptitude clean 删除下载的包文件

aptitude autoclean 仅删除过期的包文件

