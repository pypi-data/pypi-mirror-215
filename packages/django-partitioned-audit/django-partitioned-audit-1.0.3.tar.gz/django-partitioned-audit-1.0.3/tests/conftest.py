import datetime
import uuid
from datetime import timedelta
from typing import Callable

import pytest
from django.db import connection

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator


@pytest.fixture
def partition_created() -> PartitionInfo:
    """
    Creates a partition for current time, so test can run and audit events inserted.
    We need this because if only the `partitioned table` is created in migration, but no partitions.
    """
    today = datetime.date.today()
    info = PartitionInfo.create(PartitionManager.default_partitioned_table, today, today + timedelta(days=2))
    sql, params = info.generate_create_partition()
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

    yield info

    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE {info.partition}")


@pytest.fixture
def partitioned_table_create():
    def func(partitioned_table):
        with connection.cursor() as cursor:
            sql = f"""
            CREATE TABLE {partitioned_table} (
                column_1 TEXT NULL,
                column_2 TEXT NULL,
                creation_timestamp timestamp with time zone DEFAULT now() NOT NULL
            ) PARTITION BY RANGE (creation_timestamp);
            """
            cursor.execute(sql)

    return func


@pytest.fixture
def very_long_named_partitioned_table(partitioned_table_create: Callable):
    """
    Creates a `partitioned table` with a name that is truncated by postgres.
    Thus, `partitions` will be truncated too.
    """
    partitioned_table = f"partitioned_table_{uuid.uuid4().hex}_long_name_lorem_ipsum_dolor_sit_amet_consectetur"
    assert len(partitioned_table) == 99, partitioned_table

    partitioned_table_create(partitioned_table)

    return partitioned_table


@pytest.fixture
def partitioned_table(partitioned_table_create: Callable):
    """
    Creates a `partitioned table` with a name that is short,
    guaranteeing that names of `partitions` won't be truncated.
    """
    partitioned_table = f"partitioned_table_{uuid.uuid4().hex[0:7]}"
    assert len(partitioned_table) == 25
    partitioned_table_create(partitioned_table)
    return partitioned_table


@pytest.fixture
def disable_triggers():
    trigger_name = "trigger_audit_entry_creator_trigger"
    sql = """
    SELECT DISTINCT event_object_table
    FROM information_schema.triggers
    WHERE trigger_name = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [trigger_name])
        for row in cursor.fetchall():
            event_object_table = row[0]
            print(f"Dropping trigger {trigger_name} on table {event_object_table}")
            cursor.execute(f"DROP TRIGGER {trigger_name} ON {event_object_table};")


@pytest.fixture
def post_drop_partitions():
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    with connection.cursor() as cursor:
        for info in pm.get_existing_partitions():
            cursor.execute(f"DROP TABLE {info.partition}")

    yield

    with connection.cursor() as cursor:
        for info in pm.get_existing_partitions():
            cursor.execute(f"DROP TABLE {info.partition}")
