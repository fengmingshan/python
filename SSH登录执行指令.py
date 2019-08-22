# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:49:39 2019

@author: Administrator
"""

import paramiko

def ssh_session(ip,username,passwd,cmd):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22,username,passwd,timeout=5)
    for m in cmd:
      stdin, stdout, stderr = ssh.exec_command(m)
#      stdin.write("Y")  #简单交互，输入 ‘Y'
      out = stdout.readlines()
      #屏幕输出
      for o in out:
        print o,
    print '%s\tOK\n'%(ip)
    ssh.close()
  except :
    print '%s\tError\n'%(ip)


import pexpect

def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret