import logging
import time

from .yunxiao import YunXiao, UsedTime
import requests


class V2(YunXiao):
    def __init__(self, configfile: str = "yunxiao_config.ini", campus: tuple = ()):
        """
        初始化，输入用户账号密码，以及要操作的校区。
        :param campus: 校区
        :param configfile: 配置文件路径
        """
        super().__init__(configfile)
        self.campus = list(campus)

    def request(self, **kwargs) -> dict:
        response = requests.request(
            method=kwargs.get("method"),
            url=kwargs.get("url"),
            json=kwargs.get("json"),
            params=kwargs.get("params"),
            headers={"x3-authentication": self.token, "Cookie": self.cookie}
        )

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        if response.json()["code"] == 401:
            logging.error(response.json()["msg"])
            self.renew_cookie()
            self.renew_token()
            response = requests.request(
                method=kwargs.get("method"),
                url=kwargs.get("url"),
                json=kwargs.get("json"),
                params=kwargs.get("params"),
                headers={
                    "x3-authentication": self.token,
                    "Cookie": self.cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
                    "Origin": "https://yunxiao.xiaogj.com",
                    "Referer": "https://yunxiao.xiaogj.com/app/teacher/"
                }
            )

        return response.json()

    # 循环装饰器
    @staticmethod
    def loop(KEY):
        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                result = []
                count = 1
                page = kwargs.get("page")
                size = kwargs.get("size")
                while (now := len(result)) != count:
                    page += 1
                    kwargs["page"] = page
                    res = func(*args, **kwargs)
                    data = res["data"][KEY] if KEY else res["data"]
                    result.extend(data)
                    count = res["page"]["totalCount"]
                    print(f"size: {size}, page: {page}, {now}/{count}")
                    size = size if (count - len(result)) > size else (count - len(result))
                    kwargs["size"] = size
                print(f"size: {size}, page: {page}, {now}/{count}")
                return result

            return wrapper

        return wrapper_func

    # 查询机构指定月份的每日业绩
    def company_query_performance_month(self, yy_mm: str = UsedTime.yymm) -> list:
        """
        查询指定月份的每日费用数据
        :param yy_mm: 查询月份，默认为本月。**2023-02**
        :return:
        """
        course = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findCourseMoney",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        refund = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findRefundMoney",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        tuition = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findTuition",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        return list(map(lambda x: {**x[0], **x[1], **x[2]}, zip(course, refund, tuition)))

    # 查询机构指定日期范围业绩。
    def company_query_performance_daterange(self, startdate: str = UsedTime.yymm01,
                                            enddate: str = UsedTime.today) -> list:
        """
        查询机构指定日期范围业绩。
        :param startdate: 起始日期
        :param enddate: 截止日期
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate,
                "orderByCampus": 1,
                "_t_": UsedTime.stamp
            }
        )["data"]

    # 查询校区
    def campus_query(self) -> list:
        """
        查询全部校区
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-crm/campus/list?type=2"
        )["data"]

    # 查询指定日期业绩
    def campus_query_performance_date(self, date: str = UsedTime.today) -> list:
        """
        分校区列出指定日期的费用数据。
        :param date: 日期
        :return:
        """
        data_list = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": date,
                "endDate": date,
                "orderByCampus": 1,
                "_t_": UsedTime.stamp
            }
        )["data"]["dataReportVos"]
        return list(map(lambda item: {**item, "id": f"{date}-{item['campusId']}"}, data_list))

    # 查询指定日期范围业绩。
    def campus_query_performance_daterange(self, startdate: str = UsedTime.yymm01,
                                           enddate: str = UsedTime.today) -> list:
        """
        查询指定日期范围业绩。
        :param startdate: 起始日期
        :param enddate: 截止日期
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate,
                "orderByCampus": 1,
                "_t_": UsedTime.stamp
            }
        )["data"]["dataReportVos"]

    # 查询老师
    def teachers_query(self, name: str = "", status: tuple = (1,), size: int = 200) -> list:
        """
        查询老师。
        :param size: 查询数量，最大 200
        :param status: 老师状态。 **1** 在职 **0** 离职
        :param name: 查询教师的姓名
        :return: [{}...]
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "queryKey": name,
                "statusList": list(status),
                "page": {"pageNum": 1, "pageSize": size}
            }
        )["data"]

    # 查询老师排课
    def teacher_query_arrange(self, teacher_id: int, start_date: str = UsedTime.weekstrat,
                              end_date: str = UsedTime.weekend):
        """
        取得指定老师的课表。
        :param teacher_id: 查询的老师ID
        :param start_date: 起始日期，默认为本周一
        :param end_date: 结束日期，默认为本周日
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/arrange/page",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "startDate": start_date,
                "endDate": end_date,
                "teacherIds": [teacher_id],
                "reserve": 0,
                "displayCompletedClass": False,
                "courseStatusList": [],
                "page": {"pageNum": 1, "pageSize": 999}
            }
        )["data"]

    # 查询意向
    @loop("")
    def intentions_query(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                         nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                         startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码，应设为 0
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/intention/clue/allPage",
            json={
                "_t_": UsedTime.stamp,
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询意向学员
    @loop("")
    def intentions_query_students(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                                  nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                                  startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向学员
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码，应设为 0
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:https://yunxiao.xiaogj.com/app/teacher/#/cluedetails?id=7127357
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/student/listForIntentionManage",
            json={
                "_t_": UsedTime.stamp,
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询学生
    @loop("")
    def students_query(self, page, size, curriculumids: tuple = (), classids: tuple = (), name: str = "",
                       status: tuple = (1, 7), class_student_status: int = 0):
        """
        查询学生
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码，应设为 0
        :param curriculumids: 课程筛选
        :param classids: 班级筛选
        :param name: 姓名查询关键字
        :param status: 学员状态。 **0** 未收费 **1** 在读 **6** 曾就读 **7** 停课 **99** 无效学员
        :param class_student_status: **0** 不筛选 **1** 未入班 **2** 已入班
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/student/list",
            json={
                "_t_": UsedTime.stamp,
                "name": name,
                "campusIds": self.campus,
                "status": list(status),
                "curriculumIds": list(curriculumids),
                "classIds": list(classids),
                "classStudentStatus": class_student_status,
                "orgTag": 1,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 学生数据费用报表。
    @loop("cardCourseTradedList")
    def students_query_course_fee(self, page: int, size: int, displayHistory: bool = True,
                                  status: tuple = (1, 7), studentName: str = ""):
        """
        学生数据费用报表。
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param displayHistory: 是否显示曾就读学生
        :param status: 学生状态列表 **0** 未收费 **1** 在读 **7** 停课
        :param studentName: 学员姓名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findStudentCourseFee",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "displayHistory": displayHistory,
                "status": list(status),
                "studentName": studentName
            }
        )

    # 学生数据的课次报表。
    @loop("studentCourseAmountList")
    def students_query_course_amount(self, page: int, size: int, displayHistory: bool = True,
                                     status: tuple = (1, 7), studentName: str = ""):
        """
        学生数据的课次报表。
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param displayHistory: 是否显示曾就读学生
        :param status: 学生状态列表 **0** 未收费 **1** 在读 **7** 停课
        :param studentName: 学员姓名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findStudentCourseAmount",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "displayHistory": displayHistory,
                "status": list(status),
                "studentName": studentName
            }
        )

    # 查询学生课程卡
    @loop("")
    def students_query_cards(self, page: int, size: int, display_history: bool = True,
                             remain_amount_min: str = "", remain_amount_max: str = ""):
        """
        列出所有课程卡
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param display_history: 是否显示曾就读学生
        :param remain_amount_max: 限制查询剩余次数-最大
        :param remain_amount_min: 限制查询剩余次数-最小
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/studentCourseCard/report",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "displayHistory": display_history,
                "remainAmountMin": remain_amount_min,
                "remainAmountMax": remain_amount_max
            }
        )

    # 查询学生基本信息
    def student_query_info(self, studentid: int, companyid: int = None):
        """
        查询学生基本信息
        :param companyid: 机构ID
        :param studentid: 学员ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-crm/student/getContainFace",
            params={
                "_t_": UsedTime.stamp,
                "id": studentid,
                "companyId": companyid
            }
        )["data"]

    # 查询学生课程卡包
    def student_query_cards(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/cardInfo/findStudentCard",
            json={
                "_t_": UsedTime.stamp,
                "studentId": studentid,
                "page": {
                    "pageNum": 1,
                    "pageSize": 100
                }
            }
        )["data"]["cardCourseTradedList"]

    # 查询学生就读课程
    def student_query_course(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/courseStudent/findStudentAttendCourse",
            json={
                "_t_": UsedTime.stamp,
                "studentId": studentid,
                "page": {
                    "pageNum": 1,
                    "pageSize": 100
                }
            }
        )["data"]["studentAttendCourseList"]

    # 查询学生的出入班记录
    def student_query_class_records(self, studentid: int, curriculum_id: int):
        """
        [工作台][学员][就读课程][出入班记录]
        :param studentid: 学生ID
        :param curriculum_id: 课程ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/student/findOperationRecordList",
            json={
                "_t_": UsedTime.stamp,
                "studentId": str(studentid),
                "curriculumId": curriculum_id
            }
        )["data"]

    # 设置学生为停课。
    def student_operation_suspend(self, student_id: str, suspend_course_date: str = UsedTime.today,
                                  remove_class: int = True):
        """
        设置学生为停课。
        :param student_id: 学生ID
        :param suspend_course_date: 停课时间。0000-00-00
        :param remove_class: 是否从班级中移除
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/student/studentSuspendCourse",
            json={
                "_t_": UsedTime.stamp,
                "recoveryCourseDate": "",
                "extendDays": "",
                "removeClass": remove_class,
                "studentId": student_id,
                "suspendCourseDate": suspend_course_date,
                "type": 0
            }
        )

    # 设置学生为曾就读。
    def student_operation_history(self, studentlist: tuple):
        """
        设置学生为曾就读。
        :param studentlist: 学生ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/student/becomeHistory",
            json={
                "_t_": UsedTime.stamp,
                "studentIds": list(studentlist)
            }
        )

    # 查询课程
    @loop("")
    def curriculums_query(self, page, size, searchname: str = None, haltsalelist: tuple = ()):
        """
        查询课程
        :param page:
        :param size:
        :param searchname: 查找课程名
        :param haltsalelist: 是否在售。 **0** 在售 **1** 停售
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/curriculum/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "curriculumName": searchname,
                "haltSaleList": haltsalelist,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询某日排课
    def arranges_query_date(self, date: str = UsedTime.today, teacherids: tuple = ()) -> list:
        """
        列出日期范围全部排课[最大9999条]
        :param teacherids: 老师ID
        :param date: 查询日期 **2020-02-20**
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/getCompanyCourse",
            json={
                "_t_": UsedTime.stamp,
                "date": date,
                "campusIds": self.campus,
                "teacherIds": list(teacherids)
            }
        )["data"][0]["courseArrangeRecordVos"]

    # 查询某日到某日排课
    @loop("")
    def arranges_query_daterange(self, page, size, starttime: str = None, endtime: str = None, teacherids: tuple = (),
                                 studentids: tuple = (), displayCompletedClass: bool = False, before_today: int = 30,
                                 after_today: int = 30, courseStatusList: tuple = (0, 1)):
        """
        查询某日到某日的排课。
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param studentids: 查询的学生列表
        :param teacherids: 查询的教师列表
        :param displayCompletedClass: 是否已结班排课
        :param courseStatusList: 排课状态。 **0** 未点名 **1** 已点名 **2** 已取消
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :param starttime: 查询起始时间 **2020-02-20**
        :param endtime: 查询截止时间 **2020-03-20**
        :return:
        """
        starttime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if starttime is None else starttime

        endtime = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if endtime is None else endtime

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/page",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "startDate": starttime,
                "endDate": endtime,
                "courseStatusList": list(courseStatusList),
                "teacherId": list(teacherids),
                "studentIds": list(studentids),
                "displayCompletedClass": displayCompletedClass,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询班级
    @loop("")
    def classes_query(self, page, size, teacherids: tuple = (), classname: str = "", classStatus: int = 0):
        """
        查询班级
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param classname: 班级名称
        :param classStatus: 班级状态。 **0** 未结班 **1** 已结班
        :param teacherids: 老师ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/classInfo/page",
            json={
                "_t_": UsedTime.stamp,
                "orgTag": 1,
                "classStatus": classStatus,
                "campusIds": self.campus,
                "classname": classname,
                "teacherIds": list(teacherids),
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询班级信息
    def class_query_info(self, classid: int = None) -> dict:
        """
        查询指定班级信息
        :param classid: 班级id
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-edu/classInfo/getClassInfoVo",
            params={
                "_t_": UsedTime.stamp,
                "classId": classid
            }
        )["data"]

    # 查询班级排课
    def class_query_arrange(self, classid: int) -> dict:
        """
        查询班级排课
        :param classid: 班级ID
        :return: courseArrangeExtendVoList, noRollCallArrange, startCourseDate,
        stopCourseDate, surplusArrange, totalArrange
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/list",
            json={
                "_t_": UsedTime.stamp,
                "classId": classid,
                "isDesc": False,
                "status": None
            }
        )["data"]

    # 查询班级学生
    def class_query_student(self, classid: int, inout: int = 1) -> list:
        """
        查询班级学生
        :param inout: **[1]** 当前在班学员 **[2]** 历史学员
        :param classid: 班级ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-edu/classStudent/findClassStudent",
            params={
                "_t_": UsedTime.stamp,
                "classId": classid,
                "inout": inout
            }
        )["data"]

    # 列出指定上课日期范围的所有课消记录
    @loop("courseConsumeList")
    def charges_query_record(self, page, size, startdate: str = None, enddate: str = None,
                             before_today: int = 30, after_today: int = 30):
        """
        列出指定上课日期范围的所有课消记录
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param startdate: YY-MM-DD
        :param enddate: YY-MM-DD
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :return:
        """

        startdate = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if startdate is None else startdate

        enddate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if enddate is None else enddate

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findCourseSignCharge",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "courseStartTime": startdate,
                "courseEndTime": enddate
            }
        )

    # 列出指定上课日期范围的所有课消详情
    @loop("courseConsumeDetailList")
    def charges_query_detail(self, page, size, startdate: str = None, enddate: str = None,
                             before_today: int = 30, after_today: int = 30):
        """
        列出指定上课日期范围的所有课消详情
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param startdate: YY-MM-DD
        :param enddate: YY-MM-DD
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :return:
        """

        startdate = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if startdate is None else startdate

        enddate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if enddate is None else enddate

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findCourseSignChargeDetail",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "assistantTeacherIds": [],
                "campusIds": [],
                "courseEndTime": enddate,
                "courseStartTime": startdate,
                "curriculumIds": [],
                "studentIds": [],
                "teacherIds": []
            }
        )

    # 查询指定操作日期范围的所有收入/转课订单组
    @loop("")
    def orders_query(self, page, size, startdate: str = "", enddate: str = "", ordertype: int = 0,
                     searchname: str = "", orderstatuslist: tuple = ()):
        """
        查询指定操作日期范围的所有收入/转课订单组
        :param orderstatuslist: 订单状态。 **[0]** 未收费 **[1]** 已付款 **[2]** 已取消 **[3]** 已失效 **[4]** 已作废
        :param searchname: 搜索学员姓名
        :param ordertype: 订单类型 **[0]** 收费 **[1]** 转课
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/orderInfo/pageAdbOrder",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate,
                "searchName": searchname,
                "orderStatusList": list(orderstatuslist),
                "orderType": ordertype
            }
        )

    # 查询指定操作日期范围的所有收入/转课订单子项
    @loop("orderItemAllList")
    def order_query_info(self, orderinfoid: int):
        """
        查询指定操作日期范围的所有订单子项
        :param orderinfoid: 订单详情ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/orderInfo/get",
            params={
                "_t_": UsedTime.stamp,
                "orderInfoId": orderinfoid,
            }
        )

    # 查询指定操作日期范围的所有收入/转课订单子项
    @loop("orderItemAllList")
    def orders_query_items(self, page, size, startdate: str = "", enddate: str = ""):
        """
        查询指定操作日期范围的所有订单子项
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findOrderItemAll/page",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate
            }
        )

    # 查询指定操作日期范围的所有退费订单组
    @loop("")
    def orders_query_refund(self, page, size, startdate: str = "", enddate: str = ""):
        """
        列出指定操作日期范围的所有订单记录
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/orderRefund/adbRefundOrderInfoPage",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "orderType": 2,
                "startTime": startdate,
                "endTime": enddate
            }
        )

    # 查询指定操作日期范围的所有退费
    def payments_query_refund(self, startdate: str = "", enddate: str = "") -> list:
        """
        查询指定操作日期范围的所有退费
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentRefundList",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "refundFinishStartTime": startdate,
                "refundFinishEndTime": enddate
            }
        )["data"]

    # 查询指定操作日期范围的所有收入
    @loop("paymentDetailDtos")
    def payments_query(self, page, size, startdate: str = "", enddate: str = ""):
        """
        查询指定操作日期范围的所有收入
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentList",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "payStartTime": startdate,
                "payEndTime": enddate
            }
        )

    # 取得收据信息
    def payments_query_receipt(self, order_id: int, payment_group_id: int) -> dict:
        """
        取得收据信息。
        :param order_id: 订单 ID
        :param payment_group_id: 支付 ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/public/receipt/findReceipt",
            params={
                "orderInfoId": order_id,
                "paymentGroupId": payment_group_id,
                "_t_": UsedTime.stamp
            }
        )["data"]

    # 列出指定操作日期范围的所有账户收支记录
    def payments_query_record(self, startdate: str = None, enddate: str = None,
                              before_today: int = 30, after_today: int = 30) -> list:
        """
        列出指定操作日期范围的所有订单记录
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :return:
        """

        startdate = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if startdate is None else startdate

        enddate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if enddate is None else enddate

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentAccountCustomRecord",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate,
                "displayInvalidOrder": True
            }
        )["data"]

    # 查询业绩归属
    @loop("achievementBelongerDetailItems")
    def payments_query_achievements_datarange(self, page, size, startdate: str = None, enddate: str = None,
                                              before_today: int = 30, after_today: int = 30):
        """
        查询业绩归属，根据日期
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :return:
        """

        startdate = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if startdate is None else startdate

        enddate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if enddate is None else enddate

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findAchievementBelongerDetail",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate
            }
        )

    # 查询业绩归属
    def payments_query_achievements(self, startdate: str = None, enddate: str = None, productName: str = "",
                                    teacherIds: tuple = (), before_today: int = 30, after_today: int = 30):
        """
        查询业绩归属，根据信息
        :param teacherIds: 老师ID
        :param productName: 项目名称
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :param before_today: 设定起始日期为今天之前的某天，当 starttime 留空时使用。
        :param after_today: 设定起始日期为今天之后的某天，当 endtime 留空时使用。
        :return:
        """

        startdate = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)) \
            if startdate is None else startdate

        enddate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * after_today)) \
            if enddate is None else enddate

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findAchievementBelongerDetail",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate,
                "productName": productName,
                "teacherIds": list(teacherIds),
                "orderTypes": [0]
            }
        )["data"]

    # 查询招生来源
    def comefroms_query(self):
        return self.request(
            method="get",
            url=f"https://yunxiao.xiaogj.com/api/cs-crm/customField/get",
            params={"_t_": UsedTime.stamp, "customFieldId": "26118419"}
        )["data"]["selectItemList"]
