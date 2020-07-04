from exts import db
from models import Tousu


def put2base(complaint_info,session3):
    if complaint_info['country'] == '未知':
        lsit1 = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
        conlist = filter(lambda x: x in complaint_info['content'], lsit1)
        cn_list = list(conlist)
        if cn_list:
            complaint_info['country'] = cn_list[0]
        else:
            conlist = filter(lambda x: x in complaint_info['result'], lsit1)
            cn_list = list(conlist)
            if cn_list:
                complaint_info['country'] = cn_list[0]
            else:
                complaint_info['country'] = '未知'
    else:        
        complaint_info['country'] =complaint_info['country']
    if complaint_info['town'] == '':
        if complaint_info['country'] == '未知':
            complaint_info['town'] = '未知'
        else:
            a = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/del_bts2database/dict乡镇.txt', 'r')
                a = f.read()
                dict_torw = eval(a)
                f.close()
                tmplist = filter(lambda x: x in complaint_info['content'], dict_torw[complaint_info['country']])
                newlist = list(tmplist)
                if newlist:
                    complaint_info['town'] = newlist[0]
                else:
                    complaint_info['town'] = '未知'
    if complaint_info['lon'] == '':
        complaint_info['lon'] = ''
        complaint_info['latc'] = ''
    else:
        complaint_info['latc'] = complaint_info['lon'].split(',')[1]
        complaint_info['lon'] = complaint_info['lon'].split(',')[0].replace('g', '')
    if complaint_info['bts_id'] == '':
        complaint_info['bts_id'] = ''
        complaint_info['bts_name'] = ''
    else:
        complaint_info['bts_name'] = '_'.join(complaint_info['bts_id'].split('_')[1:])
        complaint_info['bts_id'] = complaint_info['bts_id'].split('_')[0]

    user1 = Tousu(工单流水号=complaint_info['serial_number'],
                  区域=complaint_info['area'],
                  投诉内容=complaint_info['content'],
                  处理结果=complaint_info['result'],
                  区县=complaint_info['country'],
                  乡镇=complaint_info['town'],
                  我方办结原因=complaint_info['res'],
                  经度=complaint_info['lon'],
                  纬度=complaint_info['latc'],
                  关联基站代码=complaint_info['bts_id'],
                  关联基站名称=complaint_info['bts_name'],
                  关联自然村_小区名=complaint_info['village'],
                  区域细类=complaint_info['area_fenlei'],
                  解决措施=complaint_info['measure'])
    session3.add(user1)
    session3.commit()
    session3.close()

def updata2base(complaint_info,session3):
    dict_pd = {}
    if complaint_info['country'] == '未知':
        lsit1 = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
        conlist = filter(lambda x: x in complaint_info['content'], lsit1)
        cn_list = list(conlist)
        if cn_list:
            dict_pd['区县'] = cn_list[0]
        else:
            conlist = filter(lambda x: x in complaint_info['result'], lsit1)
            cn_list = list(conlist)
            if cn_list:
                dict_pd['区县'] = cn_list[0]

    else:
        dict_pd['区县'] = complaint_info['country']
    if complaint_info['town'] == '':
        if dict_pd:
            a = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/del_bts2database/dict_town.txt', 'r')
                a = f.read()
                dict_torw = eval(a)
                f.close()
                tmplist = filter(lambda x: x in complaint_info['content'], dict_torw[dict_pd["区县"]])
                newlist = list(tmplist)
                if newlist:
                    dict_pd['乡镇'] = newlist[0]
                else:
                    dict_pd['乡镇'] = '未知'
    else:
        dict_pd['乡镇'] = complaint_info['town']
    if complaint_info['res'] != '未知':
        dict_pd['我方办结原因'] =complaint_info['res']
    if complaint_info['area'] != '未知':
        dict_pd['区域'] = complaint_info['area']
    if complaint_info['area_fenlei'] != '未知':
        dict_pd['区域细类'] = complaint_info['area_fenlei']
    if complaint_info['measure'] != '未知':
        dict_pd['解决措施'] = complaint_info['measure']
    if complaint_info['lon'] != '':
        dict_pd['经度'] = complaint_info['lon'].split(',')[0].replace('g', '')
        dict_pd['纬度'] = complaint_info['lon'].split(',')[1]
    if complaint_info['bts_id'] != '':
        dict_pd['关联基站代码'] = complaint_info['bts_id'].split('_')[0]
        dict_pd['关联基站名称'] = '_'.join(complaint_info['bts_id'].split('_')[1:])
    if complaint_info['village'] != '':
        dict_pd['关联自然村_小区名'] = complaint_info['village']
    dict_pd['处理结果']=complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update tousu set {k}="{v}"where 工单流水号="{id}"'.format(k=k, v=v, id=complaint_info['serial_number']))
        session3.commit()
        session3.close()