# leetcode_cn_sql

https://leetcode.cn/studyplan/sql-free-50/

## (LeetCode596:数据库) 超过5名学生的课
HAVING里面条件，HAVING里面条件跟where区别，HAVING是跟GROUP BY

https://www.jianshu.com/p/d7b1796ea811

SELECT
    class
FROM
    courses
GROUP BY
    class
HAVING
    count(DISTINCT student) >= 5;
