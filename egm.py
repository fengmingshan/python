# 本代码的目的是通过python实现德军二战时期的密码机：恩格玛
import re
import string
 
 
def simple_replace(password, replace_word1, replace_word2, replace_word3):  # 加密的主函数
    count = 0  # 设置计数器
    new_pass = ''  # 设置一个空字符串准备接收密码
    ori_table = 'abcdefghijklmnopqrstuvwxyz'  # 原始的字符串，用来建立映射表
    for obj in password:  # 开始拆解原字符串
        table1 = str.maketrans(ori_table, replace_word1)  # 建立转子1的映射表
        table2 = str.maketrans(ori_table, replace_word2)  # 建立转子2的映射表
        table3 = str.maketrans(ori_table, replace_word3)  # 建立转子3的映射表
        new_obj = str.translate(obj, table1)  # 把obj通过转子1转换
        new_obj = str.translate(new_obj, table2)  # obj通过转子2
        new_obj = str.translate(new_obj, table3)  # obj通过转子3
        new_obj = reverse_word(new_obj)  # 进入自反器，得到自反值
        reverse_table1 = str.maketrans(replace_word1, ori_table)  # 增加自反出去的对应表，反向解译
        reverse_table2 = str.maketrans(replace_word2, ori_table)
        reverse_table3 = str.maketrans(replace_word3, ori_table)
        new_obj = str.translate(new_obj, reverse_table3)  # new_obj再赋值，反向解译通过转子3
        new_obj = str.translate(new_obj, reverse_table2)  # 通过转子2
        new_obj = str.translate(new_obj, reverse_table1)  # 通过转子1
        new_pass += new_obj  # 返回的密码增加一个new_obj
        replace_word1 = rotors(replace_word1)  # 转子1每个字符都转动一次
        count += 1  # 计数器增加1
        if count % 676 == 0:   # 如果模676为0，那么转子3转动一次(因为转子2已经转动了一整圈）
            replace_word3 = rotors(replace_word3)
        elif count % 26 == 0:  # 如果模26为0，那么转子2转动一次（因为转子1已经转动了一整圈）
            replace_word2 = rotors(replace_word2)
    return new_pass  # 返回新的已经被转子加密的密码
 
# 单独把判断写成一个函数吧，这样比较好区分
 
 
def is_str(password, replace_word1, replace_word2, replace_word3):  # 判断的函数
    an = re.match('[a-z]+$', password)  # 当时的enigma机是没有空格的，所以这里要求输入的明文也必须是小写字母
    if not type(password) == type(replace_word1) == type(replace_word2) == type(replace_word3) == type('a'):
        print('密码必须是字符串！')
        return False
    elif not an:
        print('字符串只能包含小写字母！')
        return False
    elif not len(replace_word1) == len(replace_word2) == len(replace_word3) == 26:
        print('替换码必须为26个字母！')
        return False
    else:
        return True  # 修正了函数的写法，增加了一个返回true的选项
 
 
def rotors(replace_word):  # 转子转动的函数，每调用一次，就把转子前面第一个字母移动到最后
    return replace_word[1:] + replace_word[0]
 
# 还没有自反器呢！加密之后无法解密，是何其的蛋疼！
# 自反器很好设置的，只要设置一个字典，保证所有字母（26个）两两对应就可以了，怎么对应，你说了算！
 
 
def reverse_word(word):
    dic = {'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q',
           'e': 'r', 'f': 's', 'g': 't', 'h': 'u',
           'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y',
           'm': 'z', 'n': 'a', 'o': 'b', 'p': 'c',
           'q': 'd', 'r': 'e', 's': 'f', 't': 'g',
           'u': 'h', 'v': 'i', 'w': 'j', 'x': 'k',
           'y': 'l', 'z': 'm'}
    return dic[word]
 
while True:
    a_password = input('请输入明文加密或密文解密:')
    r_password1 = 'qwertyuiopasdfghjklzxcvbnm'  # 转子1，自己设置即可
    r_password2 = 'asdfqwerzxcvtyuiopghjklbnm'  # 转子2，自己设置即可
    r_password3 = 'poiuytrewqasdfghjklmnbvcxz'  # 转子3，自己设置即可
    if is_str(a_password, r_password1, r_password2, r_password3):
        print('密文/明文如下：', simple_replace(a_password, r_password1, r_password2, r_password3))