# Phase 2 - Endpoint

## Overview
Isolated Windows endpoint provisioned on wardenix-lab internal network,
verified network boundaries, and registered to Entra ID.

## Configuration
- VM: Tiny10 (lightweight Windows 10 build) on VirtualBox
- Network: Dual-NIC - Ethernet 1 (NAT, 10.0.2.15) for Entra/Wazuh phone-home,
  Ethernet 2 (wardenix-lab internal, 10.10.10.20) for isolated attack surface
- Entra device join: completed as Wale Ibrahim (AzureAD\WaleIbrahim)
- Device name: DESKTOP-K8PDBGH
- Wazuh agent: installed and deferred registration to Phase 3 (required live manager)

## Network boundary verification
- Clipboard sharing: disabled
- Shared folders: disabled
- Drag-and-drop: disabled
- Host machine confirmed unreachable from wardenix-lab network

## Evidence
- docs/screenshots/phase-2-entra-device-joined.png
