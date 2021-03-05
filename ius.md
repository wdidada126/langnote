# ius


EPEL scl

https://www.softwarecollections.org/en/
https://www.softwarecollections.org/en/scls/rhscl/devtoolset-8/



https://repo.ius.io/7/x86_64/packages/g/

git222-core-2.22.4-1.el7.ius.x86_64.rpm

git rpm包


https://ius.io/faq

How is IUS different from SCL?
IUS and Software Collections (SCL) both seek to solve the problem of providing optional newer versions of software for Enterprise Linux. They differ significantly in execution.

Most IUS packages are designed to safely replace their stock equivalent, but SCL packages are designed to be parallel installable with stock packages (and each other). This means that SCL packages must install to alternate paths such as /opt/, /etc/opt/, and /var/opt/. Most IUS packages can be used just like their stock equivalents, but commands from SCL packages must be used through the scl wrapper script. Daemons from SCL packages are named differently as well.

IUS packages follow upstream releases, but SCL packages have independent life cycles that may be shorter or longer than the upstream software.


