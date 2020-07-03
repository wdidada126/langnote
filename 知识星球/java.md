# java



以battmd的高级工程师为主



芋艿



​	

邀请用户

a->b b->c

如何统计a邀请（包括直接邀请和间接邀请）了哪些新用户

关系数据库

all_parent_id(用间隔符号拼接)  name id

null                                                a         1

1                                                     b          2

1，2                                               c         3



`select count（all_parent_id）from table where all_parent_id like a；`





还有一种用图数据库





