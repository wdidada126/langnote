# mysql doc

version 5.7

https://dev.mysql.com/doc/refman/5.7/en/

USE，比如 QUIT ，不需要分号

```mysql

补充：删除数据库

drop database databasenames;
```

清空数据库的数据



```mysql
mysqladmin -u root -p drop databasenames;
```





```mysql
USE menagerie
```



注意：不用分号



```mysql
SELECT DATABASE();
```



### 3.3.2创建表



```mysql
SHOW TABLES;
CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
```

```mysql
SHOW TABLES;
```

```mysql
DESCRIBE pet;
```



LOAD DATA Syntax

pet.txt

```mysql
LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```



### Security Issues with LOAD DATA LOCAL

load data默认不开启



INSERT

```mysql
INSERT INTO pet VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);
```



```mysql
SELECT * FROM pet;
```



updata

```mysql
DELETE FROM pet;
LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```



```mysql
UPDATE pet SET birth = '1989-08-31' WHERE name = 'Bowser';
```



```mysql
SELECT * FROM pet WHERE birth >= '1998-1-1';
SELECT * FROM pet WHERE species = 'dog' AND sex = 'f';
SELECT * FROM pet WHERE species = 'snake' OR species = 'bird';
SELECT * FROM pet WHERE (species = 'cat' AND sex = 'm') OR (species = 'dog' AND sex = 'f');
```



#### 3.3.4.3



```mysql
SELECT name, birth FROM pet;
```



distinct

```mysql
SELECT DISTINCT owner FROM pet;
```



```mysql
SELECT name, species, birth FROM pet WHERE species = 'dog' OR species = 'cat';
```



#### 3.3.4.4



```mysql
SELECT name, birth FROM pet ORDER BY birth;
```

```mysql
SELECT name, birth FROM pet ORDER BY birth DESC;

CREATE DATABASE menagerie;

```

mysql query batch module
