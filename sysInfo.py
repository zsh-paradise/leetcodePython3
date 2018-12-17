import  logging
import sys
from utils import query_for_list
class sysInfoFactory(object):
    def __init__(self, orc_cur):
        self.__data = {}
        self.__data["dependecy_dict"] = self.__dependecy(orc_cur = orc_cur)


    def __dependecy(self,orc_cur):
        sSql = " select b.task_code as secondname,c.task_code as firstname  from etl_task_rel  a " \
           "left join etl_task_base_info b on a.TASK_ID = b.task_id " \
           "left join etl_task_base_info c on a.task_super_id = c.task_id"
        return query_for_list(orc_cur,sSql)

