ho_reason = session_handover.execute(
    "SELECT `邻区`, `切换出请求总次数`,`切换出成功次数`, `切换出失败次数`, `切换出执行失败次数_源侧发生重建立`, `切换出执行失败次数_等待UECONTEXTRELEASE消息超时`, `切换出执行失败次数_其它原因`, `切换出准备失败次数_等待切换响应定时器超时`, `切换出准备失败次数_目标侧准备失败`, `切换出准备失败次数_其它原因`, `切换出准备失败次数_源侧发生重建立`, `切换出准备失败次数_用户未激活`, `切换出准备失败次数_传输资源受限`,`切换入成功次数`, `切换入失败次数`, `切换入执行失败次数_RRC重配完成超时`, `切换入执行失败次数_源侧取消切换`, `切换入执行失败次数_目标侧发生重建立`, `切换入执行失败次数_其他原因`, `切换入准备失败次数_资源分配失败`, `切换入准备失败次数_源侧取消切换`, `切换入准备失败次数_目标侧发生重建立`, `切换入准备失败次数_传输资源受限`, `切换入准备失败次数_其它原因` FROM `邻区切换` WHERE eNodeB = {enb} and `小区` = {cell} and week(`开始时间`)= {week}  and (`切换出请求总次数`>30 OR `切换入请求总次数`>30 OR `切换出成功次数`>30 OR `切换入成功次数`>30)  order by 切换出请求总次数 limit 40".format(
        enb=enb, cell=cell, week=cur_week))
ho_reason = list(ho_reason)
ho_reason_ne = [x.邻区 for x in ho_reason]
ho_sec_out = [x.切换出成功次数 for x in ho_reason]
ho_fail_out = [x.切换出失败次数 for x in ho_reason]
ho_re_fail_1 = [x.切换出准备失败次数_等待切换响应定时器超时 for x in ho_reason]
ho_re_fail_2 = [x.切换出准备失败次数_目标侧准备失败 for x in ho_reason]
ho_re_fail_3 = [x.切换出准备失败次数_其它原因 for x in ho_reason]
ho_re_fail_4 = [x.切换出准备失败次数_源侧发生重建立 for x in ho_reason]
ho_re_fail_5 = [x.切换出准备失败次数_用户未激活 for x in ho_reason]
ho_re_fail_6 = [x.切换出准备失败次数_传输资源受限 for x in ho_reason]
ho_do_fail_1 = [x[4] for x in ho_reason]
ho_do_fail_2 = [x[5] for x in ho_reason]
ho_do_fail_3 = [x[6] for x in ho_reason]
ho_sec_in = [x[13] for x in ho_reason]
ho_fail_in = [x[14] for x in ho_reason]
ho_do_in_1 = [x[15] for x in ho_reason]
ho_do_in_2 = [x[16] for x in ho_reason]
ho_do_in_3 = [x[17] for x in ho_reason]
ho_do_in_4 = [x[18] for x in ho_reason]
ho_re_in_1 = [x[19] for x in ho_reason]
ho_re_in_2 = [x[20] for x in ho_reason]
ho_re_in_3 = [x[21] for x in ho_reason]
ho_re_in_4 = [x[22] for x in ho_reason]
ho_re_in_5 = [x[23] for x in ho_reason]
ho_reason_secc_chart = draw_bar_stack(ho_reason_ne, '切换出成功次数', ho_sec_out, '切换出失败次数', ho_fail_out, '切换分析')
HO_count_chart = draw_bar_stack_6(['' for x in range(len(ho_reason_ne))], '等待切换响应定时器超时', ho_re_fail_1, '目标侧准备失败',
                                  ho_re_fail_2, '传输资源受限', ho_re_fail_6, '源侧发生重建立', ho_re_fail_4, '用户未激活',
                                  ho_re_fail_5, '其它原因', ho_re_fail_3, '切换出准备失败', )
ho_do_fail_chart = draw_bar_stack_3(['' for x in range(len(ho_reason_ne))], '源侧发生重建立', ho_do_fail_1,
                                    'UECONTEXTRELEASE超时', ho_do_fail_2, '其它原因', ho_do_fail_3, '切换出执行失败')
ho_reason_in_chart = draw_bar_stack(ho_reason_ne, '切换入成功次数', ho_sec_in, '切换入失败次数', ho_fail_in, '切换分析')
HO_do_in_chart = draw_bar_stack_4(['' for x in range(len(ho_reason_ne))], 'RRC重配完成超时', ho_do_in_1, '源侧取消切换',
                                  ho_do_in_2, '目标侧发生重建立', ho_do_in_3, '其他原因', ho_do_in_4, '切换入执行失败', )
HO_re_in_chart = draw_bar_stack_5(['' for x in range(len(ho_reason_ne))], '资源分配失败', ho_re_in_1, '源侧取消切换',
                                  ho_re_in_2, '目标侧发生重建立', ho_re_in_3, '传输资源受限', ho_re_in_4, '其它原因',
                                  ho_re_in_5, '切换入准备失败', )
ho_distance = session_handover.execute(
    "SELECT a.`邻区`, b.distance from (SELECT `邻区`,`邻区关系`,`切换出请求总次数` FROM `邻区切换` WHERE eNodeB = {enb} and 小区 = {cell} and (`切换出请求总次数`>30 OR `切换入请求总次数`>30 OR `切换出成功次数`>30 OR `切换入成功次数`>30) limit 40 ) as a left JOIN  (SELECT relation,distance from `邻区距离`) as b ON a.`邻区关系`=b.relation order by a.`切换出请求总次数`".format(
        enb=enb, cell=cell))
ho_distance = list(ho_distance)
distance_ce = [x.邻区 for x in ho_distance]
df_distance = [x.distance for x in ho_distance]
HO_distance_chart = draw_bar_reversal(distance_ce, df_distance, '邻区站点距离', ' ', )
HO_distan_chart = draw_bar_reversal(['' for x in range(len(distance_ce))], df_distance, '邻区站点距离', ' ', )
