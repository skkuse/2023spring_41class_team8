import os
from django.conf import settings

# DJANGO_SETTINGS_MODULE 환경 변수 설정 확인
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    raise ValueError("DJANGO_SETTINGS_MODULE environment variable is not set.")

# settings 모듈이 올바르게 로드되었는지 확인
if not settings.configured:
    raise ValueError("Django settings are not configured.")

# INSTALLED_APPS 설정 확인
if "sogong" not in settings.INSTALLED_APPS:
    raise ValueError("your_app_name is not included in INSTALLED_APPS.")
