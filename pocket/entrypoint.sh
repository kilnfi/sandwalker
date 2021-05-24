#!/usr/bin/env bash

function create_account_if_needed {
    if [ ! -f /home/app/.pocket/node_key.json ]
    then
	pocket accounts create
    fi
}

create_account_if_needed

# Exec is important here, we want to replace the current bash process
# so pocket keeps 1 as a PID within the container (so that signals are
# properly propagated).

exec pocket start \
     --mainnet \
     --seeds \
     03b74fa3c68356bb40d58ecc10129479b159a145@seed1.mainnet.pokt.network:20656,64c91701ea98440bc3674fdb9a99311461cdfd6f@seed2.mainnet.pokt.network:21656
