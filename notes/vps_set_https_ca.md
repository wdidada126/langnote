


# 腾讯云主机添加 let`s encrypt证书过程
- 域名
- 域名解析服务
- apache服务器(httpd)
- certbot工具

### 添加普通账户赋权
- 1、adduser xxusername //xxusername可以替换成任意用户名
- 2、passwd xxusername  //xxusername 与上一步adduser的相同
- 3、进入超级用户模式。也就是输入"su -",系统会让你输入超级用户密码，输入密码后就进入了超级用户模式。（当然，你也可以直接用root用）
编辑/etc/sudoers文件。也就是输入命令"vim /etc/sudoers",进入编辑模式，找到这一 行："root ALL=(ALL) ALL"在起下面添加"xxx ALL=(ALL) ALL"(这里的xxx是你的用户名)，然后保存退出。
然后就行了。

### 安装服务器软件
```shell
sudo yum install httpd
sudo service httpd start
```

### 安装certbot
```shell
sudo yum install certbot-apache
```

### 配置dns服务器解析到vps的ip

### 配置httpd
打开文件 /etc/httpd/conf/httpd.conf, 搜索 VirtualHost example, 找到代码如下:

```shell
<VirtualHost *:80>
    ServerName edibeta.top
    ServerAlias www.edibeta.top
    DocumentRoot /var/www/html
</VirtualHost>
```

### 运行certbot
```shell
sudo certbot --apache -d edibeta.top -d www.edibeta.top
```

[edidada@VM_0_15_centos httpd]$ sudo certbot --apache
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator apache, Installer apache
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): 1664884095@qq.com
Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org

-------------------------------------------------------------------------------
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v01.api.letsencrypt.org/directory
-------------------------------------------------------------------------------
(A)gree/(C)ancel: A

-------------------------------------------------------------------------------
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about EFF and
our work to encrypt the web, protect its users and defend digital rights.
-------------------------------------------------------------------------------
(Y)es/(N)o: Y
Starting new HTTPS connection (1): supporters.eff.org
No names were found in your configuration files. Please enter in your domain
name(s) (comma and/or space separated)  (Enter 'c' to cancel): edibeta.com
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for edibeta.com
Cleaning up challenges
Unable to find a virtual host listening on port 80 which is currently needed for Certbot to prove to the CA that you control your domain. Please add a virtual host for port 80.

IMPORTANT NOTES:
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
[edidada@VM_0_15_centos httpd]$ sudo certbot --apache
[sudo] password for edidada: 
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator apache, Installer apache
Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org
No names were found in your configuration files. Please enter in your domain
name(s) (comma and/or space separated)  (Enter 'c' to cancel): edidada.top
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for edidada.top
Cleaning up challenges
Unable to find a virtual host listening on port 80 which is currently needed for Certbot to prove to the CA that you control your domain. Please add a virtual host for port 80.


sudo certbot --apache
[sudo] password for edidada: 
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator apache, Installer apache
Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org

Which names would you like to activate HTTPS for?
-------------------------------------------------------------------------------
1: edibeta.top
2: www.edibeta.top
-------------------------------------------------------------------------------
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 1
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for edibeta.top
Waiting for verification...
Cleaning up challenges
Created an SSL vhost at /etc/httpd/conf/httpd-le-ssl.conf
Deploying Certificate to VirtualHost /etc/httpd/conf/httpd-le-ssl.conf
Enabling site /etc/httpd/conf/httpd-le-ssl.conf by adding Include to root configuration

Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
-------------------------------------------------------------------------------
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 1

-------------------------------------------------------------------------------
Congratulations! You have successfully enabled https://edibeta.top

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=edibeta.top
-------------------------------------------------------------------------------

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/edibeta.top/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/edibeta.top/privkey.pem
   Your cert will expire on 2018-06-19. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le

[edidada@VM_0_15_centos ~]$ sudo certbot --apache
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator apache, Installer apache
Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org

Which names would you like to activate HTTPS for?
-------------------------------------------------------------------------------
1: edibeta.top
2: www.edibeta.top
-------------------------------------------------------------------------------
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 2
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for www.edibeta.top
Waiting for verification...
Cleaning up challenges
Deploying Certificate to VirtualHost /etc/httpd/conf/httpd-le-ssl.conf

Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
-------------------------------------------------------------------------------
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 1

-------------------------------------------------------------------------------
Congratulations! You have successfully enabled https://www.edibeta.top

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=www.edibeta.top
-------------------------------------------------------------------------------

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/www.edibeta.top/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/www.edibeta.top/privkey.pem
   Your cert will expire on 2018-06-19. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le


   
sudo certbot --apache -d edibeta.top -d www.edibeta.top

http://blog.csdn.net/jianwushuang/article/details/8948525

1. 打开文件 /etc/httpd/conf/httpd.conf, 搜索 VirtualHost example, 找到代码如下:



<VirtualHost *:80>
    ServerName edibeta.top
    ServerAlias www.edibeta.top
    DocumentRoot /var/www/html
</VirtualHost>


scp -r root@193.112.11.197:/etc/letsencrypt /d