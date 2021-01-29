# 复杂sql编写

Complex SELECT Query

需要进一步写demo C++需要不断练习

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
https://www.datacamp.com/community/tutorials/sql-tutorial-query#importance
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
时间线后面的时间比时间线前面的时间大

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
item index collection open separator close



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
https://blog.csdn.net/weixin_37519581/article/details/103838842

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


<if test="operaType != null and operaType[0] != 0">
    and opera_type IN (
    <foreach collection="operaType" separator="," item="item" index="idx">
        #{item}
    </foreach>
    )


<update id="updateSchoolName">
	update ems_dog_permission perm,
	(
		<foreach collection="list" item="item" separator=" union all ">
			select #{item.id} id,#{item.schoolName} school_name
		</foreach>
	) tmp
	set perm.school_name = tmp.school_name
	where perm.id = tmp.id
</update>




mybatis之foreach用法  注意index
在做mybatis的mapper.xml文件的时候，我们时常用到这样的情况：动态生成sql语句的查询条件，这个时候我们就可以用mybatis的foreach了
foreach元素的属性主要有item，index，collection，open，separator，close。
item：集合中元素迭代时的别名，该参数为必选。
index：在list和数组中,index是元素的序号，在map中，index是元素的key，该参数可选
open：foreach代码的开始符号，一般是(和close=")"合用。常用在in(),values()时。该参数可选
separator：元素之间的分隔符，例如在in()的时候，separator=","会自动在元素中间用“,“隔开，避免手动输入逗号导致sql错误，如in(1,2,)这样。该参数可选。
close: foreach代码的关闭符号，一般是)和open="("合用。常用在in(),values()时。该参数可选。
collection: 要做foreach的对象，作为入参时，List对象默认用"list"代替作为键，数组对象有"array"代替作为键，Map对象没有默认的键。当然在作为入参时可以使用@Param("keyName")来设置键，设置keyName后，list,array将会失效。 除了入参这种情况外，还有一种作为参数对象的某个字段的时候。举个例子：如果User有属性List ids。入参是User对象，那么这个collection = "ids".如果User有属性Ids ids;其中Ids是个对象，Ids有个属性List id;入参是User对象，那么collection = "ids.id"


https://www.cnblogs.com/fnlingnzb-learner/p/10566452.html
https://blog.csdn.net/zbajie001/article/details/107332618


<trim prefix="(" suffix=")" suffixOverrides=",">
</trim>
<trim prefix="values (" suffix=")" suffixOverrides=",">
</trim>


select ${@com.iflytek.jkpt.ems.common.constants.Constants$PlanType@UNITE_PLAN} AS planType,

		AND townplan.plan_state ${@com.iflytek.jkpt.ems.common.util.state.PlanStateUtil@getUniteState(status)}
