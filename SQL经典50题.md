# SQL经典50题

腾讯云 mysql数据库服务

SQL经典50题（MySQL版）
https://blog.csdn.net/weixin_49984044/article/details/109267061


互联网校招SQL笔试经典50题及答案解析
https://zhuanlan.zhihu.com/p/53302593


SQL经典50题 | 附答案
https://blog.csdn.net/u010226597/article/details/106334861/



已知有以下4张表：
学生表：student(s_id,s_name,s_age,s_sex) –– 学号,学生姓名,出生年月,性别
成绩表：score(s_id,c_id,score) –– 学号,课程号,成绩
课程表：course(c_id,c_name,t_id) –– 课程号,课程名称,教师号
教师表：teacher(t_id,t_name) –– 教师号,教师姓名


```sql
-- 创建学生表
CREATE TABLE IF NOT EXISTS Student(
    s_id VARCHAR(10),
    s_name VARCHAR(20),
    s_age DATE,
    s_sex VARCHAR(10)
);
-- 往学生表中插入数据
INSERT INTO Student VALUES('01' , '赵雷' , '1990-01-01' , '男');
INSERT INTO Student VALUES('02' , '钱电' , '1990-12-21' , '男');
INSERT INTO Student VALUES('03' , '孙风' , '1990-05-20' , '男');
INSERT INTO Student VALUES('04' , '李云' , '1990-08-06' , '男');
INSERT INTO Student VALUES('05' , '周梅' , '1991-12-01' , '女');
INSERT INTO Student VALUES('06' , '吴兰' , '1992-03-01' , '女');
INSERT INTO Student VALUES('07' , '郑竹' , '1989-07-01' , '女');
INSERT INTO Student VALUES('08' , '王菊' , '1990-01-20' , '女');
```

```sql
-- 创建课程表
CREATE TABLE IF NOT EXISTS Course (
    c_id VARCHAR(10),
    c_name VARCHAR(20),
    t_id VARCHAR(10)
);
-- 往课程表插入数据
INSERT INTO Course VALUES('01' , '语文' , '02');
INSERT INTO Course VALUES('02' , '数学' , '01');
INSERT INTO Course VALUES('03' , '英语' , '03');
```

```sql
-- 创建教师表
CREATE TABLE IF NOT EXISTS Teacher (
    t_id VARCHAR(10),
    t_name VARCHAR(20)
);
-- 往教师表插入数据
INSERT INTO Teacher VALUES('01' , '张三');
INSERT INTO Teacher VALUES('02' , '李四');
INSERT INTO Teacher VALUES('03' , '王五');
```


```sql
-- 创建成绩表
CREATE TABLE IF NOT EXISTS Score (
    s_id VARCHAR(10),
    c_id VARCHAR(10),
    score VARCHAR(10)
);
-- 往成绩表插入数据
INSERT INTO Score VALUES('01' , '01' , 80);
INSERT INTO Score VALUES('01' , '02' , 90);
INSERT INTO Score VALUES('01' , '03' , 99);
INSERT INTO Score VALUES('02' , '01' , 70);
INSERT INTO Score VALUES('02' , '02' , 60);
INSERT INTO Score VALUES('02' , '03' , 80);
INSERT INTO Score VALUES('03' , '01' , 80);
INSERT INTO Score VALUES('03' , '02' , 80);
INSERT INTO Score VALUES('03' , '03' , 80);
INSERT INTO Score VALUES('04' , '01' , 50);
INSERT INTO Score VALUES('04' , '02' , 30);
INSERT INTO Score VALUES('04' , '03' , 20);
INSERT INTO Score VALUES('05' , '01' , 76);
INSERT INTO Score VALUES('05' , '02' , 87);
INSERT INTO Score VALUES('06' , '01' , 31);
INSERT INTO Score VALUES('06' , '03' , 34);
INSERT INTO Score VALUES('07' , '02' , 89);
INSERT INTO Score VALUES('07' , '03' , 98);
```


