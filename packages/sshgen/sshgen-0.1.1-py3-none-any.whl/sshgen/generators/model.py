#!/usr/bin/env python
from ruamel.yaml import CommentedMap

from sshgen.models.host import HostModel
from sshgen.models.metafields import MetaFieldsModel


class MapToHost:
    def convert(self, parsed_hosts: CommentedMap) -> list[HostModel]:
        host_models = []

        for host_group, hosts in parsed_hosts.items():
            for host, host_details in hosts['hosts'].items():
                model = HostModel(
                    host=host,
                    host_group=host_group,
                    ansible_host=host_details['ansible_host'],
                    ansible_user=host_details['ansible_user']
                )

                meta = host_details.get('_meta', {})
                auth_type = meta.get('_auth_type')
                auth_path = meta.get('_auth_path')
                aliases = meta.get('_aliases')

                if any(isinstance(field, str | list) for field in (auth_type, auth_path, aliases)):
                    model.meta_fields = MetaFieldsModel(auth_type, auth_path, aliases)

                host_models.append(model)

        return host_models
