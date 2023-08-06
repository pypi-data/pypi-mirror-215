import dataclasses
import datetime
import re
from typing import List
from typing import Optional
from typing import Tuple

PARTITION_PARSER = re.compile(
    r"""
    ^
    (?P<partitioned_table>.+)          # table name prefix
    _                         # separator
    (?P<from_year>\d{4})      # from year
    (?P<from_month>\d{2})     # from month
    (?P<from_day>\d{2})       # from day
    _                         # separator
    (?P<to_year>\d{4})        # to year
    (?P<to_month>\d{2})       # to month
    (?P<to_day>\d{2})         # to day
    $
""",
    re.VERBOSE,
)


@dataclasses.dataclass(frozen=True)
class PartitionInfo:
    partition: str  # was: `table_name`
    from_date: datetime.date
    to_date: datetime.date
    partitioned_table: str

    @classmethod
    def create(cls, partitioned_table: str, from_date: datetime.date, to_date: datetime.date) -> "PartitionInfo":
        partition = f"{partitioned_table}_{from_date.strftime('%Y%m%d')}_{to_date.strftime('%Y%m%d')}"
        return PartitionInfo(
            partition=partition, from_date=from_date, to_date=to_date, partitioned_table=partitioned_table
        )

    @classmethod
    def parse(cls, table_name: str) -> Optional["PartitionInfo"]:
        match = PARTITION_PARSER.fullmatch(table_name)
        if not match:
            return None

        from_date = datetime.date(
            year=int(match.group("from_year")), month=int(match.group("from_month")), day=int(match.group("from_day"))
        )
        to_date = datetime.date(
            year=int(match.group("to_year")), month=int(match.group("to_month")), day=int(match.group("to_day"))
        )
        if from_date >= to_date:
            raise ValueError(f"from_date {from_date} must be before to_date {to_date}")
        return PartitionInfo(
            partition=table_name,
            partitioned_table=match.group("partitioned_table"),
            from_date=from_date,
            to_date=to_date,
        )

    def generate_create_partition(self) -> Tuple[str, List[object]]:
        assert re.fullmatch(r"^[a-zA-Z0-9_]+$", self.partition)
        assert re.fullmatch(r"^[a-zA-Z0-9_]+$", self.partitioned_table)
        # We cannot return tables names as `params` because `execute()` doesn't handle that use case
        # To use `psycopg2.sql.Identifier` we need db connection
        # TODO: find a way to escape tables names, so we don't have to use that regex

        sql_statement = """
        CREATE TABLE "{partition_name}"
            PARTITION OF "{partitioned_table}"
            FOR VALUES FROM (%s) TO (%s);
        """.format(
            partition_name=self.partition, partitioned_table=self.partitioned_table
        )
        params = [self.from_date, self.to_date]
        return sql_statement, params


@dataclasses.dataclass
class TimeRange:
    from_date: datetime.date
    to_date: datetime.date

    def __post_init__(self):
        assert self.from_date < self.to_date
