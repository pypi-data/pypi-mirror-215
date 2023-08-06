import json
import logging

from django.db import models
from django.db.models import Model

import django_partitioned_audit.signals  # noqa pylint: disable=unused-import

logger = logging.getLogger(__name__)


class TriggerAuditEntry(Model):
    """
    This model exists to facilitate reading audit events.
    This maps to the partitioned table, which is manually created using migrations.

    This is mapped to the view, because Django requires a PK, so no update or delete
    operations can be done, but a `truncate()` method is provided to simplify testing.
    """

    object_table = models.CharField(max_length=128)
    object_payload = models.TextField()

    audit_entry_created = models.DateTimeField(auto_now_add=True)
    audit_txid_current = models.BigIntegerField()
    audit_operation = models.CharField(max_length=32)
    audit_version = models.IntegerField()

    class Meta:
        managed = False
        db_table = "trigger_audit_entries_v2_view"

    def __str__(self):
        return f"{self.__class__.__name__} " f"{self.object_table} " f"{self.audit_operation}"

    @property
    def object_payload_json(self) -> dict:
        return json.loads(self.object_payload)

    def is_insert(self):
        return self.audit_operation == "INSERT"

    def is_update(self):
        return self.audit_operation == "UPDATE"

    def is_delete(self):
        return self.audit_operation == "DELETE"
