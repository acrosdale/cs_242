# apply test configuaration to all test in test folder [global]
import os
import django
from django.conf import settings

# since the test exist outside the django domain we must
# add the path to them so they can be found by pytest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.app.project.settings')

# TEST: VIEWS, MODELS, FORMS, SERIALIZERS,API


def pytest_configure():
    settings.DEBUG = False
    # If you have any test specific settings, you can declare them here,
    django.setup()
