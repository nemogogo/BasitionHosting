#__author:zhang_lei

from django import conf

def kingadmin_auto_discover():
    '''
    检查在kingadmin里注册了的table
    :return:
    '''
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod=__import__('%s.autoadmin.kingadmin'%app_name)

        except ImportError as e:

            pass
kingadmin_auto_discover()