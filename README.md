# CtrlBnchMrk: SDN Controller Benchmarking Platform

An automated platform for benchmarking the **performance and scalability of open-source SDN controllers**, built on the IETF benchmarking methodology for SDN controllers (draft-ietf-bmwg-sdn-controller-benchmark, later published as [RFC 8456](https://datatracker.ietf.org/doc/rfc8456/)).

The platform runs each controller, the traffic generator and the emulated network in separate Docker containers. It builds Mininet topologies of different sizes, drives OpenFlow load, captures southbound traffic with tshark, and turns the captures into metrics and plots.

> **Published at IEEE ICSPCS 2019**
> A. M. Diaz Tello and M. Abolhasan, "SDN Controllers Scalability and Performance Study," *2019 13th International Conference on Signal Processing and Communication Systems (ICSPCS)*, Gold Coast, Australia, 2019.
> DOI: [10.1109/ICSPCS47537.2019.9008462](https://ieeexplore.ieee.org/document/9008462) · [Conference proceedings](https://ieeexplore.ieee.org/xpl/conhome/8977248/proceeding)

Developed in 2018 as part of an MSc in Internetworking at the University of Technology Sydney (UTS).

---

## Highlights

- **Six controllers benchmarked:** ONOS, OpenDaylight (Boron), Ryu, Floodlight, OpenMUL and POX.
- **Six IETF metrics automated:** from asynchronous message latency and throughput up to the largest network a controller can discover.
- **Containerised testbed:** each controller, Cbench and Mininet runs in its own Docker container on an isolated bridge network, so you can swap controllers with one command.
- **Topology generator:** builds linear, tree (hub and spoke), spine-leaf and datacenter topologies in Mininet, with a scale factor to deploy several copies at once.
- **Packet-level measurement:** live tshark dissection of OpenFlow 1.0/1.3 messages (`FEATURES_REPLY`, `PACKET_IN` with LLDP, `PORT_STATUS`, `FLOW_MOD`) gives timestamps for switch discovery, link discovery and path setup.
- **Resource monitoring:** collects controller container CPU and memory through the Docker API while tests run.
- **Plotting pipeline:** matplotlib and pandas scripts turn the CSV results into the figures used in the paper.

## Architecture

<p align="center">
  <img src="doc/HLD%20Architecture.png" alt="High-level architecture" width="380">
</p>

| Component | Role |
|---|---|
| **Ruler** (`bin/ruler.sh`) | Orchestrator on the host. Deploys containers, sets up the environment and starts tests. |
| **Controller container** | The controller being tested (fixed IP `10.0.1.10`, OpenFlow on port 6633/6653). |
| **Cbench container** | Emulates switches and floods `PACKET_IN` messages to measure latency and throughput. |
| **Mininet container** | Emulates Open vSwitch topologies that connect to the controller. |
| **Benchmark scripts** (`ctrlbnchmrk/`) | Capture OpenFlow traffic on the Docker bridge, compute the metrics and log CSV results. |

The paper's reference testbed was a Dell R740 (Xeon E5-2420 v2, 6 cores / 12 threads, 32 GB RAM) running Ubuntu 14.04.

## Benchmarks

| # | Metric (IETF) | Category | How it is measured |
|---|---|---|---|
| 1 | Asynchronous Message Processing Time | Performance | Cbench latency mode |
| 2 | Asynchronous Message Processing Rate | Performance | Cbench throughput mode (`-t`) |
| 3 | Network Topology Discovery Time | Scalability | Time from the first `FEATURES_REPLY` to the last LLDP `PACKET_IN` |
| 4 | Reactive Path Provisioning Time | Performance | Time from the ARP `PACKET_IN` until all expected `FLOW_MOD (ADD)` messages are seen |
| 5 | Network Topology Change Detection Time | Performance | Time from a simulated link failure (`PORT_STATUS`) until re-discovery |
| 6 | Network Discovery Size | Scalability | Largest linear topology that stays stable for 5 minutes (+100 switches per step) |

## Key findings

- **OpenMUL** (C) had the highest raw throughput and latency in Cbench, at about 80K flows/s in latency mode (~12.5 µs per `PACKET_IN`).
- **ONOS** was the most consistent controller overall, with the best result in 5 of 6 tests. It also discovered the largest stable network (700 switches).
- **Ryu** discovered small topologies fastest but was limited by single-threaded execution. It became unresponsive above 500 switches and could not forward traffic on topologies with redundant links.
- **Floodlight** does not set the OpenFlow 1.3 `PACKET_IN` *reason* field correctly (`OFPR_NO_MATCH` instead of `OFPR_ACTION` for LLDP). This slowed its topology change detection.
- **OpenDaylight's** L2Switch forwards traffic without installing flow paths. This slowed discovery and broke forwarding between isolated networks.

See the paper for the full results and discussion.

## Repository layout

```
bin/ruler.sh                  Orchestrator: deploy, run tests, tear down
docker/docker-compose.yml     Controller, Cbench and Mininet services on a 10.0.1.0/24 bridge
etc/config.py                 Test parameters (controller IP/port, Cbench, OpenFlow constants, scale)
ctrlbnchmrk/                  Benchmark implementations
  cbench_perf_test.py           Tests 1 & 2 (Cbench throughput/latency)
  network_topology_discovery*.py Test 3 (OF 1.0 and OF 1.3 variants)
  4_reactive_path_prov_time.py  Test 4
  5_network_topology_change_detection_time.py  Test 5
  lib/                          tshark capture logging, Docker stats, Mininet helpers
mininet_topo_builder/         Mininet launcher and topology definitions
  topologies/                   linear, tree, spineleaf, datacenter, switches
plot/                         Plotting scripts for the paper figures
doc/PerformanceTests/         Raw CSV results from the published experiments
tests/                        Reference OpenFlow packet captures (ODL, Ryu; OF 1.0/1.3)
```

## Usage

The platform expects to live at `/opt/ctrlbnchmrk` on a Linux host with Docker, docker-compose and tshark installed. The controller images are published on Docker Hub (`mauriciodtdt/odl`, `mauriciodtdt/onos`, `mauriciodtdt/floodlight`, `mauriciodtdt/pox`, `mauriciodtdt/cbench`, `mauriciodtdt/mininet`). Ryu and OpenMUL use their community images.

```bash
# Deploy a controller (odl | onos | ryu | floodlight | openmul | pox) with Mininet
./bin/ruler.sh -D onos

# Smoke test: 3-switch linear topology against the controller
./bin/ruler.sh -t onos

# Run a benchmark: ./bin/ruler.sh -T <controller> <test#> [test args]
./bin/ruler.sh -T onos 1                                     # Cbench latency
./bin/ruler.sh -T onos 2                                     # Cbench throughput
./bin/ruler.sh -T onos 3 spineleaf ...                       # Topology discovery time
./bin/ruler.sh -T onos 4 <src_mac> <dst_mac> linear 30 5     # Reactive path provisioning

# Clean Mininet / tear everything down
./bin/ruler.sh -c onos
./bin/ruler.sh -k onos
```

Test parameters such as switch and MAC counts, loop counts and scan time are set in `etc/config.py`. Results are written as CSV files to `/opt/ctrlbnchmrk/data/`.

## Tech stack

Python · Docker / docker-compose · Mininet · Open vSwitch · OpenFlow 1.0/1.3 · Cbench · tshark/Wireshark · pandas · matplotlib · Bash

> **Note:** This is research code from 2018 and is kept here as a record of the published work. It targets Python 2.7 and Ubuntu 14.04-era tooling, so it would need updating to run on a modern stack.

## Author

**Alvaro Mauricio Diaz Tello**, MSc in Internetworking, University of Technology Sydney
Supervisor: Prof. Mehran Abolhasan
