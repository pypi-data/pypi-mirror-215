from typing import List

from django.apps import AppConfig


def get_trigger_audit_models(app_config: AppConfig) -> List[str]:
    try:
        trigger_audit_models = app_config.trigger_audit_models
    except AttributeError:
        return None
    return trigger_audit_models