连等于号都不用写


	<select id="listPlanSchoolCountExamed" resultType="com.iflytek.jkpt.ems.api.model.common.PlanDetailDTO">
		<bind name="plan_field_id" value="@com.iflytek.jkpt.ems.core.util.plan.PlanFieldUtil@getTableFieldId(planType)"/>
		select 
			mockplan.${plan_field_id} planId,
			mockplan.plan_type planType,
			count(1) schoolCountExamed
		from ems_mock_plan mockplan
		where 1=1
		and mockplan.${plan_field_id} 
			in (<foreach collection="planIds" item="item" separator=",">#{item}</foreach>)
		and mockplan.complete_stu_count > 0
		group by mockplan.${plan_field_id}
	</select>

sql 列名是mybatis的入参



GROUP_CONCAT(distinct taskclass.class_id) classIds,
count(distinct taskclass.class_id) classCountExamed
出现的次数


对虚表的操作
update虚表
select出来的表



where task_id in
select出来的
select出来的是不是单个列


select出来的有时可以当作集合，有时可以当作表


<if test="!(userId!=null)">


listTestTaskState  if() sum()

mybatis
xml

一个<delete 节点
多个delete语句



<if test="classIds != null and classIds.size() > 0">
	taskclass.class_id in (
	<foreach collection="classIds" item="item" separator=",">#{item,jdbcType=VARCHAR}</foreach>)
</if>


queryClientTask


<if test="startTime != null and startTime != '' and endTime != null and endTime != ''">
	AND task.start_time BETWEEN str_to_date(concat(#{startTime}, ' 00:00:00'), '%Y-%m-%d %H:%i:%s') AND str_to_date(concat(#{endTime}, ' 23:59:59'), '%Y-%m-%d %H:%i:%s')
</if>


AND task.task_state NOT IN (0, 38, 98, 102, 103)


统计列是枚举值的事情
sum(if(task_state in (5,6,7), 1, 0)) taskEvalNum




<update id="updateTownPlanStuCountByTaskId">
	update ems_town_plan townplan,
	(select * from  (
		select plan_town_id,sum(complete_stu_count) ccount, sum(total_stu_count) tcount from ems_mock_plan
		where plan_town_id in (
			select plan_town_id from ems_test_task where id in (<foreach collection="taskIds" item="item" separator=",">#{item}</foreach>)
		)
		and plan_state != 100 and plan_town_id != ''
		GROUP BY plan_town_id
	) tmp2 ) tmp
	<if test="totalCount">
		set townplan.total_stu_count = tmp.tcount
	</if>
	<if test="!totalCount">
		set townplan.complete_stu_count = tmp.ccount
	</if>
	where tmp.plan_town_id = townplan.id
</update>



delete from ems_test_task_paper


select  COUNT(DISTINCT e.examineeCode) gatherAmount


select 列名那边 子查询


select DISTINCT area from sys_plan where area is NOT NULL and LENGTH(area) != 0

select count(*) total,sum(case when sp.planState=11 then 1 else 0 end) completed from sys_plan sp


select 7 num;
+-----+
| num |
+-----+
|   7 |
+-----+



单个sql，还是多个sql
<!--批量更新record成绩-->
<update id="updateRecord" parameterType="java.util.List">
    <foreach collection="list" item="item" index="index" open="" close="" separator=";">
        update log_hum_record
        <set>
            score = #{item.score},detail=#{item.detail},
            markStatus=#{item.markStatus},commiteTime=#{item.commiteTime},userAccount=#{item.userAccount}
        </set>
        where id = #{item.id}
    </foreach>
</update>




log_hum_examinee,log_hum_task
WHERE log_hum_examinee.taskUid = log_hum_task.uid




COUNT(DISTINCT e.examineeCode) gatherAmount


ROUND(A.分差,2) evaScoreGap,

A是表别名 分差是select查询出来虚表的列

join 默认是哪个join


where planState not in (0, 1, 2, 11);

<!--批量更新record成绩-->
<update id="updateRecord" parameterType="java.util.List">
    <foreach collection="list" item="item" index="index" open="" close="" separator=";">
        update log_hum_record
        <set>
            score = #{item.score},detail=#{item.detail},
            markStatus=#{item.markStatus},commiteTime=#{item.commiteTime},userAccount=#{item.userAccount}
        </set>
        where id = #{item.id}
    </foreach>
</update>

批量插入
批量更新



<update id="batchUpdate" parameterType="java.util.List">
	update log_hum_examinee
	<trim prefix="set" suffixOverrides=",">
		detail =
		<foreach collection="list" item="item" open="case " close=" end,">
			when examineeCode = #{item.examineeCode}
			AND paperCode = #{item.paperCode}
			AND sectionCode = #{item.senctionName}
			AND examineeType in (0,1)
			then #{item.detail}
		</foreach>
		score =
		<foreach collection="list" item="item" open="case " close=" end,">
			when examineeCode = #{item.examineeCode}
			AND paperCode = #{item.paperCode}
			AND sectionCode = #{item.senctionName}
			AND examineeType in (0,1)
			then #{item.score}
		</foreach>
	</trim>
</update>




<!-- 评分质量监控 -->
<select id="getMarkQualityMonitor" resultType="com.iflytek.webService.entitys.LogHumTaskQualityMonitorBean">
    SELECT
        r.sectionCode sectionCode,
        t.description sectionName,
        u.userType userType,
        u.taskType taskType,
        u.userAccount userAccount,
        COUNT(DISTINCT r.id) haveEvalAmount,
        t.fullScore fullScore,
        AVG(r.score) avgEvalScore,
        MAX(r.score) maxEvalScore,
        MIN(r.score) minEvalScore
    FROM
        log_hum_record r
    LEFT JOIN log_user u ON r.userAccount = u.userAccount
    LEFT JOIN log_hum_task t ON r.sectionCode = t.sectionCode
    WHERE
        r.jkptPlanId = #{planId}
    AND r.markStatus = 2
    <choose>
        <when test="roleType != -1 and roleType != null">
            <choose>
                <when test="roleType == 2">
                    AND u.userType = 3
                </when>
                <otherwise>
                    AND u.userType = 2
                    <!-- 数据库中 0 定标+验证，  1异常集-->
                    AND u.taskType = #{roleType}
                </otherwise>
            </choose>
        </when>
        <otherwise>
            AND (u.userType = 2 OR u.userType = 3)
        </otherwise>
    </choose>
    <if test="sectionCode != null">
        AND r.sectionCode = #{sectionCode}
    </if>
    GROUP BY
    r.sectionCode, u.userAccount
</select>



and data_time = (SELECT MAX(data_time) FROM large_screen_school_exam_statistics)


order by (interaction_user_count+classwork_user_count) desc




SELECT FROM manager_app_detail_${tableSuffix}


ExamTaskStatMapper.xml



	<select id="listTableColumn" resultType="com.iflytek.jkpt.manager.core.model.dto.bigdata.ColumnMetaData">
    	desc ${tableName}
    </select>

	<insert id="loadTableData">
    	load data local infile '${localFilePath}' into table ${tableName} fields
        	terminated by '${terminated}' (${fields})
    </insert>


insert into 没有values
直接是select的值


where and条件

<foreach collection="param.operaTypes" item="item" separator=" or ">
	(opera_type &amp; #{item}) > 0
</foreach>




<update id="updateSchoolName">
	update manager_product_school mps,
	(
	<foreach collection="schools" item="item" separator=" union all ">
		select #{item.id} id,#{item.schoolName} school_name
	</foreach>
	) tmp
	set mps.school_name = tmp.school_name
	where mps.id = tmp.id
</update>



<if test="!single">

<if test="single">


WHERE 1 = 1
and (school.school_id,school.phase_code) in
	(<foreach collection="schoolList" item="item" separator=",">
(#{item.schoolId},#{item.phaseCode})</foreach>)



and data_time = #{dataTime}
group by province_code
order by sum(mock_count+task_count) desc, province_code



provinceName
from  manager_tss_pandect_${tableSuffix}
where province_code != 'all'


order by sum(selftraining_count) desc,province_code,school_id



<!--资源储量统计-试题总数-->
<select id="getItemTotal" parameterType="com.iflytek.jkpt.manager.model.v2.resource.common.ResourceParamDTO"
        resultType="com.iflytek.jkpt.manager.model.v2.resource.item.ReservesItemPandectDTO">
    SELECT
    SUM(CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN item_count END) totalPhaseItem,
    SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1201' THEN item_count END) totalItemMaterial,
    SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1203' THEN item_count END) totalItemSubject,
    SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1202' THEN item_count END) totalItemSpecial,
    SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '2601' THEN item_count END) totalItemBreach,
    SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1204' THEN item_count END) totalItemFun
    FROM
        manager_reserves_item_pandect t
    WHERE
       t.phase_code = #{phaseCode}
       AND t.grade_code = #{gradeCode}
       AND item_type = 'all'
</select>

<!--试题使用与授权统计-试题总数-->
<select id="getItemAuthAndUseTotal"
        parameterType="com.iflytek.jkpt.manager.model.v2.resource.common.ResourceParamDTO"
        resultType="com.iflytek.jkpt.manager.model.v2.resource.item.ItemGrantUsePandectDTO">
     SELECT SUM( CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN area_grant END ) totalAreaGrant,
        SUM( CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN not_area_grant END ) totalNotAreaGrant,
        SUM(CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN item_count_use END) totalUse,
        SUM(CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN item_count_grant END) totalGrant,
        SUM(CASE WHEN item_classify_code = 'all' AND item_type_code = 'all' THEN item_count_not_grant END) totalNotGrant,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1201' THEN item_count_use END) totalMaterialUse,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1201' THEN item_count_grant END) totalMaterialGrant,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1203' THEN item_count_use END) totalSubjectUse,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1203' THEN item_count_grant END) totalSubjectGrant,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1202' THEN item_count_use END) totalSpecialUse,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1202' THEN item_count_grant END) totalSpecialGrant,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '2601' THEN item_count_use END) totalBreachUse,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '2601' THEN item_count_grant END) totalBreachGrant,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1204' THEN item_count_use END) totalFunUse,
        SUM(CASE WHEN item_classify_code = '0' AND item_type_code = '1204' THEN item_count_grant END) totalFunGrant
        FROM manager_item_grant_use_pandect t
    WHERE resource_phase_code = #{resourcePhaseCode}
    AND t.province_code = #{provinceCode}
    AND t.city_code = #{cityCode}
    AND t.district_code = #{districtCode}
    AND item_type = 'all'
</select>





<delete id="deleteCodeSerial" parameterType="com.iflytek.jkpt.product.api.model.dto.ActivationCodeSerialDTO">
		delete from p_activationcode_serial where 1=1
		and (data_id,data_type) in (
		<foreach collection="list" item="item" separator=",">
			(#{item.dataId}, #{item.dataType})
		</foreach>
	)
</delete>



<update id="updateById">
	update p_activationcode_serial
	<trim prefix="set" suffixOverrides=",">
		<if test="flowCode!=null">code=#{flowCode,jdbcType=VARCHAR},</if>
		<if test="dataNewId!=null">data_id=#{dataNewId,jdbcType=VARCHAR},</if>
	</trim>
	 where data_id = #{dataId} and data_type = 4;
</update>




select
<include refid="Base_Column_List"/>
from sps_practice_task
<where>
    <if test="userId != null">
        user_id = #{userId,jdbcType=BIGINT}
    </if>
<where
子节点


<select id="listClassworkList" resultType="com.iflytek.jkpt.tss.api.model.task.TssClassWork4TeacherDTO">
    select id taskId,date_format(end_datetime,'%Y-%m-%d %T') endDateTime,state taskState
    from tss_classwork
    where id in
    <foreach item="item" index="index" collection="classworkIds" open="(" separator="," close=")">
        #{item}
    </foreach>
</select>

date_format str
unix stamp三个函数


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




<select id="getNoSyncTaskCount" resultType="int">
    select count(1)
    from tss_interactive_task where state = 2
    <if test="syncDatetime != null">
        and create_datetime <![CDATA[>=]]> #{syncDatetime}
    </if>
</select>



<where>
    <if test="taskIds != null and taskIds.size() != 0">
        id in
        <foreach collection="taskIds" item="taskId" separator=","  open="(" close=")">
            #{taskId}
        </foreach>
    </if>
</where>



<select id="getClassTaskClasses" resultType="com.iflytek.jkpt.tascollect.model.dto.ems.TaskClassDto">
    SELECT DISTINCT p.id as task_id, class_id, c.class_type as class_type
    from ems_test_task p
                 LEFT JOIN ems_test_task_class c on p.id = c.task_id
            where c.class_id is not null
    <if test="taskIds != null and taskIds.size() != 0">
        and p.id in
        <foreach collection="taskIds" item="item" open="(" close=")" separator=",">
            #{item}
        </foreach>
    </if>
</select>


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

update
trim
trim
foreach
if



FROM tss_interactive_task tit
    left join tss_interactive_task_item ti on tit.id=ti.interactivetask_id


FROM tss_interactive_task task
    LEFT JOIN tss_interactive_task_item item ON task.id = item.interactivetask_id


from tss_interactive_task tit
                  left join tss_teaching_class ttc on ttc.class_id = tit.class_id


from res_auth_item ait
    INNER JOIN res_auth_item_detail aid on aid.auth_item_id=ait.id
    INNER JOIN res_item_attr ita on ita.id=aid.item_attr_id
    INNER JOIN res_item it on it.id=ita.item_id
    left  join res_template_design_item tdi on tdi.code=it.template_code
    left join res_answer_item_record_statistics air on air.item_id=it.id
    LEFT JOIN res_usage_record_statistics  ugs on it.id=ugs.res_id and ugs.creator_id=#{userId}


from res_auth_item ait
    INNER JOIN res_auth_item_detail aid on aid.auth_item_id=ait.id
    INNER JOIN res_item_attr ita on ita.id=aid.item_attr_id
    INNER JOIN res_item it on it.id=ita.item_id
    LEFT JOIN res_sequence seq ON seq.res_code = it.`code`



from res_item_attr ita
INNER JOIN res_item it on it.id=ita.item_id
left join res_answer_item_record_statistics air on air.item_id=it.id
LEFT JOIN res_usage_record_statistics  ugs on it.id=ugs.res_id and ugs.creator_id=#{userId}


FROM res_item it
INNER JOIN res_item_attr ita ON ita.item_id = it.id
left JOIN res_attr_val rav ON it.item_type_code = rav.code
left    JOIN res_attr_val_grade ravg ON ravg.code = ita.grade_code

        


from  res_item it
        INNER JOIN  res_item_attr ita on it.id=ita.item_id


FROM res_item it
        INNER JOIN res_item_attr ita ON it.id=ita.item_id

FROM res_auth_item ait
        INNER JOIN res_auth_item_detail aid ON ait.id = aid.auth_item_id
        INNER JOIN res_item_attr ita ON aid.item_attr_id =ita.id
        INNER JOIN res_item it ON ita.item_id = it.id


from res_item ri
    LEFT JOIN
    res_sync_item_info rsi on rsi.item_id=ri.id
    LEFT JOIN
    res_template_design_item rtdi on rtdi.`code`=ri.template_code


多个条件join
left JOIN res_labelled_engine a ON a.code = b.labelled_engine_code and a.delete_flag=0


FROM res_checked_packet_basic rcpb
    LEFT JOIN res_checked_packet_paper_detail rcppd ON rcpb.id = rcppd.packet_id
    LEFT JOIN res_paper_attr rpa ON rcppd.paper_id = rpa.paper_id



FROM res_checked_packet_basic rcpb
    LEFT JOIN
    res_checked_packet_paper_detail rcppd
    ON
    rcpb.id = rcppd.packet_id


FROM res_checked_packet_basic rcpb
    LEFT JOIN res_checked_packet_item_detail rcpid
    ON rcpb.id = rcpid.packet_id


FROM res_template_dynamic_paper rtp
    LEFT JOIN res_checked_packet_paper_detail rcp ON rtp.paper_id = rcp.paper_id


FROM res_checked_packet_paper_detail rcpapd
    INNER JOIN res_paper p ON rcpapd.paper_id = p.id
    INNER JOIN res_paper_attr pa ON p.id = pa.paper_id
    INNER JOIN res_template_design_paper tdp on p.template_code=tdp.`code`


LEFT JOIN
    res_checked_packet_item_detail rcpid ON
    rcpb.id = rcpid.packet_id

FROM res_book book
    RIGHT JOIN res_auth_book authbook ON book.id = authbook.book_id


FROM res_auth_item ait
        INNER JOIN res_auth_item_detail aid ON aid.auth_item_id=ait.id
        INNER JOIN res_item_attr ita ON ita.id=aid.item_attr_id
        INNER JOIN res_item it ON it.id=ita.item_id
        where ita.delete_flag=#{deleteFlag}

FROM res_auth_item  ait
        INNER JOIN res_auth_item_detail  aid ON aid.auth_item_id=ait.id
        INNER JOIN res_item_attr ita ON  ita.id=aid.item_attr_id
        INNER JOIN res_item  it ON it.id=ita.item_id


from res_auth_item ai
    INNER JOIN res_auth_item_detail aid ON ai.id = aid.auth_item_id
    INNER JOIN res_item_attr ita ON ita.id=aid.item_attr_id
    INNER JOIN res_item it ON it.id = ita.item_id

group by 临时表
        GROUP BY
        aa.use_code



from res_auth_paper ait
    INNER JOIN res_auth_paper_detail aid ON ait.id=aid.auth_paper_id



from res_auth_paper ait
    INNER JOIN res_auth_paper_detail aid ON ait.id=aid.auth_paper_id
    INNER JOIN res_paper rp ON aid.paper_id=rp.id
    INNER JOIN res_paper_attr rpa ON aid.paper_id=rpa.paper_id




FROM res_auth_paper_detail a
    INNER JOIN res_paper it ON a.paper_id = it.id
    INNER JOIN res_paper_attr ita ON it.id = ita.paper_id


Mybatios引用java代码中的函数，变量

from res_auth_paper  a
    left JOIN  res_auth_paper_detail b on b.auth_paper_id=a.id




FROM res_auth_paper rap
    INNER JOIN res_auth_paper_detail rapd ON rap.id = rapd.auth_paper_id
    INNER JOIN res_paper rp ON rapd.paper_id=rp.id
    INNER JOIN res_paper_attr rpa ON rapd.paper_id=rpa.paper_id



FROM res_item_attr ita
    INNER JOIN res_item it ON it.id=ita.item_id
    INNER JOIN res_auth_item rai ON rai.id



from res_auth_item_detail a
    INNER JOIN res_auth_item b on a.auth_item_id=b.id
    INNER  JOIN res_item_attr ita on ita.id=a.item_attr_id
    INNER  JOIN res_item it on it.id=ita.item_id
    left join res_template_design_item rtdi on it.template_code = rtdi.code




<!--更新授权组记录与授权表记录(试题)-->
<update id="updateAuthItemByGroupId" parameterType="com.iflytek.jkpt.res.core.model.po.mysql.auth.AuthItemParam">
    update res_auth_item rai,res_auth_group rag
    <set>
        <if test="authState != null and authState !=''">
            rai.state = #{authState},rai.update_time=now(),rag.state=#{authState},
        </if>
        <if test="authSource != null and authSource !=''">
            rai.source = #{authSource},
        </if>
        <if test="authGroupName != null and authGroupName !=''">
            rag.name = #{authGroupName},
        </if>
    </set>
    where rai.auth_group_id=rag.id and rag.id=#{authGroupId}
</update>



from res_auth_group rag
    left join res_auth_item rai on rag.id=rai.auth_group_id
    left join res_auth_item_detail raid on raid.auth_item_id = rai.id and raid.delete_flag=0

from res_auth_group rag
    INNER join res_auth_item rai on rag.id=rai.auth_group_id
    INNER join res_auth_item_detail raid on raid.auth_item_id = rai.id
    INNER join res_item_attr ita on ita.id=raid.item_attr_id





DELETE a,b FROM
res_auth_item a
LEFT JOIN res_auth_item_detail b ON a.id=b.auth_item_id
where a.auth_group_id in
<foreach collection="authGroupIds" index="index" item="authGroupId" separator="," open="(" close=")">
    #{authGroupId}
</foreach>;



FROM res_auth_notice ran
        INNER JOIN res_auth_item rai ON ran.auth_group_id = rai.auth_group_id
        INNER JOIN res_auth_group rag ON rag.id = ran.auth_group_id

from res_attr_type rat
    INNER JOIN res_auth_attr att
    on rat.`code`=att.unactive_attr_code

from res_attr_type a LEFT JOIN res_attr_type b
    on a.code=b.parent_code

max(if(productauth.id is null, 0, 1)) orderFlag


FROM tss_classwork a
    LEFT JOIN tss_classwork_class b ON a.id = b.classwork_id


from tss_classwork_class tcc
    left join tss_classwork tc on tc.id=tcc.classwork_id

from ems_unite_plan p
     LEFT JOIN ems_test_task t on p.id = t.plan_id
     LEFT JOIN ems_test_task_class c on t.id = c.task_id


from ems_mock_plan p
     LEFT JOIN ems_test_task t on p.id = t.plan_id
     LEFT JOIN ems_test_task_class c on t.id = c.task_id



from ems_city_plan p
    LEFT JOIN ems_test_task t on p.id=t.plan_id
    LEFT JOIN ems_test_task_class c on t.id=c.task_id



from ems_city_plan p
    LEFT JOIN ems_test_task t on p.id=t.plan_id
    LEFT JOIN ems_test_task_class c on t.id=c.task_id


from sps_practice_task_su   bmit ts
    inner join sps_practice_task t on ts.task_id = t.id



FROM p_product pp
    INNER JOIN p_product_kq_extend pe on pp.id=pe.product_id
    INNER JOIN p_product_detail pd on pp.id=pd.product_id


FROM p_product pp
    INNER JOIN p_product_kq_extend pe on pp.id=pe.product_id
    INNER JOIN p_product_detail pd on pp.id=pd.product_id


from p_activationcode pa
    INNER JOIN p_grant_record pgr ON
    pa.grant_id = pgr.id



FROM p_grant_record p
    INNER JOIN p_product pp ON p.product_code = pp.product_code
    INNER JOIN p_product_detail ppd ON pp.id = ppd.product_id


from p_activationcode pa
    INNER JOIN p_grant_record pgr on pa.grant_id = pgr.id
    INNER join p_product pp on pp.product_code  = pgr.product_code
    left join  (select  count(1)num ,grant_id  from p_activationcode where p_activationcode.activation_state = '1201' GROUP BY grant_id  )a on a.grant_id = pa.grant_id
    left join (select count(1)num ,grant_id from p_activationcode where p_activationcode.activation_state = '1202' GROUP BY grant_id  )b on b.grant_id = pa.grant_id

from p_activationcode pa
    LEFT JOIN p_grant_record pgr on pa.grant_id = pgr.id
    INNER join p_product pp on pp.product_code  = pgr.product_code


from p_activationcode pa
    LEFT JOIN p_grant_record pgr on pa.grant_id = pgr.id
    INNER join p_product pp on pp.product_code  = pgr.product_code