-- 1、查询"01"课程比"02"课程成绩高的学生的学号及课程分数
SELECT a.s_id AS s_id, score1, score2
FROM 
(SELECT s_id, score AS score1 FROM Score WHERE c_id = '01') a
INNER JOIN
(SELECT s_id, score AS score2 FROM Score WHERE c_id = '02') b
ON a.s_id = b.s_id WHERE score1 > score2;



-- 2、查询"01"课程比"02"课程成绩高的学生的信息及课程分数
SELECT s.*, a.score AS score1, b.score AS score2
FROM Student s,
     (SELECT s_id,score FROM Score WHERE c_id = '01') a,
     (SELECT s_id,score FROM Score WHERE c_id = '02') b
WHERE a.s_id = b.s_id AND a.score > b.score AND s.`s_id` = a.s_id;



-- 3、查询平均成绩大于等于60分的同学的学生编号和学生姓名和平均成绩
SELECT s.`s_id`,s.`s_name`,AVG(score) AS avg_score 
FROM student AS s,score AS sc
WHERE s.`s_id` = sc.`s_id` 
GROUP BY s.`s_id`
HAVING avg_score >= 60;



-- 3、(法二)查询平均成绩大于等于60分的同学的学生编号和学生姓名和平均成绩
SELECT s.`s_id`,s.`s_name`,b.avg_score AS avg_score 
FROM Student s
RIGHT JOIN
(SELECT s_id, AVG(score) AS avg_score FROM score
GROUP BY s_id HAVING avg_score >= 60) b
ON s.`s_id` = b.s_id;


-- 4、查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩(没成绩显示null)
SELECT s.`s_id`,s_name,COUNT(c_id)AS 选课总数,SUM(score) AS 总成绩
FROM student s
LEFT JOIN score sc
ON s.`s_id` = sc.`s_id`
GROUP BY s_id;




-- 5、查询姓“李”的老师的个数
SELECT COUNT(t_name) AS 人数
FROM teacher 
WHERE t_name LIKE '李%';


-- 6、查询没学过“张三”老师课的学生的学号、姓名
SELECT s_id, s_name FROM Student WHERE s_id NOT IN
(SELECT s_id FROM score WHERE c_id IN
(SELECT c_id FROM course WHERE t_id IN 
(SELECT t_id 
FROM teacher 
WHERE t_name = '张三')));

-- 法二
SELECT s_id, s_name 
FROM student
WHERE s_id NOT IN(SELECT sc.s_id FROM score sc
INNER JOIN course co ON sc.`c_id` = co.`c_id`
INNER JOIN teacher te ON co.`t_id`= te.`t_id`
WHERE te.`t_name`='张三');

-- 法三
SELECT s_id, s_name
FROM Student
WHERE s_name NOT IN (
    SELECT s.s_name
    FROM student AS s, course AS c, teacher AS t, score AS sc
    WHERE s.s_id = sc.s_id
        AND sc.c_id = c.c_id
        AND c.t_id = t.t_id
        AND t.t_name = '张三');



-- 7、查询学过编号为“01”的课程并且也学过编号为“02”的课程的学生的学号、姓名
SELECT s_id,s_name 
FROM Student 
WHERE s_id IN (
SELECT s_id
FROM score
WHERE c_id = '01' OR c_id = '02'
GROUP BY s_id
HAVING COUNT(c_id) >= 2);




--  8、查询课程编号为“02”的总成绩
SELECT SUM(score) AS 总成绩
FROM score
WHERE c_id = '02';





-- 9、查询没有学全所有课的学生的学号、姓名
SELECT st.`s_id`,st.`s_name` 
FROM student st
INNER JOIN score sc
ON st.`s_id` = sc.`s_id`
GROUP BY sc.`s_id`
HAVING COUNT(sc.`c_id`) < (SELECT
COUNT(DISTINCT c_id) 
FROM course);


-- 10、查询至少有一门课与学号为“01”的学生所学课程相同的学生的学号和姓名
SELECT st.`s_id`,st.`s_name`
FROM Student st 
WHERE st.`s_id` IN(
SELECT DISTINCT sc.`s_id` 
FROM score sc
WHERE sc.`c_id` IN(
SELECT sc.`c_id`
FROM score sc
WHERE sc.`s_id` = 01)) AND
st.`s_id` <> '01';

