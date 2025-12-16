
import os
import pytest
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")
django.setup()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass