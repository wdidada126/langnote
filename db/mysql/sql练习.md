# sql练习




Field	Type	Null	Key	Default	Extra
name	varchar(50)	NO	PRI	null	
continent	varchar(60)	YES	MUL	null	
area	decimal(10,0)	YES		null	
population	decimal(11,0)	YES		null	
gdp	decimal(14,0)	YES		null	
capital	varchar(60)	YES		null	
tld	varchar(5)	YES		null	
flag	varchar(255)	YES		null	

select count(1) from world;
195

select version();
10.3.27-MariaDB-0+deb10u1


```sql
drop table if exists  `employees` ; 
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');
INSERT INTO employees VALUES(10004,'1954-05-01','Chirstian','Koblick','M','1986-12-01');
INSERT INTO employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
INSERT INTO employees VALUES(10007,'1957-05-23','Tzvetan','Zielinski','F','1989-02-10');
INSERT INTO employees VALUES(10008,'1958-02-19','Saniya','Kalloufi','M','1994-09-15');
INSERT INTO employees VALUES(10009,'1952-04-19','Sumant','Peac','F','1985-02-18');
INSERT INTO employees VALUES(10010,'1963-06-01','Duangkaew','Piveteau','F','1989-08-24');
INSERT INTO employees VALUES(10011,'1953-11-07','Mary','Sluis','F','1990-01-22');
INSERT INTO employees VALUES(10012,'1959-04-19','Sumant-1','Peac-1','F','1985-02-18');
```


select * from employees order by hire_date desc limit 1;
select min(hire_date) from employees;
select * from employees where hire_date = (select min(hire_date) from employees);



```sql
drop table if exists grade;
CREATE TABLE  grade(
`id` int(4) NOT NULL,
`job` varchar(32) NOT NULL,
`score` int(10) NOT NULL,
PRIMARY KEY (`id`));
INSERT INTO grade VALUES
(1,'C++',11001),
(2,'C++',10000),
(3,'C++',9000),
(4,'Java',12000),
(5,'Java',13000),
(6,'前端',12000),
(7,'前端',11000),
(8,'前端',9999);
```

```sql
select job, round(avg(score),3) from grade group by job order by avg(score) desc;
```

```sql
drop table if exists person;
drop table if exists task;
CREATE TABLE `person` (
`id` int(4) NOT NULL,
`name` varchar(32) NOT NULL,
PRIMARY KEY (`id`));

CREATE TABLE `task` (
`id` int(4) NOT NULL,
`person_id` int(4) NOT NULL,
`content` varchar(32) NOT NULL,
PRIMARY KEY (`id`));

INSERT INTO person VALUES
(1,'fh'),
(2,'tm');

INSERT INTO task VALUES
(1,2,'tm works well'),
(2,2,'tm works well');
```

```
select p.id, p.name, t.content
from person p left join task t on p.id = t.person_id
order by p.id;
```

sql练习

高级函数
group by
join
排序
order desc(倒序)

order by后面可以跟sum函数

where having的区别
having后面可以跟sum函数

临时表

union all

MyBatis动态SQL

https://www.nowcoder.com/activity/oj


