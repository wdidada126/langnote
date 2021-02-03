# mtools

mtools is a collection of helper scripts to parse, filter, and visualize MongoDB log files (mongod, mongos). mtools also includes mlaunch, a utility to quickly set up complex MongoDB test environments on a local machine, and mtransfer, a tool for transferring databases between MongoDB instances.
https://github.com/rueckstiess/mtools


# cd /tmp
# git clone https://github.com/rueckstiess/mtools.git
# cd mtools
# git status
# git branch -a
# git checkout master
# more INSTALL.md
# python setup.py install

# which mloginfo
/usr/local/bin/mloginfo
# ls -lt /usr/local/bin |more
total 6216
-rwxr-xr-x 1 root root     384 May 31 19:57 mlaunch
-rwxr-xr-x 1 root root     390 May 31 19:57 mlogfilter
-rwxr-xr-x 1 root root     386 May 31 19:57 mloginfo
-rwxr-xr-x 1 root root     384 May 31 19:57 mlogvis
-rwxr-xr-x 1 root root     394 May 31 19:57 mplotqueries
-rwxr-xr-x 1 root root     388 May 31 19:57 mgenerate

