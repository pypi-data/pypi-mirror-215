#!/usr/bin/env python
from dataclasses import dataclass

from sshgen.models.metafields import MetaFieldsModel


@dataclass
class HostModel:
    host: str
    host_group: str
    ansible_host: str
    ansible_user: str
    meta_fields: MetaFieldsModel | None = None
