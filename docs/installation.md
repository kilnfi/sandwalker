# Installation Guide

This guide explains how to set-up your own stack of the Sandwalker.

## Requirements

You need:

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

First, create a directory that will be used by the Pocket node as a
data directory (both for the blockchain and the Sandwalker database):

```
git clone https://github.com/skillz-blockchain/sandwalker.git
cd sandwalker/infra
mkdir data
sudo chown -R 1005 data
sudo chmod -R 775 data
```

Edit the configuration so that the `VIRTUALHOST` environment variable
points to the virtualhost you want:

```
$EDITOR docker-compose.yml    # edit VIRTUALHOST=<you_hostname>
```

Build and run:

```
docker-compose build
docker-compose up -d
```

After a couple of seconds, you should have:

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
