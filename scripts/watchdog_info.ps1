echo "Password is 'admin'"
& docker-compose run --rm utility pcp_watchdog_info -U admin -h pgpool
