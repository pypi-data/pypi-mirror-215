import uuid

import pytest
import requests
from app.models import Customer
from django.urls import reverse

from django_partitioned_audit.models import TriggerAuditEntry

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
def test_create_is_audited(live_server, partition_created):
    name = str(uuid.uuid4())
    data = dict(name=name)
    response = requests.post(f"{live_server}{reverse('customer/create')}", data=data)
    response.raise_for_status()
    assert Customer.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry: TriggerAuditEntry = TriggerAuditEntry.objects.all().get()
    assert audit_entry.is_insert()
    assert audit_entry.object_payload_json["name"] == name


@pytest.mark.django_db(transaction=True)
def test_update_is_audited(live_server, partition_created):
    original_name = str(uuid.uuid4())
    customer = Customer.objects.create(name=original_name)

    new_name = str(uuid.uuid4())
    data = dict(name=new_name)
    response = requests.post(f"{live_server}{reverse('customer/update', args=[customer.pk])}", data=data)
    response.raise_for_status()
    assert Customer.objects.filter(name=new_name).exists()

    # Assert model was created and audit exists
    audit_entry: TriggerAuditEntry = TriggerAuditEntry.objects.filter(audit_operation="UPDATE").get()
    assert audit_entry.is_update()
    assert audit_entry.object_payload_json["name"] == new_name


@pytest.mark.django_db(transaction=True)
def test_delete_is_audited(live_server, partition_created):
    name = str(uuid.uuid4())
    customer = Customer.objects.create(name=name)

    response = requests.post(f"{live_server}{reverse('customer/delete', args=[customer.pk])}")
    response.raise_for_status()
    assert not Customer.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry: TriggerAuditEntry = TriggerAuditEntry.objects.filter(audit_operation="DELETE").get()
    assert audit_entry.is_delete()
    assert audit_entry.object_payload_json["name"] == name
