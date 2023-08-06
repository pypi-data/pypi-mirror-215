========================
django-partitioned-audit
========================

Creates an audit log of the modifications made to models, by using triggers.

* Only PostgreSql supported.
* Models to audit are configured in ``AppConfig``
* Triggers are applied automatically when running ``python manage.py migrate``
* The whole row is saved by the trigger by using PostgreSql's ``row_to_json()``
* The audit table is partitioned
* Management command `manage_partition_tables` creates required partitions
  * there are 3 partition strategies: one per month, one per week, one per day.

Quick start
-----------

1. Add "django_partitioned_audit" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_partitioned_audit',

        'your.app1.App1Config',
        'your.app2.App2Config',
        'your.app3.App3Config',
    ]

2. Run ``python manage.py migrate`` to create the partitioned table.

3. Run ``manage.py manage_partition_tables create --extra-days=60`` to create the partitions::

    $ manage.py manage_partition_tables create --extra-days=60
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220301_20220401  |  2022-03-01  |  2022-04-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220401_20220501  |  2022-04-01  |  2022-05-01  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+

You should run that command periodically, to make sure the database always contains a partition where to insert data.

4. Register the models you want to audit in your ``AppConfig`` instances::

    from django.apps import AppConfig
    class MyAppConfig(AppConfig):
        name = "myapp"
        trigger_audit_models = (
            'Model1',
            'Model2',
            'Model3',
        )

5. Run ``python manage.py migrate`` to create the triggers.


Security of audit entries
+++++++++++++++++++++++++

DBA should correctly configure permissions, in a way that the user used to
connect to the database from Django has permissions to INSERT rows in the
``trigger_audit_entries`` table, but NO permissions to UPDATE / DELETE them.

If security is not important and you just want to avoid deleting the audit
entries by accident, a solution could be
https://docs.djangoproject.com/en/3.1/topics/db/multi-db/#automatic-database-routing


How it works
------------

#. A trigger is executed with each insert/update/delete operation

   * the database trigger is created by ``python manage.py migrate``.
   * only for the tables associated to the models that are explicitly
     specified in your ``AppConfig``.

#. The trigger creates a new row in ``trigger_audit_entries`` table containing:

   * ``object_table``: table where the modification happened (one of your models)
   * ``object_payload``: JSON representation of the whole row (after modification)
   * ``audit_entry_created``: timestamp
   * ``audit_txid_current``: PostgreSql TXID in which the modification occurred
   * ``audit_operation``: operation: ``INSERT``, ``UPDATE``, ``DELETE``


Trigger
+++++++

The solution is very simple in terms of code running in PostgreSQL: just a trigger that calls a function.

The trigger just invokes the function for each ``INSERT``, ``UPDATE``, ``DELETE`` ::

    CREATE TRIGGER trigger_audit_entry_creator_trigger
        AFTER INSERT OR UPDATE OR DELETE ON {table_name}
        FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func_v2();

The function just serializes the row into a JSON and insert it in the audit table::

    CREATE FUNCTION trigger_audit_entry_creator_func_v2() RETURNS TRIGGER AS $scr$
        DECLARE
            object_payload  varchar;
        BEGIN
            IF (TG_OP = 'INSERT') THEN
                object_payload  = row_to_json(NEW);
            ELSIF (TG_OP = 'UPDATE') THEN
                object_payload  = row_to_json(NEW);
            ELSIF (TG_OP = 'DELETE') THEN
                object_payload  = row_to_json(OLD);
            ELSE
                RAISE EXCEPTION 'Unexpected TG_OP = %', TG_OP;
            END IF;

            INSERT INTO trigger_audit_entries_v2 (
                    object_table,
                    object_payload,
                    audit_entry_created,
                    audit_txid_current,
                    audit_operation,
                    audit_version
                )
                SELECT
                    TG_TABLE_NAME,
                    object_payload,
                    now(),
                    txid_current(),
                    TG_OP,
                    2;
            RETURN NULL;
        END;
    $scr$ LANGUAGE plpgsql;

Management of partitions
------------------------

The Django custom management command `manage_partition_tables` can be used to manage the partitions.

Sample usage
++++++++++++

If you want to have enough partition to handle next 90 days (around 3 months), you can use `--extra-days=90`.
Because it's the first time we run the command, no partition exists, and the plan will report that all
partitions need to be created::


    $ manage.py manage_partition_tables simulate --extra-days=90
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220301_20220401  |  2022-03-01  |  2022-04-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220401_20220501  |  2022-04-01  |  2022-05-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220501_20220601  |  2022-05-01  |  2022-06-01  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+


