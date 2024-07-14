# firefox

## mdn

MDN是Mozilla基金会的开发者网络平台。提供了大量关于各种HTML、CSS和JavaScript功能的开放、详细的文档，以及广泛的Web API参考资料。

## version


firefox英文版本
https://www.mozilla.org/en-US/firefox/download/thanks/

## source code
https://firefox-source-docs.mozilla.org/setup/linux_build.html
linux debian

```shell
sudo apt update
sudo apt-get install curl python3 python3-pip -y
python3 -m pip install --user mercurial
echo 'export PATH="'"$(python3 -m site --user-base)"'/bin:$PATH"' >> ~/.bashrc
curl https://hg.mozilla.org/mozilla-central/raw-file/default/python/mozboot/bin/bootstrap.py -O
python3 bootstrap.py
cd mozilla-unified
hg up -C central
./mach build
```

https://github.com/mozilla/gecko-dev

https://hg.mozilla.org/mozilla-central/

echo | python3 bootstrap.py

Python headers are required to build Mercurial but weren't found in /opt/rh/rh-python38/root/usr/include/python3.8/Python.h
