# sshgen

SSH configuration generator based on your Ansible hosts YAML file.

Current version: v0.1.1

## Table of Contents

<!-- insert TOC here -->

TBD

## Features

1. Generates a `config` file to merge with your existing SSH configuration.
2. Custom configuration for ssh-agent.
3. Custom SSH aliases for quick connections.

## Installation

### Using pip

```shell
pip install --user git+https://github.com/pythoninja/sshgen@v0.1.1
```

### Using pipx

```shell
pipx install git+https://github.com/pythoninja/sshgen@v0.1.1
```

## Usage

Before using this tool, make sure you have an Ansible `hosts.yml` in your current working directory.

Consider the following example `hosts.yml` file, which defines 2 host groups with a total of 3 hosts:

```yaml
group1: # host_group
  hosts:
    host1: # host
      ansible_host: 127.0.0.1
      ansible_user: root
      _meta:
        _auth_type: IdentityAgent
        _auth_path: ~/.1password/agent.sock
        _aliases: [ "base", "another-alias" ]

    host2:
      ansible_host: 127.0.0.2
      ansible_user: manager
      ansible_password:

group2:
  hosts:
    another_host1:
      ansible_host: 172.19.0.1
      ansible_user: postgres
      ansible_password:
```

To use `sshgen`, you can either invoke it as a Python module using `python -m sshgen --help` or directly use the
command `sshgen --help`.

By default, `sshgen` looks for the `hosts.yml` file in your current working directory. To generate the SSH
configuration, run the following command:

```shell
sshgen generate
```

After executing the command, you will see the following output:

```text
[INFO] - Generated SSH config file was saved to /my_dir/config
```

Check the file contents `cat /my_dir/config`:

```
Host host1 base another-alias # group1
    HostName 127.0.0.1
    User root
    IdentityAgent ~/.1password/agent.sock

Host host2  # group1
    HostName 127.0.0.2
    User manager
    IdentityFile ~/.ssh/ssh_key
    IdentitiesOnly yes

Host another_host1  # group2
    HostName 172.19.0.1
    User postgres
    IdentityFile ~/.ssh/ssh_key
    IdentitiesOnly yes
```

Copy and insert the output into your `~/.ssh/config` file. After that, you can use any of the defined aliases to SSH
into the corresponding hosts. For example, running `ssh base` will connect you to the host with the IP address 127.0.0.1
as the root user and utilizing 1password as your SSH agent.

For more examples, please refer to the [examples](https://github.com/pythoninja/sshgen/tree/master/examples) directory.

## License

There are no specific requirements for usage and distribution. For more information, refer to
the [LICENSE](https://github.com/pythoninja/sshgen/blob/master/LICENSE).

## Changelog

For the changelog, please see [CHANGELOG.md](https://github.com/pythoninja/sshgen/blob/master/CHANGELOG.md).
