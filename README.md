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

Before starting this LX, complete the Duckietown Manual's [Initial Setup](https://docs.duckietown.com/ente/duckietown-manual/10-setup/setup-introduction.html) so Docker and the Duckietown Shell (`dts`) are installed and configured on the base station. This LX assumes that setup; explanations of Docker are deferred to the Docker LX.

Your base station is the development computer that runs Visual Studio Code (VS Code), Docker, and `dts`. `dts code editor` starts a separate browser-editor environment from a base-station terminal. Its terminal, filesystem, and `localhost` are separate from the base station.

### Choose the terminal

| Task | Where to run it |
| --- | --- |
| Read and edit notebooks; complete self-contained local exercises in Notebooks [1](./notebooks/1-linux-foundations-and-distributions.ipynb) through [12](./notebooks/12-shell-exercises-and-output-verification.ipynb); run [Notebook 18](./notebooks/18-network-diagnostics-and-testing.ipynb) localhost examples | The `dts code editor` terminal or another local Linux environment chosen for this LX |
| Run `dts fleet discover`, `dts duckiebot virtual ...`, or physical-device `getent`, `ping`, `ssh`, and `ssh-copy-id` commands | A separate base-station terminal, outside `dts code editor` |
| Inspect files, processes, routes, or sockets after connecting to a device | The authorized physical or virtual Duckiedrone shell |
| Inspect a particular running service | The relevant service shell or workbench |

Keep the base-station terminal open while using the browser editor. A command's availability does not make it a base-station command: `dts`, base-station credentials, and the base station's network path remain outside the editor environment. For local notebooks, use an ordinary Linux terminal, the development environment provided for this LX, or the [Duckietown Workspace](https://github.com/duckietown/workspace). A dedicated development environment is optional unless the setup documentation for your learning environment requires it.

### Linux foundations and local practice

The shell commands in Notebooks [1](./notebooks/1-linux-foundations-and-distributions.ipynb) through [12](./notebooks/12-shell-exercises-and-output-verification.ipynb) run in any of those local Linux environments. They need a terminal and the LX files only; no Duckiedrone or network access is required. Interactive checkpoints require the notebook metadata supplied by `dts code editor`; a compatible Jupyter/IPython kernel with `ipywidgets` available is not sufficient by itself.

### Networking

Notebooks [13](./notebooks/13-network-addressing-and-routing.ipynb) through [17](./notebooks/17-network-names-and-service-discovery.ipynb) are conceptual. [Notebook 18](./notebooks/18-network-diagnostics-and-testing.ipynb)'s localhost examples are safe in the local Linux environment you chose. Run `dts fleet discover` and checks that need the base station's network path from the separate base-station terminal. Once `ssh` or `dts duckiebot virtual connect` opens a Duckiedrone shell, `localhost`, processes, routes, and sockets describe that Duckiedrone rather than the editor or base station.

### Authorized device access

Notebooks [19](./notebooks/19-physical-duckiedrone-ssh-access.ipynb) through [22](./notebooks/22-duckiedrone-process-inspection.ipynb) require either an authorized physical Duckiedrone or an authorized virtual Duckiedrone. Physical access also needs a network path authorized by its owner or administrator and a verified SSH identity. Virtual access uses the Duckietown Shell's local virtual Duckiedrone workflow. Filesystem and process inspection starts only after one authorized device shell is open.

You can complete local work independently. For physical-device or network activity, use only equipment and networks you own or are explicitly authorized to administer. Follow the device owner's documentation and the network-administration policy, and contact the device owner, network administrator, or another designated support contact when you need help.

## Complete the Linux shell exercises

Starter files are in `packages/shell_exercises/`. Work from the LX root, edit the files described in the Shell Exercises and Output Verification notebook, and check their syntax with:

```bash
python3 -m py_compile packages/shell_exercises/*.py
bash -n packages/shell_exercises/hello.sh
```

The notebooks explain how to run each completed script with input from the terminal or a pipe.

## Further reading

See the [GNU's Not Unix (GNU) Bash Reference Manual](https://www.gnu.org/software/bash/manual/), the [Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html), and the Internet Engineering Task Force (IETF) [IPv6 specification (Request for Comments (RFC) 8200)](https://www.rfc-editor.org/rfc/rfc8200).

## For LX authors

Learner material is in `notebooks/` and `packages/`. Structural checks are in `tests/`, and the exercise image recipe is maintained in the paired `lx-dd-linux-and-networking-recipe` repository. Run the structural checks from the LX root:

```bash
python3 -m pytest tests/
```
