# -*- coding: utf-8 -*-
from utils import auto_insert_sql ,get_db_conn,get_yesterday


class A(object):
    def __init__(self):
        self.c1 = 0
        self.c2 = 0
        self.c3 = 3


def main():
    # a = A()
    result_list =[]
    a = {'a': 1, 'b': 2}
    yesterday = '20190417';
    dw_cur = get_db_conn().cursor();
    sql='select * from etl_ctrl_show where sp_eod_dt = %s '%(yesterday);
    dw_cur.execute(sql)
    column = [val[0].lower() for val in  dw_cur.description]
    print column ,type(column)
    rows = dw_cur.fetchall()
    for row in rows :
        print row ;
        result_dic =dict(zip(column,row));
        print result_dic
        result_list.append(result_dic)
        #print result_list;



if __name__ == '__main__':
    main()