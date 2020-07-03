create database chap4;
use chap4;
create table date1(date1 date);
insert into date1 values ('1949-10-01');
insert into date1 values ('1950#2#3');
insert into date1 values ('1951@3@4');
select * from date1;

create table datetime1(datetime1 datetime);
insert into datetime1 values ('1949-10-01 11:11:11');
insert into datetime1 values ('1950#2#3 11+11+11');

create database example;

show databases;

drop database example;

show engines;

