#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: xen_vm_disk_list
author:
    - Anthony Loukinas (@anthonyloukinas)
version_added: "2.7"
short_description: List Xenserver disks
requirements: [ xe ]
description:
    - List Xenserver disks
options:
    vbdparams:
        description: 
            - VBD disk params
        required: false
    vdiparams:
        description: 
            - VDI disk params
        required: false
    vm:
        description: 
            - Narrow down your search by UUID/Name
        required: false
    multiple:
        description: 
            - Allows return of multiple disks
        required: false
    powerstate:
        description: 
            - Narrow down disk search by power-state
        required: false
'''

EXAMPLES = '''
- xen_vm_disk_list
  vm: 29cc955c-5800-a257-94db-636f72af744e
  multiple: true
  powerstate: running
'''

import os
import re
import socket
import traceback

from ansible.module_utils.basic import (
    AnsibleModule,
    get_distribution,
    get_distribution_version,
    get_platform,
    load_platform_subclass,
)
from ansible.module_utils._text import to_native
from ansible.module_utils.xenserver_common import XeBase

class XeVmDiskList(XeBase):
    """
    This is a xe vm-disk-list wrapper class
    """

    def vm_disk_list(self, vm=None, vbd-params=None, vdi-params=None, multiple=True, power-state=None):
        """
        vm_disk_list(str) -> dict
        Args:
            vm (str): uuid/name of vm
            vbdparams (str): vbd disk parameters
            vdiparams (str): vdi disk parameters
            multiple (boolean): return multiple disks
            powerstate (str): state of guest vm
        Returns:
            dict
        """
        self.cmd.append('vm-disk-list')
        if vm != None:
            self.cmd.append('vm=%s' % vm)
        if multiple == True:
            self.cmd.append('--multiple')
        rc, out, err = self.module.run_command(self.cmd)
        if rc != 0:
            self.module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return to_native(out).strip()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vm=str(required=False),
            vbdparams=str(required=False),
            vdiparams=str(required=False),
            multiple=bool(required=False),
            powerstate=str(required=False)
        ),
        supports_check_mode=True,
    )

    vm_disk_list_cmd = XeVmDiskList(module)
    vm_disk_list_vm = module.params['vm']

    out = vm_disk_list_cmd.vm_disk_list(vm=vm_disk_list_vm)

    # split output by \n and : and remove the last 3 indexe I am sure this can be done better
    out_formated = re.split(r"\n|:\s", out.replace(' ', '').strip())[:-3:]
    kw = dict(changed=True, vm_disk_list=out_formated,
              ansible_facts=dict(
                    ansible_fqdn=socket.getfqdn(),
                    ansible_domain='.'.join(socket.getfqdn().split('.')[1:])
                    )
              )

    module.exit_json(**kw)

if __name__ == '__main__':
    main()