-- 法二
SELECT DISTINCT st.`s_id`,st.`s_name`
FROM Student st 
INNER JOIN score sc
ON st.`s_id`= sc.`s_id`
WHERE sc.`c_id` IN(
SELECT sc.`c_id`
FROM score sc
WHERE sc.`s_id` = '01') AND
st.`s_id` <> '01';





-- 11、查询和“01”号同学所学课程完全相同的其他同学的信息
SELECT DISTINCT st.* 
FROM Student st
INNER JOIN score sc
ON st.`s_id` = sc.`s_id`
WHERE sc.`c_id` IN
(SELECT sc.`c_id`
FROM score sc
WHERE sc.`s_id`= '01') AND  sc.`s_id` <> '01'
GROUP BY sc.`s_id`
HAVING COUNT(sc.`c_id`) = (SELECT
COUNT(c_id) FROM score WHERE s_id = '01');


-- 12、查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩
SELECT st.`s_id`,st.`s_name`,AVG(sc.score) AS avg_score
FROM Student st, score sc 
WHERE st.`s_id` = sc.`s_id`
AND sc.`score` < 60
GROUP BY sc.`s_id`
HAVING COUNT(sc.`c_id`) >= 2;



-- 13、检索"01"课程分数小于60，按分数降序排列的学生信息
SELECT st.*,sc.`score`
FROM Student st
INNER JOIN score sc ON 
st.`s_id`= sc.`s_id` 
WHERE sc.`c_id` = '01' AND sc.`score` < 60
ORDER BY sc.`score` DESC;



-- 14、按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩
SELECT s_id, 
SUM(CASE WHEN c_id = '01' THEN score ELSE NULL END) AS score1,
SUM(CASE WHEN c_id = '02' THEN score ELSE NULL END) AS score2,
SUM(CASE WHEN c_id = '03' THEN score ELSE NULL END) AS score3,
AVG(score)
FROM score
GROUP BY s_id
ORDER BY AVG(score) DESC;




--  15、查询各科成绩最高分、最低分、平均分、及格率、中等率、优良率、优秀率
--      要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
--      以如下形式显示：课程ID，课程name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率
--      及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90 
-- 先从简单的写法开始，及格率直接用小数表示，没用百分号
SELECT co.c_id AS 课程ID, co.c_name AS 课程名称, COUNT(*) AS 选修人数, 
   MAX(score) AS 最高分 , MIN(score) AS 最低分, AVG(score) AS 平均分,
   SUM(CASE WHEN score >= 60 THEN 1 ELSE 0 END) / COUNT(*) AS  '及格率',
   SUM(CASE WHEN score BETWEEN 70 AND 80 THEN 1 ELSE 0 END) / COUNT(*) AS  '中等率',
   SUM(CASE WHEN score BETWEEN 80 AND 90 THEN 1 ELSE 0 END) / COUNT(*) AS  '优良率',
   SUM(CASE WHEN score >= 90 THEN 1 ELSE 0 END) / COUNT(*) AS  '优秀率'
FROM score sc, course co
WHERE sc.c_id = co.c_id	
GROUP BY co.c_id
ORDER BY COUNT(*) DESC, co.c_id;

-- 复杂点的写法，及格率用百分号表示
SELECT a.c_id AS '课程ID', course.c_name AS '课程name', COUNT(*) AS 选修人数,
       MAX(a.score) AS '最高分',  MIN(a.score) AS '最低分',
       CAST(AVG(a.score) AS DECIMAL(5,2)) AS '平均分',
       CONCAT(CAST(SUM(pass)/COUNT(*)*100 AS DECIMAL(5,2)),'%') AS '及格率',
       CONCAT(CAST(SUM(medi)/COUNT(*)*100 AS DECIMAL(5,2)),'%') AS '中等率',
       CONCAT(CAST(SUM(good)/COUNT(*)*100 AS DECIMAL(5,2)),'%') AS '优良率',
       CONCAT(CAST(SUM(excellent)/COUNT(*)*100 AS DECIMAL(5,2)),'%') AS '优秀率' 
