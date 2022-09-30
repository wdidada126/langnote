# sqlldr

D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\BIN\sqlldr.exe


sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_login.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad


sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_course.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad

sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_student.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad

sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_sc.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad



sqlldr icrm/icrm@18.20.20.20:1521/crmdb 
data = '/home/lee/dapai.dat'  #数据文件目录
bad = /home/lee/adpai.bad   #错误数据存放
control = /home/lee/adpai.ctl # 控制文件
direct = y  #这块需要特别注意，根据实际业务场景使用，不要随便使用
log = /home/lee/adpai.log    #日志文件
errors = 100000
