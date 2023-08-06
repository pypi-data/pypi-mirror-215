import logging

from django.apps import AppConfig
from django.db import connections
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django_partitioned_audit.utils import get_trigger_audit_models

logger = logging.getLogger(__name__)


ENABLE_TRIGGER_SQL = """
-- https://www.postgresql.org/message-id/1360944248465-5745434.post%40n5.nabble.com
DO
$src$
BEGIN
IF NOT EXISTS(SELECT * FROM information_schema.triggers
              WHERE event_object_table = '{table_name}' AND trigger_name = '{trigger_name}')
    THEN

        CREATE TRIGGER {trigger_name}
            AFTER INSERT OR UPDATE OR DELETE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func_v2();

    END IF;
END;
$src$
"""


def enable_trigger_for_table(cursor, table_name: str):
    sql = ENABLE_TRIGGER_SQL.format(
        table_name=table_name,  # FIXME: properly escape this to guarantee avoid SQL injection
        trigger_name="trigger_audit_entry_creator_trigger",
    )

    result = cursor.execute(sql)
    # FIXME: check result

    return sql, result


@receiver(post_migrate)
def audit_run_post_migrate(app_config: AppConfig, verbosity, using, **kwargs):  # pylint: disable=unused-argument
    # TODO: add 'untracked_tables' to AppConfig so we can automatically delete old triggers

    # Django 3.0: emit_post_migrate_signal emited by *flush*, only includes SOME of the documented parameters
    # plan = kwargs.get('plan')
    # apps = kwargs.get('apps')

    trigger_audit_models = get_trigger_audit_models(app_config)
    if trigger_audit_models is None:
        if verbosity >= 2:
            print(f"Ignored: no 'trigger_audit_models' found in app_config {app_config}")
        return

    if not trigger_audit_models:
        if verbosity >= 2:
            print(f"Ignored: empty 'trigger_audit_models' found in app_config {app_config}")
        return

    with connections[using].cursor() as cursor:
        # For now, we use the 'using' connection we received. Not sure if that's the best approach.
        for model_class_name in trigger_audit_models:
            model_class = app_config.get_model(model_class_name)
            table_name = model_class._meta.db_table  # pylint: disable=protected-access
            if verbosity >= 1:
                print(f" - Creating trigger on table '{table_name}'")

            sql, result = enable_trigger_for_table(cursor, table_name)

            if verbosity >= 3:
                print(f"cursor.execute(sql) result: {result}")


# *****************************************************************************
# About original implementation of signal handler
# *****************************************************************************
# ENABLE_TRIGGER_SQL = """
# -- This looks dangerous, but seems to be the recommended approach.
# -- Nevertheless, it looks dangerous, and if for some reason a CASCADE DROP
# --  happens (it should't, but anyway), so, better try some other alternative
# BEGIN;
# DROP TRIGGER IF EXISTS trigger_audit_entry_creator_trigger ON {table_name};
# CREATE TRIGGER trigger_audit_entry_creator_trigger
#     AFTER INSERT OR UPDATE OR DELETE ON {table_name}
#     FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func();
#
# COMMIT;
# """
# *****************************************************************************
