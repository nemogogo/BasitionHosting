#__author:zhang_lei
#date:2018/3/26
import os,sys
import paramiko
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from django import conf

def ssh_cmd(sub_task_obj):

    print("start thread ----",sub_task_obj)
    bind_host= sub_task_obj.bind_host

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=bind_host.host.ip_addr,
                    port=bind_host.host.port,
                    username=bind_host.host_user.username,
                    password=bind_host.host_user.password,
                    timeout=5)
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.content)
        stdout= stdout.read()
        stderr= stderr.read()

        # task_log_obj = models.TaskLogDetail.objects.get(task=task_obj,bind_host_id=bind_host.id)
        sub_task_obj.result =stdout + stderr
        print("------------result-------------")
        print(sub_task_obj.result)

        if stderr:
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 1
    except Exception as e:
        sub_task_obj.result = e
        sub_task_obj.status = 2

    sub_task_obj.save()

    print(type(sub_task_obj))
    ssh.close()

def file_transfer(sub_task_obj, task_data):
    host_to_user_obj = sub_task_obj.bind_host

    try:
        t = paramiko.Transport((host_to_user_obj.host.ip_addr, host_to_user_obj.host.port))
        t.connect(username=host_to_user_obj.remote_user.username,
                  password=host_to_user_obj.remote_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_data['file_transfer_type'] == 'send':
            sftp.put( task_data["local_file_path"],  task_data["remote_file_path"] )

            result = "file [%s] sends to [%s] succeed!" %(task_data["local_file_path"],task_data["remote_file_path"] )

        else:
            local_file_path = conf.settings.DOWNLOAD_DIR
            if not  os.path.isdir("%s%s"%(local_file_path,task_obj.id)):
                os.mkdir("%s%s"%(local_file_path,task_obj.id))

            filename ="%s.%s" %( sub_task_obj.host_to_remote_user.host.ip_addr,task_data["remote_file_path"].split('/')[-1])
            sftp.get(task_data["remote_file_path"], "%s%s/%s"% (local_file_path,sub_task_obj.task.id, filename))
            result = "download remote file [%s] succeed!"  % task_data["remote_file_path"]
        t.close()

        sub_task_obj.status = 1
    except Exception as e :
        print("-->e",e)
        result = e
        sub_task_obj.status = 2

    sub_task_obj.result = result

    sub_task_obj.save()

if __name__=="__main__":
    BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    import django
    django.setup()
    from audit import models
    from django.conf import settings
    import paramiko
    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj=models.Task.objects.get(id=task_id)
    pool = ThreadPoolExecutor(10)
    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.tasklogdetail_set.all():
           pool.submit(ssh_cmd,sub_task_obj)
    else: #文件传输
        task_data = json.loads(task_obj.content)
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer,sub_task_obj,task_data )
        file_transfer(task_obj.tasklogdetail_set.last(), task_data)
    pool.shutdown(wait=True)
