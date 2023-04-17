# mysql table


0 1 status数据 mysql表中设置成什么类型

0/1或者true/false类型的数据通常可以设置成TINYINT(1)或BOOLEAN类型。在 MySQL 中，BOOLEAN 实际上被实现为 TINYINT(1)。所以这两种类型都可以用来存储布尔值。如果只需要存储 0/1 或 true/false 值，则可以选择使用 TINYINT(1)，它占用的空间更小。