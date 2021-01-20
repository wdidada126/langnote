# 复杂sql编写

Complex SELECT Query

https://zhuanlan.zhihu.com/p/195501421

https://cloud.tencent.com/developer/article/1033405

https://blog.csdn.net/ostrichmyself/article/details/42581227


https://blog.csdn.net/culuo4781/article/details/107624314

https://www.sqlshack.com/learn-sql-how-to-write-a-complex-select-query/
https://www.sqlshack.com/sql-server-training/


https://blog.csdn.net/culuo4781/article/details/107624314


以前做过旅游业ERP的开发，看别人写的t-sql功能很强大，且简洁，但是非常难看懂，我想问问怎么才能学会很复杂sql的编写，捞取数据，处理复杂的逻辑

https://www.cnblogs.com/Hackerman/p/10934413.html
https://segmentfault.com/a/1190000011112396

http://blog.sina.com.cn/s/blog_13b7ba9b00102xl9h.html


<if test="type == 1">
    AND s.sampleType = '好'
</if>
<if test="type == 2">
    AND s.sampleType = '中'
</if>
<if test="type == 3">
    AND s.sampleType = '差'
</if>


sort_value字段
auth_role.sort_value

sql date timestamp 大小写比较 


 SELECT paper_id paperId,sum( useTimes ) useTimes,sum( scoreRate ) scoreRate
 FROM
    (
    SELECT paper_id,sum(num) useTimes,0 scoreRate FROM res_answer_paper_record WHERE num != 0 GROUP BY paper_id
    UNION
    SELECT paper_id,0 useTimes,round(sum( score_rate ) / count( 1 ),5 ) scoreRate FROM res_answer_paper_record WHERE num = 0 GROUP by paper_id
 ) a
 GROUP BY
 paper_id;


concat("%",#{pattern},"%")
vs
concat('%',#{pattern},'%')

foreach
item index collection
open separator close


set case when
```
    <!--更新任务的schoolId-->
    <update id="UpdateListTaskSchoolId" parameterType="list">
        update tss_classwork
        <trim prefix="set" suffixOverrides=",">
            <trim prefix="school_id =case" suffix="end,">
                <foreach collection="list" item="i" index="index">
                    <if test="i.schoolId!=null">
                        when id=#{i.id} then #{i.schoolId}
                    </if>
                </foreach>
            </trim>
        </trim>
        where
        <foreach collection="list" separator="or" item="i" index="index">
            id=#{i.id}
        </foreach>
    </update>
```


ifnull()
MySQL中IF()、IFNULL()、NULLIF()、ISNULL()函数的使用

GROUP BY task.plan_mock_id, taskclass.class_id
多个

	<select id="getMockPlanStuCount" resultType="com.iflytek.jkpt.emscheck.core.model.po.mysql.EmsMockPlan">
		select ctmp.plan_mock_id id,ctmp.ccount completeStuCount, ifnull(ttmp.tcount , 0) totalStuCount from 
		(
			select plan_mock_id,sum(complete_stu_count) ccount from ems_test_task
					where plan_mock_id = #{planMockId}
					and task_state != 100
					GROUP BY plan_mock_id limit 1000000
		) ctmp
		left join (
			select plan_mock_id,sum(tcount) tcount from
			(
				select task.plan_mock_id, taskclass.class_id, max(taskclass.total_stu_count) tcount from ems_test_task task
				inner join ems_test_task_class taskclass on taskclass.task_id = task.id
				where task.plan_mock_id = #{planMockId}
				and task.task_state != 100
				GROUP BY task.plan_mock_id, taskclass.class_id
			) tcounttmp limit 1000000
		) ttmp on ttmp.plan_mock_id = ctmp.plan_mock_id
	</select>

	 <update id="updateTaskClassName">
		update ems_test_task_class taskclass,
		(
			<foreach collection="classList" item="item" separator=" union all ">
				select #{item.classId} class_id,#{item.className} class_name
			</foreach>
		) tmp
		set taskclass.class_name = tmp.class_name
		where taskclass.class_id = tmp.class_id and taskclass.id in (
			<foreach collection="classDbIds" item="item" separator=",">#{item}</foreach>
		)
	</update>



