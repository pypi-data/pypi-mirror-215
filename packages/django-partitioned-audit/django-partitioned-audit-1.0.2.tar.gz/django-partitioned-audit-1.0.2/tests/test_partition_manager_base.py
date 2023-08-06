import pytest
from django.db import connection

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_time_range import BasePartitionManager
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator as MTRG
from django_partitioned_audit.partitions.time_range_partitioning import NotImplementedTimeRangeGenerator


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("tmg_class", [MTRG, NotImplementedTimeRangeGenerator])
def test_get_tables(tmg_class):
    pm = BasePartitionManager(time_range_generator=tmg_class())
    tables = pm.get_tables()
    assert set(tables) == {
        "app_customer",
        "app_invoice",
        "app_product",
        "auth_group",
        "auth_group_permissions",
        "auth_permission",
        "auth_user",
        "auth_user_groups",
        "auth_user_user_permissions",
        "django_admin_log",
        "django_content_type",
        "django_migrations",
        "django_session",
        "trigger_audit_entries_v2",
        "trigger_audit_entries_v2_view",
    }


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("tmg_class", [MTRG, NotImplementedTimeRangeGenerator])
def test_get_existing_partitions_when_partitions_exists(partitioned_table: str, tmg_class):
    with connection.cursor() as cursor:
        sql = f"""
        CREATE TABLE {partitioned_table}_19990101_19990201
            PARTITION OF {partitioned_table}
            FOR VALUES FROM ('1999-01-01') TO ('1999-02-01');
        """
        cursor.execute(sql)

    partition = f"{partitioned_table}_19990101_19990201"

    pm = PartitionManager(partitioned_table=partitioned_table, time_range_generator=tmg_class())
    assert partitioned_table in pm.get_tables()
    assert partition in pm.get_tables()

    assert set(pm.get_existing_partitions()) == {PartitionInfo.parse(partition)}


@pytest.mark.django_db
@pytest.mark.parametrize("tmg_class", [MTRG, NotImplementedTimeRangeGenerator])
def test_get_existing_partitions_when_no_partitions(partitioned_table: str, tmg_class):
    pm = PartitionManager(partitioned_table=partitioned_table, time_range_generator=tmg_class())
    assert partitioned_table in pm.get_tables()
    partitions = list(pm.get_existing_partitions())
    assert len(partitions) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("tmg_class", [MTRG, NotImplementedTimeRangeGenerator])
def test_create_partitions(partitioned_table: str, tmg_class):
    pm = PartitionManager(partitioned_table=partitioned_table, time_range_generator=tmg_class())

    partition = f"{partitioned_table}_19990101_19990201"
    partition_info = PartitionInfo.parse(partition)

    assert partitioned_table in pm.get_tables()
    assert partition not in pm.get_tables()

    pm.create_partitions([partition_info])

    assert partition in pm.get_tables()