FROM
    (SELECT * ,
        CASE WHEN score>=60 THEN 1 ELSE 0 END AS pass,
        CASE WHEN score>=70 AND score<80 THEN 1 ELSE 0 END AS medi,
        CASE WHEN score>=80 AND score<90 THEN 1 ELSE 0 END AS good,
        CASE WHEN score>=90 THEN 1 ELSE 0 END AS excellent
     FROM score) a
LEFT JOIN course ON a.c_id=course.c_id
GROUP BY a.c_id
ORDER BY COUNT(*) DESC, a.c_id;



SELECT s.*, rank_01, rank_02, rank_03, rank_total
FROM student s
LEFT JOIN (SELECT s_id, rank() over(PARTITION BY c_id ORDER BY score DESC) AS rank_01 FROM score WHERE c_id=01) A ON s.s_id=A.s_id
LEFT JOIN (SELECT s_id, rank() over(PARTITION BY c_id ORDER BY score DESC) AS rank_02 FROM score WHERE c_id=02) B ON s.s_id=B.s_id
LEFT JOIN (SELECT s_id, rank() over(PARTITION BY c_id ORDER BY score DESC) AS rank_03 FROM score WHERE c_id=03) C ON s.s_id=C.s_id
LEFT JOIN (SELECT s_id, rank() over(ORDER BY AVG(score) DESC) AS rank_total FROM score GROUP BY s_id) D ON s.s_id=D.s_id
ORDER BY rank_total ASC;




-- 17、按各科成绩进行排序，并显示排名
SELECT a.`c_id`,a.`s_id`,a.`score`,COUNT(b.`score`)+1 AS rank 
FROM score a
LEFT JOIN score b
ON a.`score`< b.`score` AND a.`c_id`= b.`c_id`
GROUP BY a.`c_id`,a.`s_id`,a.`score`
ORDER BY a.`c_id`,rank;




-- 18、查询学生的总成绩并进行排名
SELECT a.*, @rank:= @rank+1 AS rank 
FROM 
  (SELECT s_id,SUM(score)
    FROM score 
    GROUP BY s_id 
    ORDER BY SUM(score) DESC) a,
  (SELECT @rank:=0) b;

-- 法二
SELECT s_id, SUM(score), rank() over(ORDER BY SUM(score) DESC) AS ranking
FROM score
GROUP BY s_id
ORDER BY ranking;




-- 19、查询不同老师所教不同课程平均分从高到低显示
SELECT te.`t_id`, te.`t_name`, AVG(sc.`score`)
FROM score sc INNER JOIN course co ON sc.`c_id`= co.`c_id`
INNER JOIN teacher te ON co.`t_id`= te.`t_id`
GROUP BY te.`t_id`
ORDER BY AVG(sc.`score`) DESC;


--  20、查询所有课程的成绩第2名到第3名的学生信息及该课程成绩
SELECT result.c_id, result.s_id, result.score, student.`s_name`,student.`s_age`,student.`s_sex`
FROM 
(SELECT *, IF(@pa=a.c_id, @rank:= @rank+1, @rank:=1) AS rank, @pa:=a.c_id
FROM 
(SELECT c_id, s_id,score FROM score
GROUP BY c_id, s_id ORDER BY c_id, score DESC) a,
(SELECT @rank:=0,@pa:=NULL) b) result
LEFT JOIN student ON result.s_id = student.`s_id`
WHERE rank BETWEEN 2 AND 3
GROUP BY c_id, score DESC;




--  21、使用分段[85-100],[70-84],[60-69],[<60]来统计各科成绩，分别统计各分数段人数：课程ID和课程名称
SELECT a.c_id AS '课程编号',course.c_name AS '课程名称',
SUM(level1) AS '[85-100]人数', SUM(level1)/COUNT(1) AS '[85-100]占比',
SUM(level2) AS '[70-84]人数', SUM(level2)/COUNT(1) AS '[70-84]占比',
SUM(level3) AS '[60-69]人数', SUM(level3)/COUNT(1) AS '[60-69]占比',
SUM(level4) AS '[0-59]人数', SUM(level4)/COUNT(1) AS '[0-59]占比' FROM
(SELECT *,
(CASE WHEN score BETWEEN 85 AND 100 THEN 1 ELSE 0 END) AS 'level1',
(CASE WHEN score BETWEEN 70 AND 84 THEN 1 ELSE 0 END) AS 'level2',
(CASE WHEN score BETWEEN 60 AND 69 THEN 1 ELSE 0 END) AS 'level3',
(CASE WHEN score BETWEEN 0 AND 59 THEN 1 ELSE 0 END) AS 'level4'
FROM score) a
LEFT JOIN course ON a.c_id=course.c_id
GROUP BY a.c_id;



