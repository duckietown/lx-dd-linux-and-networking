<p align="center">
<a href="https://duckietown.com"><img src="./assets/images/dtlogo.png" alt="Duckietown Logo" width="50%"></a>
</p>

# Learning Experience (LX): Linux and Networking on the Duckiedrone

`Software: ente`; `Hardware: DD24-B`

Linux and networking provide the conceptual and practical foundation for working with a Duckiedrone. In this learning experience (LX), you will learn how Linux systems, filesystems, processes, and networks fit together, then apply that model through safe local practice and authorized device inspection.

## Intended learning outcomes

After completing this learning experience, learners will be able to:

1. Distinguish the Linux kernel, distributions, user space, and central processing unit (CPU) architecture before navigating a Linux filesystem. Create and safely manage files, use wildcards and searches, interpret command results, understand standard streams, redirection, pipes, variables, permissions, processes, and trusted shell scripts, and write and verify small Python and shell programs that read from and write to standard streams.

2. Explain how Media Access Control (MAC) addresses, Internet Protocol (IP) addresses, subnets, gateways, Dynamic Host Configuration Protocol (DHCP), Network Address Translation (NAT), firewalls, Domain Name System (DNS), multicast Domain Name System (mDNS), ports, and network quality support Duckiedrone connectivity. Use authorized, targeted `ip`, `getent`, `ping`, `nc`, `ss`, `curl`, and `dts fleet discover` checks to investigate a connection.

3. Distinguish a base-station shell, a physical Duckiedrone Secure Shell (SSH) shell, a virtual Duckiedrone shell, and a service shell. With explicit authorization, access one Duckiedrone and inspect its filesystem, processes, and running services without changing device state.

## Notebooks

Start with [Notebook 1](./notebooks/1-linux-foundations-and-distributions.ipynb), which establishes the core Linux concepts used throughout this LX. The remaining notebooks are ordered for the complete LX, but each has a focused orientation and checkpoint so it can be completed independently or used to focus on an individual concept.

| # | Notebook | Description |
| --- | --- | --- |
| 1 | [Notebook 1](./notebooks/1-linux-foundations-and-distributions.ipynb) | Linux kernel, user space, CPU architecture, and distributions |
| 2 | [Notebook 2](./notebooks/2-linux-shell-and-navigation.ipynb) | Terminal, shell, current directory, and paths |
| 3 | [Notebook 3](./notebooks/3-shell-variables-quoting-and-environment.ipynb) | Variables, quoting, `PATH`, and environment values |
| 4 | [Notebook 4](./notebooks/4-create-and-manage-files.ipynb) | Create, inspect, copy, rename, and safely remove files |
| 5 | [Notebook 5](./notebooks/5-filenames-wildcards-and-search.ipynb) | Filename conventions, wildcards, `find`, and `grep` |
| 6 | [Notebook 6](./notebooks/6-shell-help-errors-and-exit-status.ipynb) | Help, error recovery, and command status |
| 7 | [Notebook 7](./notebooks/7-standard-streams-and-redirection.ipynb) | Standard input (`stdin`), standard output (`stdout`), standard error (`stderr`), and redirection |
| 8 | [Notebook 8](./notebooks/8-pipes-and-data-processing.ipynb) | Pipes and composed text processing |
| 9 | [Notebook 9](./notebooks/9-shell-scripts-and-execution.ipynb) | Trusted shell scripts, execution, and sourcing |
| 10 | [Notebook 10](./notebooks/10-users-ownership-and-permissions.ipynb) | Users, ownership, and least-privilege permissions |
| 11 | [Notebook 11](./notebooks/11-processes-monitoring-and-job-control.ipynb) | Controlled jobs, process inspection, and read-only monitoring |
| 12 | [Notebook 12](./notebooks/12-shell-exercises-and-output-verification.ipynb) | Stream exercises and output comparison |
| 13 | [Notebook 13](./notebooks/13-physical-duckiedrone-ssh-access.ipynb) | Authorized physical Duckiedrone SSH access |
| 14 | [Notebook 14](./notebooks/14-virtual-duckiedrone-connections.ipynb) | Local virtual Duckiedrone access |
| 15 | [Notebook 15](./notebooks/15-duckiedrone-filesystem-inspection.ipynb) | Read-only Duckiedrone filesystem tour |
| 16 | [Notebook 16](./notebooks/16-duckiedrone-process-inspection.ipynb) | Read-only Duckiedrone process inspection |
| 17 | [Notebook 17](./notebooks/17-network-addressing-and-routing.ipynb) | Inspect local networks, addresses, subnets, gateways, and Internet Protocol version 6 (IPv6) |
| 18 | [Notebook 18](./notebooks/18-network-protocols-and-quality.ipynb) | Inspect endpoints, protocols, packet layers, and network quality |
| 19 | [Notebook 19](./notebooks/19-localhost-and-service-binding.ipynb) | Test localhost and service binding safely |
| 20 | [Notebook 20](./notebooks/20-network-configuration-and-access-policy.ipynb) | Inspect DHCP, private addresses, NAT, firewalls, and access policy |
| 21 | [Notebook 21](./notebooks/21-network-names-and-service-discovery.ipynb) | Use DNS, mDNS, Uniform Resource Locators (URLs), discovery, and service availability evidence |
| 22 | [Notebook 22](./notebooks/22-network-diagnostics-and-testing.ipynb) | Authorized local and Duckiedrone diagnostic checks |

