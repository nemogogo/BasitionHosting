#__author:zhang_lei
#date:2018/3/26

import json
from audit import models
import subprocess
from django import conf


class MultiTaskManager(object):
    def __init__(self, request):
        self.request = request
        self.task_run()
    def task_parser(self):
        """任务解析"""
        print(self.request.POST.get('task_data'))
        self.task_data = json.loads(self.request.POST.get('task_data'))

        task_type = self.task_data.get('task_type')
        if hasattr(self,task_type):
            task_func = getattr(self,task_type)
            task_func()
        else:
            print("cannot find task ",task_type)


    def task_run(self):
        """调用任务"""
        self.task_parser()

    def cmd(self):
        """
        批量命令
        1、生成任务在数据库中的记录，得到任务ID
        2、触发任务，不阻塞
        3、返回任务id给前段
        :return:
        """
        task_obj=models.Task.objects.create(
            task_type='cmd',
            content=self.task_data.get('cmd'),
            user=self.request.user
        )
        task_obj.save()
        selected_host_ids=set(self.task_data['selected_hosts'])
        task_log_objs=[]
        for id in selected_host_ids:
            task_log_objs.append(
                models.TaskLogDetail(task=task_obj,bind_host_id=id,result='init...')
            )
        models.TaskLogDetail.objects.bulk_create(task_log_objs)

        try:
            task_cmd ='python3 {base_dir}/backend/task_runner.py  {id}' .format (base_dir=conf.settings.BASE_DIR, id=task_obj.id)

            cmd_process = subprocess.Popen(task_cmd, shell=True)
            print(cmd_process)

            print('Running batch commands...')
        except Exception as e:
            task_obj.result = e
            task_obj.status = 2


        print('2323')
        self.task_obj = task_obj


    def file_transfer(self):
        """文件分发"""
        task_obj = models.Task.objects.create(
            task_type = 'file_transfer',
            content = json.dumps(self.task_data),
            user = self.request.user
        )
        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs =[]
        for id in selected_host_ids:
            task_log_objs.append(
                models.TaskLogDetail(task=task_obj,bind_host_id=id,result='init...')
            )
        models.TaskLogDetail.objects.bulk_create(task_log_objs)

        task_script = "python3 %s/backend/task_runner.py %s" % (conf.settings.BASE_DIR, task_obj.id)

        cmd_process = subprocess.Popen(task_script, shell=True)
        print("running batch file transfer ....")

        self.task_obj = task_obj

