-- 22、查询学生平均成绩及其名次
SELECT a.*,@rank:=@rank+1 AS rank
FROM 
  (SELECT s_id, AVG(score) AS '平均成绩' 
  FROM score 
  GROUP BY s_id
  ORDER BY AVG(score) DESC) a,
  (SELECT @rank:=0) b;





-- 23、查询各科成绩前三名的记录
SELECT a.`c_id`,a.`s_id`,a.`score`
FROM score a
WHERE
  (SELECT COUNT(b.s_id) FROM score b WHERE a.`c_id`=b.`c_id` AND a.`score`< b.`score`) < 3
GROUP BY a.`c_id`, a.`s_id`;




-- 24、查询每门课程被选修的学生数
SELECT c_id, COUNT(s_id) AS '选修人数'
FROM score
GROUP BY c_id;


-- 25、 查询出只有两门课程的全部学生的学号和姓名
SELECT s_id,s_name 
FROM student 
WHERE s_id IN(
SELECT s_id 
FROM score 
GROUP BY s_id
HAVING COUNT(c_id)=2);




-- 26、查询男生、女生人数
SELECT s_sex AS '性别',COUNT(*) AS  '人数'
FROM student
GROUP BY s_sex;




-- 27、查询名字中含有"风"字的学生信息
SELECT * 
FROM student 
WHERE s_name LIKE '%风%';


-- 28、查询同名同姓学生名单，并统计同名人数
SELECT s_name, num AS '同名人数'
FROM (
  SELECT *, COUNT(s_id) -1 AS num 
  FROM student
  GROUP BY s_name) a;





-- 29、查询1990年出生的学生名单
SELECT *
FROM student
WHERE YEAR(s_age) = '1990';


-- 30、查询平均成绩大于等于85的所有学生的学号、姓名和平均成绩
SELECT st.`s_id` AS '学号',st.`s_name` AS '姓名',AVG(score) AS '平均成绩'
FROM student st
INNER JOIN score sc 
ON st.`s_id`=sc.`s_id`
GROUP BY sc.`s_id`
HAVING AVG(score)>= 85;




-- 31、查询每门课程的平均成绩，结果按平均成绩升序排序，平均成绩相同时，按课程号降序排列
SELECT c_id, AVG(score) AS '平均成绩'
FROM score
GROUP BY c_id
ORDER BY AVG(score),c_id DESC;


-- 32、查询课程名称为"数学"，且分数低于60的学生姓名和分数
SELECT st.`s_id`,st.`s_name`,score 
FROM student st
INNER JOIN score sc
ON st.`s_id`=sc.`s_id`
WHERE score < 60 AND sc.`c_id` IN (
SELECT c_id 
FROM course 
WHERE c_name = '数学');




-- 33、查询所有学生的课程及分数情况
SELECT sc.`s_id`,
SUM(CASE WHEN co.c_name = '语文' THEN sc.score ELSE NULL END) AS '语文成绩',
SUM(CASE WHEN co.c_name = '数学' THEN sc.score ELSE NULL END) AS '数学成绩',
SUM(CASE WHEN co.c_name = '英语' THEN sc.score ELSE NULL END) AS '英语成绩'
FROM score sc INNER JOIN course co ON sc.`c_id`= co.`c_id`
GROUP BY sc.`s_id`;




-- 34、查询任何一门课程成绩在70分以上的姓名、课程名称和分数
SELECT st.`s_name` AS '姓名', co.`c_name` AS '课程名称',sc.`score` AS '分数'
FROM student st
INNER JOIN score sc ON st.`s_id`= sc.`s_id`
INNER JOIN course co ON sc.`c_id`= co.`c_id`
WHERE sc.`score` >= 70;





