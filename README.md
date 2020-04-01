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
* Pgpool-II's `pool_passwd` must contain the necessary credentials when using `md5` authentication. See why in [`pgpool`'s documentation](https://www.pgpool.net/docs/latest/en/html/auth-pool-hba-conf.html) - read `auth_method`, `md5`.
* Pgpool-II's `pool_passwd` and `pcp.conf` files contains user/password in similar fashion, but the actual format is different
  * [`pool_passwd`'s format](https://www.pgpool.net/docs/latest/en/html/pg-md5.html): `username:md5`*`<md5 hash of passwordusername concatenated together>`*
  * [`pcp.conf`'s format](https://www.pgpool.net/docs/latest/en/html/configuring-pcp-conf.html#CONFIGURING-PCP-CONF): `username:`*`<md5 hash of password>`*
* When a PostgreSQL node disappears from the cluster and comes back online it needs to be reattached to the Pgpool-II pool(s) (it's status will be *down*). Use `pcp_attach_node` to reattach the node.
* **When a new PostgreSQL node becomes primary other nodes go down**. Nodes needs to be restarted using a different value for the `REPMGR_PRIMARY_HOST` environment variable, e.g. if the new primary node is `1` then `REPMGR_PRIMARY_HOST` should equal `pg-1`, in short nodes need to be reconfigured and restarted.

## Running

This starts up the cluster and generates several files.
By default **there are 3 PostgreSQL and 3 Pgpool-II nodes in the clusters**.

```ps1
pip install pipenv
pipenv shell
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
