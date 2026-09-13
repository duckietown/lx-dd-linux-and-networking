<p align="center">
<a href="https://duckietown.com"><img src="./assets/images/dtlogo.png" alt="Duckietown Logo" width="50%"></a>
</p>

# Learning Experience (LX): Linux and Networking on the Duckiedrone

`Software: ente`; `Hardware: DD24-B`

Linux and networking provide the conceptual and practical foundation for working with a Duckiedrone. In this learning experience (LX), you will learn how Linux systems, filesystems, processes, and networks fit together, then apply that model through safe local practice and authorized device inspection.

## Intended learning outcomes

### Linux foundations and local practice

Learners will distinguish the Linux kernel, distributions, user space, and
central processing unit (CPU) architecture before navigating a Linux filesystem. They will create and safely
manage files, use wildcards and searches, interpret command results, and
understand standard streams, redirection, pipes, variables, permissions,
processes, and trusted shell scripts. They will also write and verify small
Python and shell programs that read from and write to standard streams.

### Networking

Learners will explain how Media Access Control (MAC) addresses, Internet Protocol
(IP) addresses, subnets, gateways, Dynamic Host Configuration Protocol (DHCP),
Network Address Translation (NAT), firewalls, Domain Name System (DNS), multicast
Domain Name System (mDNS), ports, and network quality support Duckiedrone
connectivity. They will use authorized, targeted `ip`, `getent`, `ping`, `nc`,
`ss`, `curl`, and `dts fleet discover` checks to investigate a connection.

### Authorized device access

Learners will distinguish a base-station shell, a physical Duckiedrone Secure Shell (SSH)
shell, a virtual Duckiedrone shell, and a service-container shell. With
explicit authorization, they will access one Duckiedrone and inspect its
filesystem, processes, and running containers without changing device state.

## Notebooks

Start with required Module 1, which establishes the core Linux concepts used
throughout this LX. The remaining modules are ordered for the complete LX, but
each has a focused orientation and checkpoint so instructors can assign individual concepts.

| # | Notebook | Description |
| --- | --- | --- |
| 1 | `1-linux-foundations-and-distributions.ipynb` | Linux kernel, user space, CPU architecture, and distributions |
| 2 | `2-linux-shell-and-navigation.ipynb` | Terminal, shell, current directory, and paths |
| 3 | `3-shell-variables-quoting-and-environment.ipynb` | Variables, quoting, `PATH`, and environment values |
| 4 | `4-create-and-manage-files.ipynb` | Create, inspect, copy, rename, and safely remove files |
| 5 | `5-filenames-wildcards-and-search.ipynb` | Filename conventions, wildcards, `find`, and `grep` |
| 6 | `6-shell-help-errors-and-exit-status.ipynb` | Help, error recovery, and command status |
| 7 | `7-standard-streams-and-redirection.ipynb` | Standard input (`stdin`), standard output (`stdout`), standard error (`stderr`), and redirection |
| 8 | `8-pipes-and-data-processing.ipynb` | Pipes and composed text processing |
| 9 | `9-shell-scripts-and-execution.ipynb` | Trusted shell scripts, execution, and sourcing |
| 10 | `10-users-ownership-and-permissions.ipynb` | Users, ownership, and least-privilege permissions |
| 11 | `11-processes-monitoring-and-job-control.ipynb` | Controlled jobs, process inspection, and read-only monitoring |
| 12 | `12-shell-exercises-and-output-verification.ipynb` | Stream exercises and output comparison |
| 13 | `13-network-addressing-and-routing.ipynb` | Local networks, addressing, subnets, gateways, and Internet Protocol version 6 (IPv6) |
| 14 | `14-network-protocols-and-quality.ipynb` | Endpoints, protocols, packet layers, and network quality |
| 15 | `15-localhost-and-service-binding.ipynb` | Localhost and service binding |
| 16 | `16-network-configuration-and-access-policy.ipynb` | DHCP, private networks, NAT, firewalls, and access policy |
| 17 | `17-network-names-and-service-discovery.ipynb` | DNS, mDNS, Uniform Resource Locators (URLs), discovery, and service availability |
| 18 | `18-network-diagnostics-and-testing.ipynb` | Authorized local and Duckiedrone diagnostic checks |
| 19 | `19-physical-duckiedrone-ssh-access.ipynb` | Authorized physical Duckiedrone SSH access |
| 20 | `20-virtual-duckiedrone-connections.ipynb` | Local virtual Duckiedrone access |
| 21 | `21-duckiedrone-filesystem-inspection.ipynb` | Read-only Duckiedrone filesystem tour |
| 22 | `22-duckiedrone-process-inspection.ipynb` | Read-only Duckiedrone process inspection |

## What you need

Your base station is the development computer that runs Visual Studio Code (VS Code). For local
modules, use an ordinary Linux terminal, a development container provided for
this LX, or the [Duckietown Workspace](https://github.com/duckietown/workspace).
A development container is optional unless your instructor's instructions
require it.

### Linux foundation and practice modules

Modules 1 through 12 run in any of those local Linux environments. They need a
terminal and the LX files only; no Duckiedrone or network access is required.

### Networking modules

Modules 13 through 17 are conceptual. Module 18's localhost examples are safe
in the local Linux environment you chose. Its discovery command requires
the Duckietown Shell on an authorized base station, and its Duckiedrone checks
require a known authorized device and network.

### Authorized device modules

Modules 19 through 22 require either an authorized physical Duckiedrone or an
authorized virtual Duckiedrone. Physical access also needs an approved network
path and verified Secure Shell (SSH) identity. Virtual access uses the Duckietown
Shell's local virtual-device workflow. Filesystem and process inspection starts only
after one authorized device shell is open.

You can complete local work independently. For physical-device or network
activity, use only equipment and networks you own or are explicitly authorized
to administer. Where a module refers to an instructor or information technology (IT) team, an
independent learner should follow the device owner's documentation, their
network-administration policy, or appropriate local support.

## Complete the shell exercises

Starter files are in `packages/shell_exercises/`. Work from the LX root, edit
the files described in the Shell Exercises and Output Verification module, and
check their syntax with:

```bash
python3 -m py_compile packages/shell_exercises/*.py
bash -n packages/shell_exercises/hello.sh
```

The notebooks explain how to run each completed script with input from the terminal or a pipe.

## Further reading

See the [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/),
the [Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html),
and the Internet Engineering Task Force (IETF) [IPv6 specification (RFC 8200)](https://www.rfc-editor.org/rfc/rfc8200).

## For LX authors

Learner material is in `notebooks/` and `packages/`. Structural checks are in `tests/`, and the exercise image recipe is maintained in the paired `lx-dd-linux-and-networking-recipe` repository.
Run the structural checks from the LX root:

```bash
pytest tests/
```
