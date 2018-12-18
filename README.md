# Ansible Xenserver Module
A custom ansible module for working with Xenserver. It is a wrapper around the xe command. This is a fork of an old project hoping to spring some life into it. I've run into the need for more native Ansible integration and would like to open this project up to anyone with spare time and interest in automating XenServer.

## Setup
- Requires ansible 2.4+
- Requires build tools (make)

#### Ubuntu/Debian
```
sudo apt install build-essential
```

#### CentOS/Fedora/RedHat Enterprise
```
sudo yum group install "Development Tools"
```

## Install
Next build the module.
```
make
make install
# It installs under /usr/share/ansible/xenserver
```
Edit /etc/ansible/ansible.cfg and add the following lines:
```
library = /usr/share/ansible/modules
module_utils = /usr/share/ansible/module_utils
```
## Uninstall
```
make uninstall
```

## Example play using the module
```
---
- hosts: xenserver01
  remote_user: root
  tasks:
    - name: "List xen guests"
      xen_vm_list:
        params: all
        
    - name: "install vm"
      xen_vm_install:
        template: <template uuid>
        name_label: test-from-ansible
      register: vm_uuid

    - name: "start vm"
      xen_vm_start:
        uuid: "{{ vm_uuid.uuid }}"

    - name: "get ipv4 address"
      xen_vm_param:
        uuid: "{{ vm_uuid.uuid }}"
        param: networks
      register: vm_ip
...
```
## Develop

Follow the Ansible Development Documentation and Style Guides.  

## Contribute:

Please fork, make changes on a feature branch and open up a pull request.