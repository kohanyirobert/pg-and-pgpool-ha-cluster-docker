from sys import argv
from hashlib import md5
from os import path, makedirs, remove
from shutil import rmtree
from datetime import datetime
from subprocess import check_output, PIPE
from random import randint
from jinja2 import Template


class Context:

  def __init__(self):
    self.number_of_nodes = 3
    self.postgres_password = 'admin'
    self.admin_username = 'admin'
    self.admin_password = 'admin'
    self.custom_username = 'admin'
    self.custom_password = 'admin'
    self.custom_database = 'admin'
    self.all_node_ids = tuple(range(self.number_of_nodes))
    self.subnet = '192.168.0.0/24'
    self.backend_ips = [f'192.168.0.1{x}' for x in self.all_node_ids]
    self.pool_ips = [f'192.168.0.2{x}' for x in self.all_node_ids]
    self.delegate_ip = '192.168.0.200'


def pool_passwd_md5(username, password):
  return md5(f'{password}{username}'.encode("utf8")).hexdigest()


def pcp_conf_md5(password):
  return md5(password.encode("utf8")).hexdigest()


def with_template(template_path, output_path, **kwargs):
  with open(template_path, mode='r', encoding='utf8', newline='\n') as f:
    template = Template(f.read())
  makedirs(path.dirname(output_path), exist_ok=True)
  with open(output_path, mode='w', encoding='utf8', newline='\n') as f:
    f.write(template.render(kwargs))


def generate_dotenv(ctx):
  with_template('./templates/.env.j2', './.env',
    primary_node_id=ctx.all_node_ids[0],
    all_node_ids=ctx.all_node_ids,
    postgres_password=ctx.postgres_password,
    custom_username=ctx.custom_username,
    custom_password=ctx.custom_password,
    custom_database=ctx.custom_database,
  )


def generate_pgpool_conf(ctx):
  for node_id in ctx.all_node_ids:
    other_node_ids = [x for x in ctx.all_node_ids if x != node_id]
    with_template('./templates/pgpool.conf.j2', f'./out/pgpool-{node_id}/pgpool.conf',
      all_node_ids=ctx.all_node_ids,
      primary_node_id=node_id,
      other_node_ids=other_node_ids,
      delegate_ip=ctx.delegate_ip,
      custom_username=ctx.custom_username,
      custom_password=ctx.custom_password,
      custom_database=ctx.custom_database,
    )


def generate_pool_hba_conf(ctx):
  for node_id in ctx.all_node_ids:
    with_template('./templates/pool_hba.conf.j2', f'./out/pgpool-{node_id}/pool_hba.conf',
      custom_username=ctx.custom_username,
    )


def generate_pool_passwd(ctx):
  for node_id in ctx.all_node_ids:
    with_template('./templates/pool_passwd.j2', f'./out/pgpool-{node_id}/pool_passwd',
      all_node_ids=ctx.all_node_ids,
      postgres_md5=pool_passwd_md5('postgres', ctx.postgres_password),
      custom_username=ctx.custom_username,
      custom_md5=pool_passwd_md5(ctx.custom_username, ctx.custom_password),
    )


def generate_pcp_conf(ctx):
  for node_id in ctx.all_node_ids:
    with_template('./templates/pcp.conf.j2', f'./out/pgpool-{node_id}/pcp.conf',
      admin_username=ctx.admin_username,
      admin_md5=pcp_conf_md5(ctx.admin_password),
    )

def generate_pgpool_pool_id(ctx):
  for node_id in ctx.all_node_ids:
    with_template('./templates/pgpool_node_id.j2', f'./out/pgpool-{node_id}/pgpool_node_id',
      node_id=node_id,
    )

def generate_docker_compose_yml(ctx):
  with_template('./templates/docker-compose.yml.j2', f'./docker-compose.yml',
      all_node_ids=ctx.all_node_ids,
      delegate_ip=ctx.delegate_ip,
      subnet=ctx.subnet,
      backend_ips=ctx.backend_ips,
      pool_ips=ctx.pool_ips,
    )


def main(ctx):
  generate_dotenv(ctx)
  generate_pgpool_conf(ctx)
  generate_pool_hba_conf(ctx)
  generate_pool_passwd(ctx)
  generate_pcp_conf(ctx)
  generate_pgpool_pool_id(ctx)
  generate_docker_compose_yml(ctx)


if __name__ == '__main__':
  ctx = Context()
  if ctx.number_of_nodes < 0 or ctx.number_of_nodes > 9:
    raise ValueError()
  main(ctx)