-- 35、查询不及格的课程并按课程号从大到小排列
SELECT co.`c_id`,co.`c_name`,sc.`score`
FROM course co
INNER JOIN score sc ON co.`c_id`=sc.`c_id`
WHERE score < 60
ORDER BY c_id DESC;





-- 36、查询课程编号为03且课程成绩在80分以上的学生的学号和姓名
SELECT st.`s_id` AS '学号',st.`s_name` AS '姓名'
FROM student st
INNER JOIN score sc ON st.`s_id`= sc.`s_id` 
WHERE c_id = '03' AND score > 80;



-- 37、求每门课程的学生人数
SELECT c_id, COUNT(s_id) AS '选课人数'
FROM score
GROUP BY c_id;




-- 38、成绩不重复，查询选修“张三”老师所授课程的学生中成绩最高的学生姓名及其成绩
SELECT st.`s_id` AS '学号' , st.`s_name` AS '姓名' ,MAX(sc.`score`) AS '成绩' 
FROM student st
INNER JOIN score sc ON st.`s_id`= sc.`s_id`
WHERE sc.`c_id` IN (SELECT c_id
               FROM course
               WHERE t_id IN (SELECT t_id
                              FROM teacher
                              WHERE t_name = '张三'
                              ));



-- 39、成绩有重复的情况下，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩
SELECT * FROM
    (SELECT *, DENSE_RANK() over(ORDER BY score DESC) A
    FROM score
    WHERE c_id = (SELECT c_id FROM Course WHERE t_id = (SELECT t_id FROM Teacher WHERE t_name='张三'))
) B
WHERE B.A=1;





-- 40、查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩
SELECT a.`s_id`,a.`c_id`,b.`c_id`,a.`score`,b.`score`
FROM score a, score b
WHERE a.`s_id`= b.`s_id` AND a.`score`= b.`score` AND a.`c_id`<> b.`c_id`;


-- 41、查询每门功课成绩最好的前两名
(select * from score where c_id = '01' order by score desc limit 2)
union 
(select * from score where c_id = '02' order by score DESC limit 2)
union
(select * from score where c_id = '03' order by score DESC limit 2);




-- 42、统计每门课程的学生选修人数（超过5人的课程才统计）。
-- 要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
SELECT c_id,COUNT(s_id) AS '选修人数'
FROM score
GROUP BY c_id
HAVING COUNT(s_id) >= 5
ORDER BY COUNT(s_id) DESC, c_id;




-- 43、检索至少选修两门课程的学生学号
SELECT s_id, COUNT(c_id) AS '选修课程数'
FROM score 
GROUP BY s_id
HAVING COUNT(c_id) >= 2;

-- 44、查询选修了全部课程的学生信息
SELECT * 
FROM student 
WHERE s_id IN (
  SELECT s_id
  FROM score
  GROUP BY s_id
  HAVING COUNT(c_id) = (SELECT COUNT(DISTINCT c_id) FROM course));




-- 45、查询各学生的年龄
SELECT s_id,
       s_name,
       (YEAR(NOW()) - YEAR(s_age)) AS '年龄'
FROM student;


-- 46、按照出生日期来算，当前月日 < 出生年月的月日,则年龄减一
SELECT s_id,
       s_name,
       TIMESTAMPDIFF(YEAR,s_age,NOW()) AS '年龄'
FROM student;


-- 47、查询本周过生日的学生
SELECT *
FROM student
WHERE WEEK(s_age) = WEEK(NOW());

-- 以周一为一周的开始
SELECT *
FROM student
WHERE WEEK(s_age) = WEEK(NOW(),1);




-- 48、查询下周过生日的学生
SELECT *
FROM student
WHERE WEEK(s_age) = WEEK(NOW())+1;

-- 以周一为一周的开始
SELECT *
FROM student
WHERE WEEK(s_age) = WEEK(NOW(),1)+1;






-- 49、查询本月过生日的学生
SELECT *
FROM student
WHERE MONTH(s_age) = MONTH(NOW());



--  50、查询下个月过生日的学生
SELECT *
FROM Student
WHERE MONTH(s_age) = MONTH(NOW())+1;