We can also see the plan if no extra days are requested (this way, we'll only create partitions for
the current month::


    $ manage.py manage_partition_tables simulate --extra-days=0
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+


Now let's create the partitions::


    $ manage.py manage_partition_tables create --extra-days=0
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+
    sql: CREATE TABLE "trigger_audit_entries_v2_20220201_20220301" PARTITION OF "trigger_audit_entries_v2" FOR VALUES FROM (%s) TO (%s); / params: [datetime.date(2022, 2, 1), datetime.date(2022, 3, 1)]


If we run the command and we pass `--extra-days=90`, the partition for the current month already exists, and
only partitions for next months (to cover 90 days) will be created::


    $ manage.py manage_partition_tables create --extra-days=90
    +----------------------------------------------+--------------+--------------+----------------+
    |  table_name                                  |  from_date   |  to_date     |  status        |
    +----------------------------------------------+--------------+--------------+----------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |  ✓ exists      |
    |  trigger_audit_entries_v2_20220301_20220401  |  2022-03-01  |  2022-04-01  |  ❌ to create  |
    |  trigger_audit_entries_v2_20220401_20220501  |  2022-04-01  |  2022-05-01  |  ❌ to create  |
    |  trigger_audit_entries_v2_20220501_20220601  |  2022-05-01  |  2022-06-01  |  ❌ to create  |
    +----------------------------------------------+--------------+--------------+----------------+
    sql: CREATE TABLE "trigger_audit_entries_v2_20220301_20220401" PARTITION OF "trigger_audit_entries_v2" FOR VALUES FROM (%s) TO (%s); / params: [datetime.date(2022, 3, 1), datetime.date(2022, 4, 1)]
    sql: CREATE TABLE "trigger_audit_entries_v2_20220401_20220501" PARTITION OF "trigger_audit_entries_v2" FOR VALUES FROM (%s) TO (%s); / params: [datetime.date(2022, 4, 1), datetime.date(2022, 5, 1)]
    sql: CREATE TABLE "trigger_audit_entries_v2_20220501_20220601" PARTITION OF "trigger_audit_entries_v2" FOR VALUES FROM (%s) TO (%s); / params: [datetime.date(2022, 5, 1), datetime.date(2022, 6, 1)]


We can use `list` to list existing partitions::


    $ manage.py manage_partition_tables list
    +----------------------------------------------+--------------+--------------+
    |  table_name                                  |  from_date   |  to_date     |
    +----------------------------------------------+--------------+--------------+
    |  trigger_audit_entries_v2_20220201_20220301  |  2022-02-01  |  2022-03-01  |
    |  trigger_audit_entries_v2_20220301_20220401  |  2022-03-01  |  2022-04-01  |
    |  trigger_audit_entries_v2_20220401_20220501  |  2022-04-01  |  2022-05-01  |
    |  trigger_audit_entries_v2_20220501_20220601  |  2022-05-01  |  2022-06-01  |
    +----------------------------------------------+--------------+--------------+


Partition per week
++++++++++++++++++

We can use one partition per week::


    $ manage.py manage_partition_tables create --extra-days=30 --time-range-generator=WeeklyTimeRangeGenerator
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220222_20220301  |  2022-02-22  |  2022-03-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220301_20220308  |  2022-03-01  |  2022-03-08  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220308_20220315  |  2022-03-08  |  2022-03-15  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220315_20220322  |  2022-03-15  |  2022-03-22  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220322_20220329  |  2022-03-22  |  2022-03-29  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+


Partition per day
+++++++++++++++++

We can use one partition per day::


    $ manage.py manage_partition_tables create --extra-days=10 --time-range-generator=DailyTimeRangeGenerator
    +----------------------------------------------+--------------+--------------+---------------+
    |  table_name                                  |  from_date   |  to_date     |  status       |
    +----------------------------------------------+--------------+--------------+---------------+
    |  trigger_audit_entries_v2_20220222_20220223  |  2022-02-22  |  2022-02-23  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220223_20220224  |  2022-02-23  |  2022-02-24  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220224_20220225  |  2022-02-24  |  2022-02-25  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220225_20220226  |  2022-02-25  |  2022-02-26  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220226_20220227  |  2022-02-26  |  2022-02-27  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220227_20220228  |  2022-02-27  |  2022-02-28  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220228_20220301  |  2022-02-28  |  2022-03-01  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220301_20220302  |  2022-03-01  |  2022-03-02  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220302_20220303  |  2022-03-02  |  2022-03-03  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220303_20220304  |  2022-03-03  |  2022-03-04  |  ⚠ to create  |
    |  trigger_audit_entries_v2_20220304_20220305  |  2022-03-04  |  2022-03-05  |  ⚠ to create  |
    +----------------------------------------------+--------------+--------------+---------------+


Test
----

Tested on:

* Python 3.8, 3.9, 3.10, 3.11
* Django 3.2, 4.1, 4.2
* PostgreSql 12, 13, 14, 15


Known issues
------------

* Not tested with psycopg3
* Coupled to Django (would be nice if Django is supported but possible to use it without Django)
* Only a single app can use it (will be solved when decoupled from Django)
* Works only on default db schema
