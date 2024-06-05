# About

Example of running a multi-node PostgreSQL database cluster with one read-write master and multiple read-only slaves behind a multi-node Pgpool-II cluster distributing read operations between read-only slaves with high-availability.

Based on this [tutorial](
https://www.pgpool.net/docs/latest/en/html/example-cluster.html).

## Notes

* The `docker-compose.yml` is generated via `./scripts/generate.py`.
* After the Docker ecosystem is running nodes are available via the following hostnames
  * PostgreSQL nodes: `pg-0`, `pg-1`, `pg-2`
  * Pgpool-II nodes: `pgpool-0`, `pgpool-1`, `pgpool-2` and most importantly **the floating/virtual IP managed by the nodes will point to `pgpool`**.
* By default three Pgpool-II is needed at least to achieve HA, since [with only two nodes when one disappears from the cluster the quorum won't exist](https://www.pgpool.net/docs/latest/en/html/runtime-watchdog-config.html#CONFIG-WATCHDOG-VIP-CONTROL).
* Pgpool-II's `pool_passwd` must contain the necessary credentials when using `scram-sha-256` authentication. See why in [`pgpool`'s documentation](https://www.pgpool.net/docs/latest/en/html/auth-pool-hba-conf.html).
* Pgpool-II's `pool_passwd` and `pcp.conf` files contains user/password in similar fashion, but the actual format is different (and this still uses `md5`)
* Fortunately creation of these file are handled by `bitnami/pgpool`
* The `Dockerfile` that customizes `bitnamie/pgpool` uses `root` to install a few things, `sudo` to allow UID 1001 to use `ip` and `arping` (so that failover nodes could take over the floating IP)
* **However everything else must run with UID 1001**, otherwise everything will be `root`'s, which is problematic, since he Pgpool-II process runs under 1001 either way, and this causes errors (e.g. auth erro, since the process access pool_passwd)
* Also, setting `CAP_NET_ADMIN` in the `docker-compose.yml` is important, since otherwise Pgpool-II processes couldn't use `ip` or other commands during a failover
* Using `useradd` in the `Dockerfile` is also important, since this allows us to use the `sudoers` file, because UID 1001 need to have a username in order to be referenced in `sudoers`
* To run `pcp` commands the command needs `-W` to ask for passwords, `PGPASSWORD` is ignored and by default no password is asked
* Also, to be able to connect via the floating IP Pgpool-II needs to listen for `pcp` commands on all interfaces (`pcp_listen_addresses = '*'`)
* When a PostgreSQL node disappears from the cluster and comes back online it needs to be reattached to the Pgpool-II pool(s) (it's status will be *down*). Use `pcp_attach_node` to reattach the node.
* **When a new PostgreSQL node becomes primary other nodes go down**. Nodes needs to be restarted using a different value for the `REPMGR_PRIMARY_HOST` environment variable, e.g. if the new primary node is `1` then `REPMGR_PRIMARY_HOST` should equal `pg-1`, in short nodes need to be reconfigured and restarted.

## Running

This starts up the cluster and generates several files.
By default **there are 3 PostgreSQL and 3 Pgpool-II nodes in the clusters**.

```ps1
pip install pipenv
pipenv shell
pipenv install
.\scripts\up.ps1
```

**It may take some time for nodes to settle down**.
To see exactly what kind of files are being generated look at `./templates`, but **be sure to look at `.env` and `docker-compose.yml`**.

This displays the status of the PostgreSQL backends.

```ps1
.\scripts\pool_nodes.ps1
```

This displays the status of the Pgpool-II cluster.

```ps1
.\scripts\watchdog_info.ps1
```

Use this command to execute an SQL command through the master Pgpool-II node.

```ps1
.\scripts\psql.ps1 "select 1"
```

This stops PostgreSQL/Pgpool-II nodes to see how the clusters respond to outages.

```ps1
docker-compose stop pg-0     # stops the first PostgreSQL node
docker-compose stop pgpool-2 # stops the last Pgpool-II node
```

To check how nodes are doing.

```ps1
docker-compose logs --follow pg-1
docker-compose logs --follow pgpool-3
```

This stops the cluster and cleans up every generated files.

```ps1
.\scripts\down.ps1
```
