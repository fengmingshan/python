from exts import db
from models import Tousu


def put2base(complaint_info,session3):
    if complaint_info['country'] == '0':
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
        dict_ct = {'1': '沾益', '2': '马龙', '3': '陆良', '4': '师宗', '5': '罗平', '6': '宣威', '7': '会泽', '8': '富源', '9': '麒麟'}
        complaint_info['country'] = dict_ct[complaint_info['country']]
    if complaint_info['town'] == '':
        if complaint_info['country'] == '0' or complaint_info['country'] == '未知':
            complaint_info['town'] = '未知'
        else:
            a = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/KPI_report/dict乡镇.txt', 'r')
                a = f.read()
                dict_torw = eval(a)
                f.close()
                tmplist = filter(lambda x: x in complaint_info['content'], dict_torw[complaint_info['country']])
                newlist = list(tmplist)
                if newlist:
                    complaint_info['town'] = newlist[0]
                else:
                    complaint_info['town'] = '未知'
    dict_B = {'0': '未知',
                  '1': '弱覆盖',
                  '2': '无覆盖',
                  '3': '基站故障',
                  '4': '光缆故障',
                  '5': '用户终端故障',
                  '6': '容量问题',
                  '7': '优化问题',
                  '8': '达量限速',
                  '9': '其他'}
    complaint_info['res'] = dict_B[complaint_info['res']]
    dict_quyu = {'0': '未知',
                 '1': '城区',
                 '2': '乡镇',
                 '3': '农村', }
    complaint_info['area'] = dict_quyu[complaint_info['area']]
    dict_quyuxilei = {'0': '未知',
                      '1': '住宅小区',
                      '2': '厂矿企业',
                      '3': '政府机关单位',
                      '4': '商业区',
                      '5': '学校',
                      '6': '医院',
                      '7': '宾馆酒店',
                      '8': '交通枢纽',
                      '9': '娱乐场所',
                      '10': '乡镇',
                      '11': '自然村'}
    complaint_info['area_fenlei'] = dict_quyuxilei[complaint_info['area_fenlei']]
    dict_measure = {'0': '未知',
                      '1': '处理基站故障',
                      '2': '优化调整',
                      '3': '基站扩容',
                      '4': '基站建设',
                      '5': '使用WIFI替代',
                      '6': '用户自行处理',
                      '7': '网络正常无需处理',
                      '8': '非本期间故障无法处理',
                      '9': '开通volte替代'}
    complaint_info['measure']=dict_measure[complaint_info['measure']]
    user1 = Tousu(工单流水号=complaint_info['serial_number'],
                  区域=complaint_info['area'],
                  投诉内容=complaint_info['content'],
                  处理结果=complaint_info['result'],
                  区县=complaint_info['country'],
                  乡镇=complaint_info['town'],
                  我方办结原因=complaint_info['res'],
                  经度=complaint_info['lon'],
                  纬度=complaint_info['lat'],
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
    if complaint_info['country'] == '0':
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
        dict_ct = {'1': '沾益', '2': '马龙', '3': '陆良', '4': '师宗', '5': '罗平', '6': '宣威', '7': '会泽', '8': '富源',
                   '9': '麒麟'}
        complaint_info['country'] = dict_ct.get(complaint_info['country'])
        dict_pd['区县'] = complaint_info['country']
    if complaint_info['town'] == '':
        if dict_pd:
            a = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/KPI_report/dict乡镇.txt', 'r')
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
    if complaint_info['res'] != '0':
        dict_B = {'0': '未知',
                  '1': '弱覆盖',
                  '2': '无覆盖',
                  '3': '基站故障',
                  '4': '光缆故障',
                  '5': '用户终端故障',
                  '6': '容量问题',
                  '7': '优化问题',
                  '8': '达量限速',
                  '9': '其他'}
        dict_pd['我方办结原因'] = dict_B[complaint_info['res']]
    if complaint_info['area'] != '0':
        dict_quyu = {'0': '未知',
                     '1': '城区',
                     '2': '乡镇',
                     '3': '农村', }
        dict_pd['区域'] = dict_quyu[complaint_info['area']]
    if complaint_info['area_fenlei'] != '0':
        dict_quyuxilei = {'0': '未知',
                          '1': '住宅小区',
                          '2': '厂矿企业',
                          '3': '政府机关单位',
                          '4': '商业区',
                          '5': '学校',
                          '6': '医院',
                          '7': '宾馆酒店',
                          '8': '交通枢纽',
                          '9': '娱乐场所',
                          '10': '乡镇',
                          '11': '自然村'}
        dict_pd['区域细类'] = dict_quyuxilei[complaint_info['area_fenlei']]
    if complaint_info['measure'] != '0':
        dict_measure = {'0': '未知',
                        '1': '处理基站故障',
                        '2': '优化调整',
                        '3': '基站扩容',
                        '4': '基站建设',
                        '5': '使用WIFI替代',
                        '6': '用户自行处理',
                        '7': '网络正常无需处理',
                        '8': '非本期间故障无法处理',
                        '9': '开通volte替代'}
        dict_pd['解决措施'] = dict_measure[complaint_info['measure']]
    if complaint_info['lon'] != '':
        dict_pd['经度'] = complaint_info['lon']
    if complaint_info['lat'] != '':
        dict_pd['纬度'] = complaint_info['lat']
    if complaint_info['bts_id'] != '':
        dict_pd['关联基站代码'] = complaint_info['bts_id']
    if complaint_info['bts_name'] != '':
        dict_pd['关联基站名称'] = complaint_info['bts_name']
    if complaint_info['village'] != '':
        dict_pd['关联自然村_小区名'] = complaint_info['village']
    dict_pd['处理结果']=complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update tousu set {k}="{v}"where 工单流水号="{id}"'.format(k=k, v=v, id=complaint_info['serial_number']))
        session3.commit()
        session3.close()