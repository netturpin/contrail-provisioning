#!/usr/bin/python
#
# Copyright (c) 2015 Juniper Networks, Inc. All rights reserved.
#
"""Upgrade's Contrail Database components."""

from setup import DatabaseSetup
from contrail_provisioning.common.upgrade import ContrailUpgrade

from fabric.api import local


class DatabaseUpgrade(ContrailUpgrade, DatabaseSetup):
    def __init__(self, args_str = None):
        ContrailUpgrade.__init__(self)
        DatabaseSetup.__init__(self)

        self.update_upgrade_data()

    def update_upgrade_data(self):
        self.upgrade_data['upgrade'] = self._args.packages
        self.upgrade_data['restore'].append(
            '/etc/contrail/database_nodemgr_param')
        self.upgrade_data['rename_config'].append(
            ('/etc/contrail/database_nodemgr_param',
             '/etc/contrail/contrail-database-nodemgr.conf'))

    def restart(self):
        local('service zookeeper restart')
        local('service supervisor-database restart')

    def upgrade(self):
        self._upgrade()
        self.upgrade_python_pkgs()
        self.restart()


def main():
    database = DatabaseUpgrade()
    database.upgrade()

if __name__ == "__main__":
    main()