## What you need

Before starting this LX, complete the Duckietown Manual's [Initial Setup](https://docs.duckietown.com/ente/duckietown-manual/10-setup/setup-introduction.html) so Docker and the Duckietown Shell (`dts`) are installed and configured on the base station. This LX assumes that setup; explanations of Docker are deferred to the Docker LX.

Your base station is the development computer that runs Visual Studio Code (VS Code), Docker, and `dts`. `dts code editor` starts a separate browser-editor environment from a base-station terminal. Its terminal, filesystem, and `localhost` are separate from the base station.

### Choose the terminal

| Task | Where to run it |
| --- | --- |
| Read and edit notebooks; complete self-contained local exercises in the local-practice notebooks; run [Notebook 22](./notebooks/22-network-diagnostics-and-testing.ipynb) localhost examples | The `dts code editor` terminal or another local Linux environment chosen for this LX |
| Run `dts fleet discover`, `dts duckiebot virtual ...`, or physical-device `getent`, `ping`, `ssh`, and `ssh-copy-id` commands | A separate base-station terminal, outside `dts code editor` |
| Inspect files, processes, routes, or sockets after connecting to a device | The authorized physical or virtual Duckiedrone shell |
| Inspect a particular running service | The relevant service shell or workbench |

Keep the base-station terminal open while using the browser editor. A command's availability does not make it a base-station command: `dts`, base-station credentials, and the base station's network path remain outside the editor environment. For local notebooks, use an ordinary Linux terminal, the development environment provided for this LX, or the [Duckietown Workspace](https://github.com/duckietown/workspace). A dedicated development environment is optional unless the setup documentation for your learning environment requires it.

### Linux foundations and local practice

The shell commands in the local-practice notebooks run in any of those local Linux environments. They need a terminal and the LX files only; no Duckiedrone or network access is required. Interactive checkpoints require the notebook metadata supplied by `dts code editor`; a compatible Jupyter/IPython kernel with `ipywidgets` available is not sufficient by itself.

### Networking

Start with either authorized physical access in [Notebook 13](./notebooks/13-physical-duckiedrone-ssh-access.ipynb) or the local virtual workflow in [Notebook 14](./notebooks/14-virtual-duckiedrone-connections.ipynb). Then use [Notebook 15](./notebooks/15-duckiedrone-filesystem-inspection.ipynb) and [Notebook 16](./notebooks/16-duckiedrone-process-inspection.ipynb) to orient yourself in the authorized Duckiedrone shell before continuing to network concepts. [Notebook 22](./notebooks/22-network-diagnostics-and-testing.ipynb)'s localhost examples are safe in the local Linux environment you chose. Run `dts fleet discover` and checks that need the base station's network path from the separate base-station terminal. Once `ssh` or `dts duckiebot virtual connect` opens a Duckiedrone shell, `localhost`, processes, routes, and sockets describe that Duckiedrone rather than the editor or base station.

### Authorized device access

[Notebook 13](./notebooks/13-physical-duckiedrone-ssh-access.ipynb) requires an authorized physical Duckiedrone; [Notebook 14](./notebooks/14-virtual-duckiedrone-connections.ipynb) uses the Duckietown Shell's local virtual workflow. Physical access also needs a network path you own or are explicitly authorized to administer and a verified SSH identity. Filesystem inspection in [Notebook 15](./notebooks/15-duckiedrone-filesystem-inspection.ipynb) and process inspection in [Notebook 16](./notebooks/16-duckiedrone-process-inspection.ipynb) start only after one authorized device shell is open.

You can complete local work independently. For physical-device or network activity, use only equipment and networks you own or are explicitly authorized to administer. Follow the applicable device documentation and network policy. If you cannot verify authorization or resolve a problem using those resources, stay with local or virtual activities rather than broadening the test.

## Complete the Linux shell exercises

Starter files are in `packages/shell_exercises/`. Work from the LX root, edit the files described in the Shell Exercises and Output Verification notebook, and check their syntax with:

```bash
python3 -m py_compile packages/shell_exercises/*.py
bash -n packages/shell_exercises/hello.sh
```

The notebooks explain how to run each completed script with input from the terminal or a pipe.

## Further reading

Each notebook's Further reading section is the primary reference for its lesson. This guide groups the course's verified sources:

- **Linux foundations and distributions:** [Linux Kernel documentation](https://docs.kernel.org/), [CPU architecture documentation](https://docs.kernel.org/arch/index.html), the [Debian overview](https://www.debian.org/intro/about), the [Ubuntu project overview](https://ubuntu.com/about), and [Fedora project documentation](https://docs.fedoraproject.org/en-US/project/).

- **Shell, files, and scripts:** the Ubuntu [Linux command-line tutorial](https://ubuntu.com/desktop/docs/en/latest/tutorial/the-linux-command-line-for-beginners/); GNU's Not Unix (GNU) Bash references for [parameters and expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html), [builtins](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html), [redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html), [pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html), and [job control](https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html); the [GNU Findutils manual](https://www.gnu.org/software/findutils/manual/html_mono/find.html), the [GNU Grep manual](https://www.gnu.org/software/grep/manual/grep.html), the [GNU diffutils manual](https://www.gnu.org/software/diffutils/manual/), and the [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html).

- **Duckiedrone access and inspection:** the [Duckietown Manual](https://docs.duckietown.com/ente/duckietown-manual/), the [Duckiedrone DD24 manual](https://docs.duckietown.com/ente/opmanual-dd24/), the OpenSSH [`ssh` client manual](https://man.openbsd.org/ssh.1), and the Linux [`ps(1)` manual](https://man7.org/linux/man-pages/man1/ps.1.html).

- **Network addressing, policy, and discovery:** the Linux [`ip address`](https://man7.org/linux/man-pages/man8/ip-address.8.html) and [`ip(7)`](https://man7.org/linux/man-pages/man7/ip.7.html) manuals; IETF specifications for [packet delay variation](https://www.rfc-editor.org/rfc/rfc3393), [DHCP](https://www.rfc-editor.org/rfc/rfc2131), [private IPv4 addresses](https://www.rfc-editor.org/rfc/rfc1918), [traditional NAT](https://www.rfc-editor.org/rfc/rfc3022), and [mDNS](https://www.rfc-editor.org/rfc/rfc6762).

- **Targeted diagnostics:** manual pages for [getent](https://man7.org/linux/man-pages/man1/getent.1.html), [`ip route`](https://man7.org/linux/man-pages/man8/ip-route.8.html), [`ss`](https://man7.org/linux/man-pages/man8/ss.8.html), and [ping](https://man7.org/linux/man-pages/man8/ping.8.html), plus curl's [command-line reference](https://curl.se/docs/manpage.html).

## For LX authors

Learner material is in `notebooks/` and `packages/`. Structural checks are in `tests/`, and the exercise image recipe is maintained in the paired `lx-dd-linux-and-networking-recipe` repository. Run the structural checks from the LX root:

```bash
python3 -m pytest tests/
```
