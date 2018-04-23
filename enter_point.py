#__author:zhang_lei
#date:2018/3/24

import os
if __name__=="__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BasitionHosting.settings")
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
    from django.conf import settings
    print(settings.SESSION_TRACKER_SCRIPT)
    from audit import models
    from backend import userprotal
    portal=userprotal.UserPortal()
    portal.interactive()
