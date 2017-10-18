# coding:utf-8
import Deadline.DeadlineConnect as connect
import os
import getpass


# 使用远程pulse服务必须保证aux file能被pulse服务器访问到
# 注意筛选机子

def deadline_node():
    # obj = connect.DeadlineCon('PC00052', 8080)
    obj = connect.DeadlineCon('deadline', 8080)
    return obj


def submit_testjob():
    scriptfile = r'Z:\Resource\Share\z张旭强\script\printpath.py'
    jobInfor = {
        'Name': 'testjob',

        'UserName': '%(UserName)s' % {
            'UserName': getpass.getuser()
        },
        'Frames': '1',
        'MachineLimit': '1',
        'Plugin': 'Python',

        # 'SynchronizeAllAuxiliaryFiles': True
        # 这句话就会复制aux文件到slave 本地
    }
    pluginInfor = {
        "ScriptFile": os.path.normpath(scriptfile),
        'Arguments': '',

        "Version": "2.7"
    }

    jobfile = r'D:\testjob.job'
    pluginfile = r'd:\testjobplugin.job'
    # job = deadline_node().Jobs.SubmitJobFiles(jobfile,pluginfile,
    #                                           scriptfile
    #                                      )
    job = deadline_node().Jobs.SubmitJob(jobInfor, pluginInfor,
                                         # scriptfile
                                         )

    # 使用aux 会拷贝aux文件到slave机器的deadline用户目录下,所以尽量不要使用aux文件,防止容量问题,当然也可以achive job
    return job
