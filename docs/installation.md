/[WIP]: This documentation is not yet aligned with the current implementation./

# Installation Guide

This guide explains how to set-up your own stack of the Sandwalker.

## Requirements

You need:

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

The Sandwalker is ready-to-deploy using Docker Compose:

```
cd infra
docker-compose build
docker-compose up -d
```

After a couple of minutes, you should have:

- the frontend listening locally on port `5000`,
- an instrumentalized Pocket node synchronizing from block 0.

It takes 3-4 days for the Pocket node to synchonize with the
network. This step is necessary to fill up the Sandwalker database
with data coming from the blockchain. Once synchronized, the Pocket
node will continue catching up with the network as any other node,
providing real-time data of rewards from the Pocket network.

## Monitoring

Current block height is displayed on the homepage of the Sandwalker
and can be used to monitor at which block the Pocket node is
synchronized.
