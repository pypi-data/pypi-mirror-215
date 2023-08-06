#!/usr/bin/env python
# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------------
# | Copyright (C) 2016 Yunify, Inc.
# +-------------------------------------------------------------------------
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this work except in compliance with the License.
# | You may obtain a copy of the License in the LICENSE file, or at:
# |
# | http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.
# +-------------------------------------------------------------------------

# DO NOT EDIT!
# This code is generated with snips tool
# using python-spec-tmpl template

import time
import yaml
import sys
import click
import json
from qingcloud_hpc.config import Config
from qingcloud_hpc.sdk_api.hpc import Hpc

api = None
ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
client_conf = "../conf/client.yaml"


@click.group()
@click.option('--config', default='../conf/client.yaml')
def root(**kwargs):
    config = Config()
    config.load_config_from_filepath(kwargs['config'])
    global api
    api = Hpc(config)


@root.command()
@click.option('--cpu_core_num', type=str, help='the simulation job cpu')
@click.option(
    '--duration',
    type=int,
    help=
    '[paid period (Month), valid only when production paid type is Reserved].')
@click.option('--paid_type',
              required=True,
              type=str,
              help='[production paid type].')
@click.option('--plan_name',
              type=str,
              help='[the name of remote application if exist]')
@click.option('--prod_name',
              required=True,
              type=str,
              help='[new billing production name].')
@click.option('--queue_type',
              type=str,
              help='[queue type, valid only when queue is private queue].')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cost(**kwargs):
    resp = api.get_cost(kwargs['cpu_core_num'], kwargs['duration'],
                        kwargs['paid_type'], kwargs['plan_name'],
                        kwargs['prod_name'], kwargs['queue_type'],
                        kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--aggregation', required=True, type=str, help='aggregation')
@click.option('--end_time', required=True)
@click.option('--instance_id',
              required=True,
              type=str,
              help='product instance id')
@click.option('--metering_period',
              required=True,
              type=str,
              help='metering period')
@click.option('--meters')
@click.option('--start_time', required=True)
@click.option('--time_zone', required=True, type=str, help='time_zone')
@click.option('--timestamp', required=True)
def get_meter(**kwargs):
    resp = api.get_meter(
        kwargs['aggregation'], kwargs['end_time'], kwargs['instance_id'],
        kwargs['metering_period'],
        json.loads(kwargs['meters']) if kwargs['meters'] else None,
        kwargs['start_time'], kwargs['time_zone'], kwargs['timestamp'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--prod_name',
              required=True,
              type=str,
              help='[new billing production name].')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_product_billing_model(**kwargs):
    resp = api.get_product_billing_model(kwargs['prod_name'],
                                         kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--app_name', type=str, help='the app name to filter')
@click.option('--app_state', type=str, help='the app state to filter')
@click.option('--app_user_id',
              type=str,
              help='the id of user who use the app, from boss need')
@click.option('--duration_max',
              type=int,
              help='Maximum duration of app usage period for search')
@click.option('--duration_min',
              type=int,
              help='Minimum duration of app usage period for search,')
@click.option('--end_time')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='whether sort by sort_key reverse')
@click.option('--sort_key', type=str, help='sort by sort_key')
@click.option('--start_time')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_remoteapp_log(**kwargs):
    resp = api.list_remoteapp_log(
        kwargs['app_name'], kwargs['app_state'], kwargs['app_user_id'],
        kwargs['duration_max'], kwargs['duration_min'], kwargs['end_time'],
        kwargs['limit'], kwargs['offset'], kwargs['reverse'],
        kwargs['sort_key'], kwargs['start_time'], kwargs['timestamp'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--access_sys_id',
              required=True,
              type=str,
              help='access system id')
@click.option('--event', required=True, type=str, help='notify event')
@click.option('--occurred_at', required=True)
@click.option('--prod_inst_id_ext',
              required=True,
              type=str,
              help='product instance id')
@click.option('--user_id',
              required=True,
              type=str,
              help='user id, such as admin')
@click.option('--zone', type=str, help='zone id')
def notify(**kwargs):
    resp = api.notify(kwargs['timestamp'], kwargs['access_sys_id'],
                      kwargs['event'], kwargs['occurred_at'],
                      kwargs['prod_inst_id_ext'], kwargs['user_id'],
                      kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--access_sys_id',
              required=True,
              type=str,
              help='access system id')
@click.option('--event', required=True, type=str, help='notify event')
@click.option('--occurred_at', required=True)
@click.option('--prod_inst_id_ext',
              required=True,
              type=str,
              help='product instance id')
@click.option('--user_id',
              required=True,
              type=str,
              help='user id, such as admin')
@click.option('--zone', type=str, help='zone id')
def remoteapp_notify(**kwargs):
    resp = api.remoteapp_notify(kwargs['timestamp'], kwargs['access_sys_id'],
                                kwargs['event'], kwargs['occurred_at'],
                                kwargs['prod_inst_id_ext'], kwargs['user_id'],
                                kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cmd', type=str, help='the hpc command to be execute')
@click.option('--dispatcher', type=str, help='the hpc dispacther to be used')
@click.option('--ip', type=str, help='the cli agent ip address')
@click.option('--user', type=str, help='the cluster_id of hpc cluster')
@click.option('--zone', type=str, help='zone id')
def run_cmd(**kwargs):
    resp = api.run_cmd(kwargs['timestamp'], kwargs['cmd'],
                       kwargs['dispatcher'], kwargs['ip'], kwargs['user'],
                       kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--node_count', type=str, help='the cluster node count')
@click.option('--node_name',
              type=str,
              help='the ID of cluster you want to add new nodes')
@click.option('--node_role', type=str, help='the cluster node role type')
@click.option('--private_ips')
@click.option('--resource_conf',
              type=str,
              help='the cluster node role resource conf')
@click.option('--zone', required=True, type=str, help='zone id')
def add_cluster_nodes(**kwargs):
    resp = api.add_cluster_nodes(
        kwargs['timestamp'], kwargs['cluster_id'], kwargs['node_count'],
        kwargs['node_name'], kwargs['node_role'],
        json.loads(kwargs['private_ips']) if kwargs['private_ips'] else None,
        kwargs['resource_conf'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              type=str,
              help='the ID of cluster you want to add new nodes')
@click.option('--node_count', type=str, help='the cluster node count')
@click.option('--node_name',
              type=str,
              help='the ID of cluster you want to add new nodes')
@click.option('--node_role', type=str, help='the cluster node role type')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def add_cluster_nodes_fee(**kwargs):
    resp = api.add_cluster_nodes_fee(kwargs['cluster_id'],
                                     kwargs['node_count'], kwargs['node_name'],
                                     kwargs['node_role'], kwargs['timestamp'],
                                     kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='')
@click.option('--cluster_node', required=True, type=str, help='')
@click.option('--eip_id', required=True, type=str, help='')
@click.option('--zone', required=True, type=str, help='zone id')
def associate_login_node_eip(**kwargs):
    resp = api.associate_login_node_eip(kwargs['timestamp'],
                                        kwargs['cluster_id'],
                                        kwargs['cluster_node'],
                                        kwargs['eip_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--charge_mode', type=str, help='The hpc cluster id')
@click.option('--cluster_conf')
@click.option('--cluster_name', type=str, help='The hpc cluster id')
@click.option('--cluster_type', type=str, help='The hpc cluster type')
@click.option('--deploy_mode',
              type=str,
              help='The hpc cluster deployment mode')
@click.option(
    '--duration',
    type=int,
    help='if paid_type is Reserved, Set the duration period is required')
@click.option('--is_auto_renewal',
              type=int,
              help='if paid_type is Reserved, auto renew is required')
@click.option('--owner', required=True, type=str, help='cluster owner')
@click.option('--zone', required=True, type=str, help='zone id')
def create_cluster(**kwargs):
    resp = api.create_cluster(kwargs['timestamp'], kwargs['charge_mode'],
                              kwargs['cluster_conf'], kwargs['cluster_name'],
                              kwargs['cluster_type'], kwargs['deploy_mode'],
                              kwargs['duration'], kwargs['is_auto_renewal'],
                              kwargs['owner'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_ids', required=True)
@click.option('--run_user',
              required=True,
              type=str,
              help='the run_user of hpc cluster')
@click.option('--unlease', type=str, help='if ')
@click.option('--zone', required=True, type=str, help='zone id')
def delete_cluster(**kwargs):
    resp = api.delete_cluster(
        kwargs['timestamp'],
        json.loads(kwargs['cluster_ids']) if kwargs['cluster_ids'] else None,
        kwargs['run_user'], kwargs['unlease'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--node_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def delete_cluster_nodes(**kwargs):
    resp = api.delete_cluster_nodes(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['node_ids']) if kwargs['node_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='')
@click.option('--eip_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def dissociate_login_node_eip(**kwargs):
    resp = api.dissociate_login_node_eip(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['eip_ids']) if kwargs['eip_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_type', type=str, help='cluster type HPC or EHPC')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_conf(**kwargs):
    resp = api.get_cluster_conf(kwargs['cluster_type'], kwargs['timestamp'],
                                kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='the cluster_id of hpc cluster')
@click.option('--health_status', type=str, help='the node status')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--node_role', type=str, help='cluster node role')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status', type=str, help='status of the cluster nodes')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_nodes(**kwargs):
    resp = api.get_cluster_nodes(kwargs['cluster_id'], kwargs['health_status'],
                                 kwargs['limit'], kwargs['node_role'],
                                 kwargs['offset'], kwargs['reverse'],
                                 kwargs['search_word'], kwargs['sort_key'],
                                 kwargs['status'], kwargs['timestamp'],
                                 kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_ids', required=True)
@click.option('--owner', type=str, help='the cluster owner')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_hpc_cluster_detail(**kwargs):
    resp = api.get_hpc_cluster_detail(
        json.loads(kwargs['cluster_ids']) if kwargs['cluster_ids'] else None,
        kwargs['owner'], kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--search_word', type=str, help='search_word')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_nas_info(**kwargs):
    resp = api.get_nas_info(kwargs['cluster_id'], kwargs['search_word'],
                            kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='the cluster_id of hpc cluster')
@click.option('--cluster_type', type=str, help='The hpc cluster type')
@click.option('--end_time')
@click.option('--iam_cluster_ids',
              type=str,
              help='the cluster_ids of hpc cluster')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='cluster owner')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--shared_status',
              type=str,
              help='The hpc cluster shared status')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--start_time')
@click.option('--status', type=str, help='status of the cluster nodes')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_cluster(**kwargs):
    resp = api.list_cluster(kwargs['cluster_id'], kwargs['cluster_type'],
                            kwargs['end_time'], kwargs['iam_cluster_ids'],
                            kwargs['limit'], kwargs['offset'], kwargs['owner'],
                            kwargs['reverse'], kwargs['run_user'],
                            kwargs['search_word'], kwargs['shared_status'],
                            kwargs['sort_key'], kwargs['start_time'],
                            kwargs['status'], kwargs['timestamp'],
                            kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--cluster_name', type=str, help='the name of hpc cluster')
@click.option('--description', type=str, help='the description of hpc cluster')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_cluster(**kwargs):
    resp = api.modify_cluster(kwargs['timestamp'], kwargs['cluster_id'],
                              kwargs['cluster_name'], kwargs['description'],
                              kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--node_id',
              required=True,
              type=str,
              help='the description of hpc cluster')
@click.option('--node_name',
              required=True,
              type=str,
              help='the name of hpc cluster')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_cluster_node(**kwargs):
    resp = api.modify_cluster_node(kwargs['timestamp'], kwargs['cluster_id'],
                                   kwargs['node_id'], kwargs['node_name'],
                                   kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of this hpc cluster')
@click.option('--cpu', type=str, help='node cpu')
@click.option('--gpu', type=str, help='node gpu')
@click.option('--instance_class', type=str, help='the instance class')
@click.option('--memory', type=str, help='node memory in MB')
@click.option('--node_role', type=str, help='the role of node to resize')
@click.option('--storage_size',
              type=str,
              help='the storage size of cluster node in GB')
@click.option('--zone', required=True, type=str, help='zone id')
def resize_cluster(**kwargs):
    resp = api.resize_cluster(kwargs['timestamp'], kwargs['cluster_id'],
                              kwargs['cpu'], kwargs['gpu'],
                              kwargs['instance_class'], kwargs['memory'],
                              kwargs['node_role'], kwargs['storage_size'],
                              kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              type=str,
              help='the ID of cluster you want to add new nodes')
@click.option('--cpu', type=str, help='node cpu')
@click.option('--gpu', type=str, help='node gpu')
@click.option('--instance_class', type=str, help='the instance class')
@click.option('--memory', type=str, help='node memory in MB')
@click.option('--node_role', type=str, help='the role of node to resize')
@click.option('--storage_size',
              type=str,
              help='the storage size of cluster node in GB')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def resize_cluster_fee(**kwargs):
    resp = api.resize_cluster_fee(kwargs['cluster_id'], kwargs['cpu'],
                                  kwargs['gpu'], kwargs['instance_class'],
                                  kwargs['memory'], kwargs['node_role'],
                                  kwargs['storage_size'], kwargs['timestamp'],
                                  kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--node_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def restart_cluster_nodes(**kwargs):
    resp = api.restart_cluster_nodes(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['node_ids']) if kwargs['node_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_ids', required=True)
@click.option('--owner', type=str, help='owner')
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='zone id')
def resume_cluster(**kwargs):
    resp = api.resume_cluster(
        kwargs['timestamp'],
        json.loads(kwargs['cluster_ids']) if kwargs['cluster_ids'] else None,
        kwargs['owner'], kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def start_cluster(**kwargs):
    resp = api.start_cluster(
        kwargs['timestamp'],
        json.loads(kwargs['cluster_ids']) if kwargs['cluster_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def stop_cluster(**kwargs):
    resp = api.stop_cluster(
        kwargs['timestamp'],
        json.loads(kwargs['cluster_ids']) if kwargs['cluster_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--app_version', required=True, type=str, help='app version id')
@click.option('--clusters', required=True)
@click.option('--owner', type=str, help='')
@click.option('--zone', required=True, type=str, help='zone id')
def upgrade_cluster(**kwargs):
    resp = api.upgrade_cluster(
        kwargs['timestamp'], kwargs['app_version'],
        json.loads(kwargs['clusters']) if kwargs['clusters'] else None,
        kwargs['owner'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='the cluster id')
@click.option('--enable',
              required=True,
              type=int,
              help='enable: 1, disable: 0')
@click.option('--shared_dir', type=str, help='The epfs shared dir')
@click.option('--zone', type=str, help='zone id')
def enable_ehpc_subuser_stor(**kwargs):
    resp = api.enable_ehpc_subuser_stor(kwargs['timestamp'],
                                        kwargs['cluster_id'], kwargs['enable'],
                                        kwargs['shared_dir'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of ehpc cluster')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_ehpc_subuser_stor_enable_status(**kwargs):
    resp = api.get_ehpc_subuser_stor_enable_status(
        kwargs['cluster_id'], kwargs['limit'], kwargs['offset'],
        kwargs['run_user'], kwargs['timestamp'], kwargs['verbose'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of ehpc cluster')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--subuser_ids',
              type=str,
              help='the subuser ids of ehpc cluster')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_ehpc_subuser_stor(**kwargs):
    resp = api.list_ehpc_subuser_stor(kwargs['cluster_id'], kwargs['limit'],
                                      kwargs['offset'], kwargs['run_user'],
                                      kwargs['subuser_ids'],
                                      kwargs['timestamp'], kwargs['verbose'],
                                      kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--file_type',
              required=True,
              type=str,
              help='The type of job file')
@click.option('--file_value',
              required=True,
              type=str,
              help='The file content of job file')
@click.option('--target_file',
              required=True,
              type=str,
              help='The target file path and name of job file')
@click.option('--zone', required=True, type=str, help='zone id')
def create_job_file(**kwargs):
    resp = api.create_job_file(kwargs['timestamp'], kwargs['cluster_id'],
                               kwargs['file_type'], kwargs['file_value'],
                               kwargs['target_file'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--job_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def delete_jobs(**kwargs):
    resp = api.delete_jobs(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['job_ids']) if kwargs['job_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--job_uuid', required=True, type=str, help='ID of job')
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_job_detail(**kwargs):
    resp = api.get_job_detail(kwargs['job_uuid'], kwargs['cluster_id'],
                              kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--end_time', required=True)
@click.option('--job_id', required=True)
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--meters', required=True)
@click.option('--start_time', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_job_monitor(**kwargs):
    resp = api.get_job_monitor(kwargs['cluster_id'], kwargs['end_time'],
                               kwargs['job_id'], kwargs['limit'],
                               kwargs['meters'], kwargs['start_time'],
                               kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--cluster_type', type=str, help='in boss job list cluster_type')
@click.option('--end_time')
@click.option('--hpcjob_uuid', type=str, help='in the boss of hpcjob_uuid')
@click.option('--hpcqueue_id', type=str, help='job of queue')
@click.option('--iamuser_name', type=str, help='iamuser_name')
@click.option('--job_status', type=str, help='Job Status')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='job list owner')
@click.option('--queue_name', type=str, help='the queue name to filter')
@click.option('--reverse', type=int, help='whether sort by sort_key reverse')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word', type=str, help='the search key word')
@click.option('--sort_key', type=str, help='sort by sort_key')
@click.option('--start_time')
@click.option('--submit_type',
              type=int,
              help='[submit job type. 1:cli , 0:console]')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_jobs(**kwargs):
    resp = api.list_jobs(
        kwargs['cluster_id'], kwargs['cluster_type'], kwargs['end_time'],
        kwargs['hpcjob_uuid'], kwargs['hpcqueue_id'], kwargs['iamuser_name'],
        kwargs['job_status'], kwargs['limit'], kwargs['offset'],
        kwargs['owner'], kwargs['queue_name'], kwargs['reverse'],
        kwargs['run_user'], kwargs['search_word'], kwargs['sort_key'],
        kwargs['start_time'], kwargs['submit_type'], kwargs['timestamp'],
        kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--jobs', required=True)
@click.option('--last_usage_time',
              type=int,
              help='the last metric record time')
@click.option('--this_usage_time',
              type=int,
              help='the current metric record time')
@click.option('--zone', required=True, type=str, help='zone id')
def push_job_metrics(**kwargs):
    resp = api.push_job_metrics(
        kwargs['timestamp'],
        json.loads(kwargs['jobs']) if kwargs['jobs'] else None,
        kwargs['last_usage_time'], kwargs['this_usage_time'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--hpcjob_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def recover_job_status(**kwargs):
    resp = api.recover_job_status(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['hpcjob_ids']) if kwargs['hpcjob_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--job_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def resume_jobs(**kwargs):
    resp = api.resume_jobs(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['job_ids']) if kwargs['job_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--job_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def stop_jobs(**kwargs):
    resp = api.stop_jobs(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['job_ids']) if kwargs['job_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--cmd_line', type=str, help='The job command line')
@click.option('--core_limit', type=int, help='The job core limit')
@click.option('--hpcqueue_id', type=str, help='run job queue id')
@click.option('--input_file', type=str, help='The job input file path')
@click.option('--mem_limit', type=int, help='The job memory limit')
@click.option('--name', required=True, type=str, help='The job name')
@click.option('--resource_limit',
              type=str,
              help='The limit of resource used by job')
@click.option('--run_user',
              required=True,
              type=str,
              help='The run user of job file')
@click.option('--scheduler_queue_name', type=str, help='The job queue name')
@click.option('--stderr_redirect_path',
              type=str,
              help='The job stderr redirect path')
@click.option('--stdout_redirect_path',
              type=str,
              help='The job stdout redirect path')
@click.option('--time_limit', type=int, help='The job execution time limit')
@click.option('--zone', required=True, type=str, help='zone id')
def submit_job(**kwargs):
    resp = api.submit_job(
        kwargs['timestamp'], kwargs['cluster_id'], kwargs['cmd_line'],
        kwargs['core_limit'], kwargs['hpcqueue_id'], kwargs['input_file'],
        kwargs['mem_limit'], kwargs['name'], kwargs['resource_limit'],
        kwargs['run_user'], kwargs['scheduler_queue_name'],
        kwargs['stderr_redirect_path'], kwargs['stdout_redirect_path'],
        kwargs['time_limit'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--app_cluster_id',
              required=True,
              type=str,
              help='The cluster of job file')
@click.option('--data')
@click.option('--zone', required=True, type=str, help='zone id')
def update_ehpc_job_status(**kwargs):
    resp = api.update_ehpc_job_status(
        kwargs['timestamp'], kwargs['app_cluster_id'],
        json.loads(kwargs['data']) if kwargs['data'] else None, kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--job_events', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def update_job_status(**kwargs):
    resp = api.update_job_status(
        kwargs['timestamp'],
        json.loads(kwargs['job_events']) if kwargs['job_events'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def hello_world(**kwargs):
    resp = api.hello_world(kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--action_describe', type=str, help='job action describe')
@click.option('--directive', type=str, help='operation job directive')
@click.option('--end_time')
@click.option('--job_action', type=str, help='operation job_action')
@click.option('--job_ids', type=str, help='job ids')
@click.option('--jobs', type=str, help='operation jobs id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='operation job owner')
@click.option('--resource_ids', type=str, help='operation job resource_ids')
@click.option('--reverse', type=int, help='operation job reverse')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--start_time')
@click.option('--status', type=str, help='operation job status')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_operation(**kwargs):
    resp = api.list_operation(
        kwargs['action_describe'], kwargs['directive'], kwargs['end_time'],
        kwargs['job_action'], kwargs['job_ids'], kwargs['jobs'],
        kwargs['limit'], kwargs['offset'], kwargs['owner'],
        kwargs['resource_ids'], kwargs['reverse'], kwargs['search_word'],
        kwargs['start_time'], kwargs['status'], kwargs['timestamp'],
        kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--action_describe', type=str, help='job action describe')
@click.option('--directive', type=str, help='operation job directive')
@click.option('--end_time')
@click.option('--job_action', type=str, help='operation job_action')
@click.option('--job_ids', type=str, help='job ids')
@click.option('--jobs', type=str, help='operation jobs id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='operation job owner')
@click.option('--resource_ids', type=str, help='operation job resource_ids')
@click.option('--reverse', type=int, help='operation job reverse')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--start_time')
@click.option('--status', type=str, help='operation job status')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def simulation_operation(**kwargs):
    resp = api.simulation_operation(
        kwargs['action_describe'], kwargs['directive'], kwargs['end_time'],
        kwargs['job_action'], kwargs['job_ids'], kwargs['jobs'],
        kwargs['limit'], kwargs['offset'], kwargs['owner'],
        kwargs['resource_ids'], kwargs['reverse'], kwargs['search_word'],
        kwargs['start_time'], kwargs['status'], kwargs['timestamp'],
        kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--user_id', required=True, type=str, help='userId')
def disable_hpc(**kwargs):
    resp = api.disable_hpc(kwargs['timestamp'], kwargs['user_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--user_id', required=True, type=str, help='userId')
def enable_hpc(**kwargs):
    resp = api.enable_hpc(kwargs['timestamp'], kwargs['user_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--user_id', required=True, type=str, help='ID of user')
@click.option('--timestamp', required=True)
def get_hpc_status(**kwargs):
    resp = api.get_hpc_status(kwargs['user_id'], kwargs['timestamp'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--member_infos')
@click.option('--project_id',
              required=True,
              type=str,
              help='the id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def add_member(**kwargs):
    resp = api.add_member(
        kwargs['timestamp'],
        json.loads(kwargs['member_infos']) if kwargs['member_infos'] else None,
        kwargs['project_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_group_id',
              required=True,
              type=str,
              help='the rule group id of hpc project')
@click.option('--rule_id',
              required=True,
              type=str,
              help='the rule id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def add_project_rule(**kwargs):
    resp = api.add_project_rule(kwargs['timestamp'], kwargs['project_id'],
                                kwargs['rule_group_id'], kwargs['rule_id'],
                                kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--role_id',
              required=True,
              type=str,
              help='the role id of hpc project')
@click.option('--rule_group_id',
              required=True,
              type=str,
              help='the rule group id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def add_project_rule_group(**kwargs):
    resp = api.add_project_rule_group(kwargs['timestamp'],
                                      kwargs['project_id'], kwargs['role_id'],
                                      kwargs['rule_group_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--create_time')
@click.option('--description', type=str, help='The hpc cluster description')
@click.option('--enabled', type=int, help='The hpc cluster id')
@click.option('--owner', type=str, help='preject member owner')
@click.option('--project_id',
              required=True,
              type=str,
              help='The hpc project id')
@click.option('--resource_id',
              required=True,
              type=str,
              help='The hpc project resource id')
@click.option('--resource_type',
              type=str,
              help='The hpc project resource type')
@click.option('--status_time')
@click.option('--zone', required=True, type=str, help='zone id')
def add_resource(**kwargs):
    resp = api.add_resource(kwargs['timestamp'], kwargs['create_time'],
                            kwargs['description'], kwargs['enabled'],
                            kwargs['owner'], kwargs['project_id'],
                            kwargs['resource_id'], kwargs['resource_type'],
                            kwargs['status_time'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description', type=str, help='The hpc cluster description')
@click.option('--enabled', type=int, help='The hpc project enable status')
@click.option('--member_infos')
@click.option('--project_name', type=str, help='The hpc project name')
@click.option('--resource_id',
              required=True,
              type=str,
              help='The hpc project resource id')
@click.option('--zone', required=True, type=str, help='zone id')
def create_project(**kwargs):
    resp = api.create_project(
        kwargs['timestamp'], kwargs['description'], kwargs['enabled'],
        json.loads(kwargs['member_infos']) if kwargs['member_infos'] else None,
        kwargs['project_name'], kwargs['resource_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--create_time')
@click.option('--description', type=str, help='The hpc role description')
@click.option('--owner', type=str, help='preject role owner')
@click.option('--project_id',
              required=True,
              type=str,
              help='The hpc project id')
@click.option('--readonly',
              type=int,
              help='System role is readonly, can not del by api')
@click.option('--role_id', type=str, help='The hpc project role id')
@click.option('--role_name', type=str, help='The hpc project role name')
@click.option('--role_type', type=str, help='The hpc project role type')
@click.option('--status', type=str, help='The hpc role status')
@click.option('--status_time')
@click.option('--zone', required=True, type=str, help='zone id')
def create_project_role(**kwargs):
    resp = api.create_project_role(kwargs['timestamp'], kwargs['create_time'],
                                   kwargs['description'], kwargs['owner'],
                                   kwargs['project_id'], kwargs['readonly'],
                                   kwargs['role_id'], kwargs['role_name'],
                                   kwargs['role_type'], kwargs['status'],
                                   kwargs['status_time'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--create_time')
@click.option('--description', type=str, help='The hpc rule description')
@click.option('--owner', type=str, help='preject rule owner')
@click.option('--project_id',
              required=True,
              type=str,
              help='The hpc project id')
@click.option('--readonly',
              type=int,
              help='System rule is readonly, can not del by api')
@click.option('--rule_id',
              required=True,
              type=str,
              help='The hpc project rule id')
@click.option('--status', type=str, help='The hpc rule status')
@click.option('--status_time')
@click.option('--zone', required=True, type=str, help='zone id')
def create_project_rule(**kwargs):
    resp = api.create_project_rule(kwargs['timestamp'], kwargs['create_time'],
                                   kwargs['description'], kwargs['owner'],
                                   kwargs['project_id'], kwargs['readonly'],
                                   kwargs['rule_id'], kwargs['status'],
                                   kwargs['status_time'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--create_time')
@click.option('--description', type=str, help='The hpc rule group description')
@click.option('--owner', type=str, help='preject rule group owner')
@click.option('--project_id',
              required=True,
              type=str,
              help='The hpc project id')
@click.option('--readonly',
              type=int,
              help='System rule group is readonly, can not del by api')
@click.option('--rule_group_id',
              type=str,
              help='The hpc project rule group id')
@click.option('--status', type=str, help='The hpc rule group status')
@click.option('--status_time')
@click.option('--zone', required=True, type=str, help='zone id')
def create_project_rule_group(**kwargs):
    resp = api.create_project_rule_group(
        kwargs['timestamp'], kwargs['create_time'], kwargs['description'],
        kwargs['owner'], kwargs['project_id'], kwargs['readonly'],
        kwargs['rule_group_id'], kwargs['status'], kwargs['status_time'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--member_id', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def del_member(**kwargs):
    resp = api.del_member(
        kwargs['timestamp'],
        json.loads(kwargs['member_id']) if kwargs['member_id'] else None,
        kwargs['project_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_group_id',
              required=True,
              type=str,
              help='the rule group id of hpc project')
@click.option('--rule_id',
              required=True,
              type=str,
              help='the rule id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def del_project_rule(**kwargs):
    resp = api.del_project_rule(kwargs['timestamp'], kwargs['project_id'],
                                kwargs['rule_group_id'], kwargs['rule_id'],
                                kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--role_id',
              required=True,
              type=str,
              help='the role id of hpc project')
@click.option('--rule_group_id',
              required=True,
              type=str,
              help='the rule group id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def del_project_rule_group(**kwargs):
    resp = api.del_project_rule_group(kwargs['timestamp'],
                                      kwargs['project_id'], kwargs['role_id'],
                                      kwargs['rule_group_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the id of hpc project')
@click.option('--resource_id', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def del_resource(**kwargs):
    resp = api.del_resource(
        kwargs['timestamp'], kwargs['project_id'],
        json.loads(kwargs['resource_id']) if kwargs['resource_id'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id', required=True)
@click.option('--unlease', type=str, help='if ')
@click.option('--zone', required=True, type=str, help='zone id')
def destroy_project(**kwargs):
    resp = api.destroy_project(
        kwargs['timestamp'],
        json.loads(kwargs['project_id']) if kwargs['project_id'] else None,
        kwargs['unlease'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--role_id', required=True)
@click.option('--unlease', type=str, help='if ')
@click.option('--zone', required=True, type=str, help='zone id')
def destroy_project_role(**kwargs):
    resp = api.destroy_project_role(
        kwargs['timestamp'], kwargs['project_id'],
        json.loads(kwargs['role_id']) if kwargs['role_id'] else None,
        kwargs['unlease'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_id', required=True)
@click.option('--unlease', type=str, help='if ')
@click.option('--zone', required=True, type=str, help='zone id')
def destroy_project_rule(**kwargs):
    resp = api.destroy_project_rule(
        kwargs['timestamp'], kwargs['project_id'],
        json.loads(kwargs['rule_id']) if kwargs['rule_id'] else None,
        kwargs['unlease'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_group_id', required=True)
@click.option('--unlease', type=str, help='if ')
@click.option('--zone', required=True, type=str, help='zone id')
def destroy_project_rule_group(**kwargs):
    resp = api.destroy_project_rule_group(
        kwargs['timestamp'], kwargs['project_id'],
        json.loads(kwargs['rule_group_id']) if kwargs['rule_group_id'] else
        None, kwargs['unlease'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def init_configuration(**kwargs):
    resp = api.init_configuration(kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--member_account',
              type=str,
              help='member_account of the hpc project member')
@click.option('--member_id',
              type=str,
              help='the member_id of hpc project member')
@click.option('--member_name',
              type=str,
              help='member_name of the hpc project member')
@click.option('--member_user',
              type=str,
              help='member_user of the hpc project member')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--role_type',
              type=str,
              help='role_type of the hpc project member')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_member(**kwargs):
    resp = api.list_member(
        kwargs['limit'], kwargs['member_account'], kwargs['member_id'],
        kwargs['member_name'], kwargs['member_user'], kwargs['offset'],
        kwargs['project_id'], kwargs['reverse'], kwargs['role_type'],
        kwargs['run_user'], kwargs['search_word'], kwargs['sort_key'],
        kwargs['timestamp'], kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--resource_id', type=str, help='resource_id of the hpc project')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status', type=str, help='status of the hpc project')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_project(**kwargs):
    resp = api.list_project(kwargs['limit'], kwargs['offset'],
                            kwargs['project_id'], kwargs['resource_id'],
                            kwargs['reverse'], kwargs['run_user'],
                            kwargs['search_word'], kwargs['sort_key'],
                            kwargs['status'], kwargs['timestamp'],
                            kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status',
              type=str,
              help='status of the hpc project rule group')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_project_role(**kwargs):
    resp = api.list_project_role(kwargs['limit'], kwargs['offset'],
                                 kwargs['project_id'], kwargs['reverse'],
                                 kwargs['run_user'], kwargs['search_word'],
                                 kwargs['sort_key'], kwargs['status'],
                                 kwargs['timestamp'], kwargs['verbose'],
                                 kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status', type=str, help='status of the hpc project rule')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_project_rule(**kwargs):
    resp = api.list_project_rule(kwargs['limit'], kwargs['offset'],
                                 kwargs['project_id'], kwargs['reverse'],
                                 kwargs['run_user'], kwargs['search_word'],
                                 kwargs['sort_key'], kwargs['status'],
                                 kwargs['timestamp'], kwargs['verbose'],
                                 kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status',
              type=str,
              help='status of the hpc project rule group')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_project_rule_group(**kwargs):
    resp = api.list_project_rule_group(
        kwargs['limit'], kwargs['offset'], kwargs['project_id'],
        kwargs['reverse'], kwargs['run_user'], kwargs['search_word'],
        kwargs['sort_key'], kwargs['status'], kwargs['timestamp'],
        kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--project_id', type=str, help='the project_id of hpc project')
@click.option('--resource_id',
              type=str,
              help='the resource_id of hpc project resource')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_resource(**kwargs):
    resp = api.list_resource(kwargs['limit'], kwargs['offset'],
                             kwargs['project_id'], kwargs['resource_id'],
                             kwargs['reverse'], kwargs['run_user'],
                             kwargs['search_word'], kwargs['sort_key'],
                             kwargs['timestamp'], kwargs['verbose'],
                             kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description', type=str, help='the description of hpc project')
@click.option('--enabled', type=int, help='The hpc project enable status')
@click.option('--member_id',
              required=True,
              type=str,
              help='the project_id of hpc project')
@click.option('--member_name', type=str, help='the name of hpc project member')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project_id of hpc project')
@click.option('--role', type=str, help='the role id of hpc project member')
@click.option('--role_type',
              type=str,
              help='the role type of hpc project member')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_member(**kwargs):
    resp = api.modify_member(kwargs['timestamp'], kwargs['description'],
                             kwargs['enabled'], kwargs['member_id'],
                             kwargs['member_name'], kwargs['project_id'],
                             kwargs['role'], kwargs['role_type'],
                             kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description', type=str, help='the description of hpc project')
@click.option('--enabled', type=int, help='The hpc project enable status')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project_id of hpc project')
@click.option('--project_name', type=str, help='the name of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_project(**kwargs):
    resp = api.modify_project(kwargs['timestamp'], kwargs['description'],
                              kwargs['enabled'], kwargs['project_id'],
                              kwargs['project_name'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description',
              type=str,
              help='the description of hpc project role')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--role_id',
              required=True,
              type=str,
              help='the role id of hpc project')
@click.option('--status', type=str, help='The hpc project role enable status')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_project_role(**kwargs):
    resp = api.modify_project_role(kwargs['timestamp'], kwargs['description'],
                                   kwargs['project_id'], kwargs['role_id'],
                                   kwargs['status'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description',
              type=str,
              help='the description of hpc project rule')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_id',
              required=True,
              type=str,
              help='the rule id of hpc project')
@click.option('--status', type=str, help='The hpc project enable status')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_project_rule(**kwargs):
    resp = api.modify_project_rule(kwargs['timestamp'], kwargs['description'],
                                   kwargs['project_id'], kwargs['rule_id'],
                                   kwargs['status'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description',
              type=str,
              help='the description of hpc project rule group')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project id of hpc project')
@click.option('--rule_group_id',
              required=True,
              type=str,
              help='the rule group id of hpc project')
@click.option('--status', type=str, help='The hpc project enable status')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_project_rule_group(**kwargs):
    resp = api.modify_project_rule_group(kwargs['timestamp'],
                                         kwargs['description'],
                                         kwargs['project_id'],
                                         kwargs['rule_group_id'],
                                         kwargs['status'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--description', type=str, help='the description of hpc project')
@click.option('--enabled', type=int, help='The hpc project enable status')
@click.option('--project_id',
              required=True,
              type=str,
              help='the project_id of hpc project')
@click.option('--resource_id',
              required=True,
              type=str,
              help='the resource_id of hpc project')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_resource(**kwargs):
    resp = api.modify_resource(kwargs['timestamp'], kwargs['description'],
                               kwargs['enabled'], kwargs['project_id'],
                               kwargs['resource_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--allow_accounts', type=str, help=' allow count default ALL')
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--default_queue', type=int, help='0:NO,1:YES,default 0')
@click.option('--deny_accounts', type=str, help='deny count default NO')
@click.option('--max_time', type=str, help='max time of task default INFINITE')
@click.option('--min_node',
              type=int,
              help='the min number of compute node default 1')
@click.option('--name', required=True, type=str, help='the name of queue')
@click.option('--status', type=int, help=' 1:UP,0:DOWN,default 1')
@click.option('--user_group', type=str, help='the user_group of ehpc queue')
@click.option('--zone', required=True, type=str, help='zone id')
def add_ehpc_queue(**kwargs):
    resp = api.add_ehpc_queue(kwargs['timestamp'], kwargs['allow_accounts'],
                              kwargs['cluster_id'], kwargs['default_queue'],
                              kwargs['deny_accounts'], kwargs['max_time'],
                              kwargs['min_node'], kwargs['name'],
                              kwargs['status'], kwargs['user_group'],
                              kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--hpcqueue_id', required=True, type=str, help='the queue_id')
@click.option('--nodelist', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def add_ehpc_queue_nodes(**kwargs):
    resp = api.add_ehpc_queue_nodes(
        kwargs['timestamp'], kwargs['cluster_id'], kwargs['hpcqueue_id'],
        json.loads(kwargs['nodelist']) if kwargs['nodelist'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--belong',
              required=True,
              type=int,
              help='indicate if this queue is a private')
@click.option('--categories',
              required=True,
              type=str,
              help='the categories of hpc phy queue')
@click.option('--hpq_name', required=True, type=str, help='the name of queue')
@click.option('--scheduler_queue_name',
              required=True,
              type=str,
              help='the name of scheduler(e.g. aip) queue')
@click.option('--type_id',
              required=True,
              type=str,
              help='the id of hpc queue type')
@click.option('--user_group',
              required=True,
              type=str,
              help='the user_group of hpc phy queue')
@click.option('--zone', required=True, type=str, help='zone id')
def add_phy_queue(**kwargs):
    resp = api.add_phy_queue(kwargs['timestamp'], kwargs['belong'],
                             kwargs['categories'], kwargs['hpq_name'],
                             kwargs['scheduler_queue_name'], kwargs['type_id'],
                             kwargs['user_group'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cpu_num',
              required=True,
              type=int,
              help='the cpu num of  hpc queue type')
@click.option('--gpu_num',
              required=True,
              type=int,
              help='the gpu num of hpc queue type')
@click.option('--mem_size',
              required=True,
              type=int,
              help='the mem size of hpc queue type')
@click.option('--name',
              required=True,
              type=str,
              help='the name of hpc queue type')
@click.option('--node_num',
              required=True,
              type=int,
              help='the id of hpc queue type')
@click.option('--zone', required=True, type=str, help='zone id')
def add_queue_type(**kwargs):
    resp = api.add_queue_type(kwargs['timestamp'], kwargs['cpu_num'],
                              kwargs['gpu_num'], kwargs['mem_size'],
                              kwargs['name'], kwargs['node_num'],
                              kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              type=str,
              help='the cluster_id that private queue belong to')
@click.option(
    '--duration',
    type=int,
    help='if paid_type is Reserved ,Set the queue duration period required')
@click.option(
    '--is_auto_renewal',
    type=int,
    help=
    'if paid_type is Reserved ,sets the queue is automatically renewed required'
)
@click.option('--name',
              required=True,
              type=str,
              help='the name of private queue')
@click.option('--paid_type',
              required=True,
              type=str,
              help='set pay type for private queue')
@click.option('--type_id',
              required=True,
              type=str,
              help='the id of private queue type')
@click.option('--zone', required=True, type=str, help='zone id')
def bind_private_queue(**kwargs):
    resp = api.bind_private_queue(kwargs['timestamp'], kwargs['cluster_id'],
                                  kwargs['duration'],
                                  kwargs['is_auto_renewal'], kwargs['name'],
                                  kwargs['paid_type'], kwargs['type_id'],
                                  kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='ehpc cluster_id')
@click.option('--queue_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def del_ehpc_queues(**kwargs):
    resp = api.del_ehpc_queues(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['queue_ids']) if kwargs['queue_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--hpq_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def del_phy_queues(**kwargs):
    resp = api.del_phy_queues(
        kwargs['timestamp'],
        json.loads(kwargs['hpq_ids']) if kwargs['hpq_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--type_ids', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def del_queue_types(**kwargs):
    resp = api.del_queue_types(
        kwargs['timestamp'],
        json.loads(kwargs['type_ids']) if kwargs['type_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='the id of current cluster id')
@click.option('--id', required=True, type=str, help='the private id for queue')
@click.option('--owner', type=str, help='queue owner')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def describe_queue(**kwargs):
    resp = api.describe_queue(kwargs['cluster_id'], kwargs['id'],
                              kwargs['owner'], kwargs['timestamp'],
                              kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option(
    '--belong',
    type=int,
    help='the belong type for queue.[0:shared;1:private,-1:all,default:all]')
@click.option('--cluster_id',
              type=str,
              help='the cluster id private queue belong to ')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='queue list owner')
@click.option('--reverse', type=int, help='whether sort by sort_key reverse')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[resource_id,name]')
@click.option('--sort_key', type=str, help='sort by sort_key')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_current_queue(**kwargs):
    resp = api.get_current_queue(kwargs['belong'], kwargs['cluster_id'],
                                 kwargs['limit'], kwargs['offset'],
                                 kwargs['owner'], kwargs['reverse'],
                                 kwargs['search_word'], kwargs['sort_key'],
                                 kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='ehpc cluster_id')
@click.option('--is_active',
              type=int,
              help='is queue active only 1: action queue only')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--name', type=str, help='get queue with name')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--queue_ids')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_ehpc_queue_list(**kwargs):
    resp = api.get_ehpc_queue_list(
        kwargs['cluster_id'], kwargs['is_active'], kwargs['limit'],
        kwargs['name'], kwargs['offset'],
        json.loads(kwargs['queue_ids']) if kwargs['queue_ids'] else None,
        kwargs['reverse'], kwargs['search_word'], kwargs['sort_key'],
        kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--hpq_ids')
@click.option('--hpq_name', type=str, help='get queue with name')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_phy_queues(**kwargs):
    resp = api.get_phy_queues(
        json.loads(kwargs['hpq_ids']) if kwargs['hpq_ids'] else None,
        kwargs['hpq_name'], kwargs['limit'], kwargs['offset'],
        kwargs['reverse'], kwargs['search_word'], kwargs['sort_key'],
        kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--hpcqueue_id',
              required=True,
              type=str,
              help='the private id for queue')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_queue_nodes(**kwargs):
    resp = api.get_queue_nodes(kwargs['hpcqueue_id'], kwargs['limit'],
                               kwargs['offset'], kwargs['search_word'],
                               kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--name', type=str, help='get queue type with name')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--type_ids')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_queue_type_list(**kwargs):
    resp = api.get_queue_type_list(
        kwargs['limit'], kwargs['name'], kwargs['offset'], kwargs['reverse'],
        kwargs['search_word'], kwargs['sort_key'], kwargs['timestamp'],
        json.loads(kwargs['type_ids']) if kwargs['type_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_queue_types(**kwargs):
    resp = api.get_queue_types(kwargs['limit'], kwargs['offset'],
                               kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--scheduler_queue_name',
              required=True,
              type=str,
              help='the name of aip private queue')
@click.option('--timestamp', required=True)
@click.option('--user_id', required=True, type=str, help='the id of Iass user')
@click.option('--zone', required=True, type=str, help='Zone ID')
def is_available_queue(**kwargs):
    resp = api.is_available_queue(kwargs['scheduler_queue_name'],
                                  kwargs['timestamp'], kwargs['user_id'],
                                  kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--allow_accounts', type=str, help=' allow count default ALL')
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--default_queue', type=int, help='0:NO,1:YES,default 0')
@click.option('--deny_accounts', type=str, help='deny count default NO')
@click.option('--hpcqueue_id', required=True, type=str, help='the queue_id')
@click.option('--max_time', type=str, help='max time of task default INFINITE')
@click.option('--min_node',
              type=int,
              help='the min number of compute node default 1')
@click.option('--name', type=str, help='the ehpc queue name')
@click.option('--status', type=int, help=' 1:UP,0:DOWN,default 1')
@click.option('--user_group', type=str, help='the user_group of ehpc queue')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_ehpc_queue(**kwargs):
    resp = api.modify_ehpc_queue(
        kwargs['timestamp'], kwargs['allow_accounts'], kwargs['cluster_id'],
        kwargs['default_queue'], kwargs['deny_accounts'],
        kwargs['hpcqueue_id'], kwargs['max_time'], kwargs['min_node'],
        kwargs['name'], kwargs['status'], kwargs['user_group'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--hpcqueue_id', required=True, type=str, help='the queue_id')
@click.option('--nodelist', required=True)
@click.option('--zone', required=True, type=str, help='zone id')
def remove_ehpc_queue_nodes(**kwargs):
    resp = api.remove_ehpc_queue_nodes(
        kwargs['timestamp'], kwargs['cluster_id'], kwargs['hpcqueue_id'],
        json.loads(kwargs['nodelist']) if kwargs['nodelist'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--ids', required=True, type=str, help='queue primary id')
@click.option('--zone', required=True, type=str, help='zone id')
def unbind_private_queue(**kwargs):
    resp = api.unbind_private_queue(
        kwargs['timestamp'],
        json.loads(kwargs['ids']) if kwargs['ids'] else None, kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--id', required=True, type=str, help='the queue primary id')
@click.option('--name', required=True, type=str, help='the queue alias name')
@click.option('--zone', required=True, type=str, help='zone id')
def update_queue_name(**kwargs):
    resp = api.update_queue_name(kwargs['timestamp'], kwargs['id'],
                                 kwargs['name'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='cluster id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='the bill info owner')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word', type=str, help='fuzzy query - support keys:')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_bill_info(**kwargs):
    resp = api.get_cluster_bill_info(kwargs['cluster_id'], kwargs['limit'],
                                     kwargs['offset'], kwargs['owner'],
                                     kwargs['reverse'], kwargs['search_word'],
                                     kwargs['sort_key'], kwargs['timestamp'],
                                     kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', required=True, type=str, help='cluster id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--paid_type', type=str, help='set pay type for private queue')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word', type=str, help='fuzzy query - support keys:')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_private_resource_info(**kwargs):
    resp = api.get_cluster_private_resource_info(
        kwargs['cluster_id'], kwargs['limit'], kwargs['offset'],
        kwargs['paid_type'], kwargs['reverse'], kwargs['search_word'],
        kwargs['sort_key'], kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', required=True, type=str, help='cluster id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word', type=str, help='fuzzy query - support keys:')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_share_resource_info(**kwargs):
    resp = api.get_cluster_share_resource_info(
        kwargs['cluster_id'], kwargs['limit'], kwargs['offset'],
        kwargs['reverse'], kwargs['search_word'], kwargs['sort_key'],
        kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--end_time')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--resource_type', required=True, type=str, help='resource type')
@click.option('--start_time')
@click.option('--timestamp', required=True)
@click.option('--user_id', required=True, type=str, help=' user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_hpc_free_info(**kwargs):
    resp = api.get_hpc_free_info(kwargs['end_time'], kwargs['limit'],
                                 kwargs['offset'], kwargs['resource_type'],
                                 kwargs['start_time'], kwargs['timestamp'],
                                 kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word', type=str, help='fuzzy query - support keys:')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_remoteapp_bill_info(**kwargs):
    resp = api.get_remoteapp_bill_info(kwargs['limit'], kwargs['offset'],
                                       kwargs['reverse'],
                                       kwargs['search_word'],
                                       kwargs['sort_key'], kwargs['timestamp'],
                                       kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--class_id', type=str, help='the software is class_id')
@click.option('--deploy_mode', type=int, help='the software deploy_mode')
@click.option('--description', type=str, help='the software description')
@click.option('--icon', required=True, type=str, help='the software icon')
@click.option('--ini_cmd',
              required=True,
              type=str,
              help='the software ini cmd')
@click.option('--new_class', type=int, help='is new software class')
@click.option('--new_class_name', type=str, help='is new software class name')
@click.option('--software_mess', type=str, help='the software is help message')
@click.option('--sw_name', required=True, type=str, help='the software name')
@click.option('--sw_type', required=True, type=int, help='the software type')
@click.option('--sw_ver',
              required=True,
              type=str,
              help='the software sw version')
def add_software(**kwargs):
    resp = api.add_software(kwargs['limit'], kwargs['offset'],
                            kwargs['search_word'], kwargs['timestamp'],
                            kwargs['zone'], kwargs['class_id'],
                            kwargs['deploy_mode'], kwargs['description'],
                            kwargs['icon'], kwargs['ini_cmd'],
                            kwargs['new_class'], kwargs['new_class_name'],
                            kwargs['software_mess'], kwargs['sw_name'],
                            kwargs['sw_type'], kwargs['sw_ver'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--email', required=True, type=str, help='the user email')
@click.option('--phone', required=True, type=str, help='the user phone')
@click.option('--platform', type=int, help='platform')
@click.option('--reason', required=True, type=str, help='the reason')
@click.option('--sw_name', type=str, help='the software name')
def apply_software(**kwargs):
    resp = api.apply_software(kwargs['timestamp'], kwargs['zone'],
                              kwargs['email'], kwargs['phone'],
                              kwargs['platform'], kwargs['reason'],
                              kwargs['sw_name'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--class_id',
              required=True,
              type=str,
              help='the software class id')
def delete_class(**kwargs):
    resp = api.delete_class(kwargs['limit'], kwargs['offset'],
                            kwargs['search_word'], kwargs['timestamp'],
                            kwargs['zone'], kwargs['class_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--hpcsw_id', required=True, type=str, help='the software id')
def delete_software(**kwargs):
    resp = api.delete_software(kwargs['limit'], kwargs['offset'],
                               kwargs['search_word'], kwargs['timestamp'],
                               kwargs['zone'], kwargs['hpcsw_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--apply_type', type=str, help='the apply_type')
@click.option('--is_apply', type=int, help='the is_apply')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='cluster owner')
@click.option(
    '--platform',
    type=int,
    help='[hpc software supported platform, 1.HPC  2.EHPC 3. both HPC and EHPC]'
)
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status', type=str, help='the apply status')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_apply(**kwargs):
    resp = api.get_apply(kwargs['apply_type'], kwargs['is_apply'],
                         kwargs['limit'], kwargs['offset'], kwargs['owner'],
                         kwargs['platform'], kwargs['reverse'],
                         kwargs['search_word'], kwargs['sort_key'],
                         kwargs['status'], kwargs['timestamp'],
                         kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id',
              required=True,
              type=str,
              help='hpc/ehpc cluster id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_cluster_software_list(**kwargs):
    resp = api.get_cluster_software_list(kwargs['cluster_id'],
                                         kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--apply_type', type=str, help='the apply_type')
@click.option('--is_apply', type=int, help='the is_apply')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='cluster owner')
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_graphics(**kwargs):
    resp = api.get_graphics(kwargs['apply_type'], kwargs['is_apply'],
                            kwargs['limit'], kwargs['offset'], kwargs['owner'],
                            kwargs['reverse'], kwargs['sort_key'],
                            kwargs['timestamp'], kwargs['user_id'],
                            kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--class_id', type=str, help='software class id')
@click.option(
    '--deploy_mode',
    type=int,
    help='[hpc software deploy mode: 1.pre-installed 2. on demand deployment]')
@click.option('--hpcsw_id', type=str, help='software id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='cluster owner')
@click.option(
    '--platform',
    type=int,
    help='[hpc software supported platform, 1.HPC  2.EHPC 3. both HPC and EHPC]'
)
@click.option('--reverse', type=int, help='0:ASC, 1:DESC.')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort key - default:create_time.')
@click.option('--status', type=int, help='the user_visible')
@click.option('--sw_type',
              type=str,
              help='the sw_type opensource[1] or commercial[0]')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_list(**kwargs):
    resp = api.get_list(kwargs['class_id'], kwargs['deploy_mode'],
                        kwargs['hpcsw_id'], kwargs['limit'], kwargs['offset'],
                        kwargs['owner'], kwargs['platform'], kwargs['reverse'],
                        kwargs['search_word'], kwargs['sort_key'],
                        kwargs['status'], kwargs['sw_type'],
                        kwargs['timestamp'], kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--hpcsw_id', type=str, help='[hpcsw id]')
@click.option('--nas_mount_point', type=str, help='[nas_mount_point]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_remoteapp_link(**kwargs):
    resp = api.get_remoteapp_link(kwargs['hpcsw_id'],
                                  kwargs['nas_mount_point'],
                                  kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', type=str, help='')
@click.option('--sw_ids')
@click.option('--zone', type=str, help='zone id')
def install_cluster_softwares(**kwargs):
    resp = api.install_cluster_softwares(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['sw_ids']) if kwargs['sw_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--class_id', type=str, help='software class id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_class(**kwargs):
    resp = api.list_class(kwargs['class_id'], kwargs['timestamp'],
                          kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--mark', required=True, type=int, help='1 mark  0 cancle mark')
@click.option('--sw_name', required=True, type=str, help='software name')
@click.option('--user_id', required=True, type=str, help='user_id')
def mark(**kwargs):
    resp = api.mark(kwargs['timestamp'], kwargs['zone'], kwargs['mark'],
                    kwargs['sw_name'], kwargs['user_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--class_id', type=str, help='the software class id')
@click.option('--hpcsw_id', required=True, type=str, help='software id')
@click.option('--ini_cmd', type=str, help='the software ini cmd')
@click.option('--sw_name', type=str, help='the software name')
def modify_software(**kwargs):
    resp = api.modify_software(kwargs['limit'], kwargs['offset'],
                               kwargs['search_word'], kwargs['timestamp'],
                               kwargs['zone'], kwargs['class_id'],
                               kwargs['hpcsw_id'], kwargs['ini_cmd'],
                               kwargs['sw_name'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--hpcsw_id', required=True, type=str, help='hpcsw_id')
@click.option('--user_visible',
              required=True,
              type=int,
              help='the software is user visible')
def start_software(**kwargs):
    resp = api.start_software(kwargs['timestamp'], kwargs['zone'],
                              kwargs['hpcsw_id'], kwargs['user_visible'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--hpcsw_id', required=True, type=str, help='hpcsw_id')
@click.option('--user_visible',
              required=True,
              type=int,
              help='the software is user visible')
def stop_software(**kwargs):
    resp = api.stop_software(kwargs['timestamp'], kwargs['zone'],
                             kwargs['hpcsw_id'], kwargs['user_visible'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', type=str, help='')
@click.option('--sw_ids')
@click.option('--zone', type=str, help='zone id')
def uninstall_cluster_softwares(**kwargs):
    resp = api.uninstall_cluster_softwares(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['sw_ids']) if kwargs['sw_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--is_apply', required=True, type=int, help='is apply software')
@click.option('--notify_email', type=str, help='notify_email')
@click.option('--reason', required=True, type=str, help='apply reason')
@click.option('--reason_id', required=True, type=str, help='reason_id')
@click.option('--sw_name', required=True, type=str, help='the software name')
def update_apply(**kwargs):
    resp = api.update_apply(kwargs['timestamp'], kwargs['zone'],
                            kwargs['is_apply'], kwargs['notify_email'],
                            kwargs['reason'], kwargs['reason_id'],
                            kwargs['sw_name'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--hpc_status', type=str, help='[hpc permission status].')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='operation job reverse')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_subusers(**kwargs):
    resp = api.list_subusers(kwargs['hpc_status'], kwargs['limit'],
                             kwargs['offset'], kwargs['reverse'],
                             kwargs['search_word'], kwargs['timestamp'],
                             kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster id ldap user belong to')
@click.option('--password', required=True, type=str, help='password')
@click.option('--username', required=True, type=str, help='username')
@click.option('--zone', required=True, type=str, help='zone id')
def add_user(**kwargs):
    resp = api.add_user(kwargs['timestamp'], kwargs['cluster_id'],
                        kwargs['password'], kwargs['username'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster id ldap user belong to')
@click.option('--username', required=True, type=str, help='username')
@click.option('--zone', required=True, type=str, help='zone id')
def delete_user(**kwargs):
    resp = api.delete_user(kwargs['timestamp'], kwargs['cluster_id'],
                           kwargs['username'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def describe_hpc_login_account_user(**kwargs):
    resp = api.describe_hpc_login_account_user(kwargs['timestamp'],
                                               kwargs['user_id'],
                                               kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--reverse', type=int, help='operation job reverse')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--sort_key', type=str, help='sort_key')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_users(**kwargs):
    resp = api.list_users(kwargs['cluster_id'], kwargs['limit'],
                          kwargs['offset'], kwargs['reverse'],
                          kwargs['search_word'], kwargs['sort_key'],
                          kwargs['timestamp'], kwargs['user_id'],
                          kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster id ldap user belong to')
@click.option('--new_password', required=True, type=str, help='new_password')
@click.option('--username', required=True, type=str, help='username')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_user(**kwargs):
    resp = api.modify_user(kwargs['timestamp'], kwargs['cluster_id'],
                           kwargs['new_password'], kwargs['username'],
                           kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--file_name', required=True, type=str, help='file_name')
@click.option('--format', required=True, type=str, help='format')
@click.option('--text', type=str, help='text')
def file_create_template(**kwargs):
    resp = api.file_create_template(kwargs['timestamp'], kwargs['zone'],
                                    kwargs['file_name'], kwargs['format'],
                                    kwargs['text'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def file_list_templates(**kwargs):
    resp = api.file_list_templates(kwargs['limit'], kwargs['offset'],
                                   kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--file_id', required=True, type=str, help='file_id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def file_template_delete(**kwargs):
    resp = api.file_template_delete(kwargs['file_id'], kwargs['timestamp'],
                                    kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--file_id', required=True, type=str, help='file_id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def file_template_detail(**kwargs):
    resp = api.file_template_detail(kwargs['file_id'], kwargs['timestamp'],
                                    kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--file_id', required=True, type=str, help='file_id')
@click.option('--file_name', required=True, type=str, help='file_name')
@click.option('--format', required=True, type=str, help='format')
@click.option('--text', type=str, help='text')
def file_template_update(**kwargs):
    resp = api.file_template_update(kwargs['timestamp'], kwargs['zone'],
                                    kwargs['file_id'], kwargs['file_name'],
                                    kwargs['format'], kwargs['text'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--end_time', type=str, help='end_time')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--resource',
              required=True,
              type=str,
              help='get resource charge records')
@click.option('--start_time', type=str, help='start_time')
@click.option('--timestamp', required=True)
@click.option('--user_id', type=str, help='user id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_charge_records(**kwargs):
    resp = api.get_charge_records(kwargs['end_time'], kwargs['limit'],
                                  kwargs['offset'], kwargs['resource'],
                                  kwargs['start_time'], kwargs['timestamp'],
                                  kwargs['user_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--cluster_id', required=True, type=str, help='cluster_id')
@click.option('--cmd_line', type=str, help='cmd_line')
@click.option('--cmd_line_type', type=str, help='cmd_line_type')
@click.option('--core_limit', type=int, help='core_limit')
@click.option('--host_name', type=str, help='host_name')
@click.option('--job_name', type=str, help='job_name')
@click.option('--job_priority')
@click.option('--resource_limit', type=str, help='resource_limit')
@click.option('--resources', type=str, help='resources')
@click.option('--run_user', type=str, help='run_user')
@click.option('--scheduler_queue_name', type=str, help='scheduler_queue_name')
@click.option('--stderr_redirect_path', type=str, help='stderr_redirect_path')
@click.option('--stderr_redirect_path_type',
              type=str,
              help='stderr_redirect_path_type')
@click.option('--stdout_redirect_path', type=str, help='stdout_redirect_path')
@click.option('--stdout_redirect_path_type',
              type=str,
              help='stdout_redirect_path_type')
@click.option('--temp_name', required=True, type=str, help='temp_name')
@click.option('--user_id', required=True, type=str, help='user_id')
def job_create_template(**kwargs):
    resp = api.job_create_template(
        kwargs['timestamp'], kwargs['zone'], kwargs['cluster_id'],
        kwargs['cmd_line'], kwargs['cmd_line_type'], kwargs['core_limit'],
        kwargs['host_name'], kwargs['job_name'], kwargs['job_priority'],
        kwargs['resource_limit'], kwargs['resources'], kwargs['run_user'],
        kwargs['scheduler_queue_name'], kwargs['stderr_redirect_path'],
        kwargs['stderr_redirect_path_type'], kwargs['stdout_redirect_path'],
        kwargs['stdout_redirect_path_type'], kwargs['temp_name'],
        kwargs['user_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', required=True, type=str, help='cluster_id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--search_word',
              type=str,
              help='fuzzy query - support keys:[name]')
@click.option('--timestamp', required=True)
@click.option('--user_id', required=True, type=str, help='user_id')
@click.option('--zone', required=True, type=str, help='Zone ID')
def job_list_templates(**kwargs):
    resp = api.job_list_templates(kwargs['cluster_id'], kwargs['limit'],
                                  kwargs['offset'], kwargs['search_word'],
                                  kwargs['timestamp'], kwargs['user_id'],
                                  kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--temp_id', required=True, type=str, help='temp_id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def job_template_delete(**kwargs):
    resp = api.job_template_delete(kwargs['temp_id'], kwargs['timestamp'],
                                   kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--temp_id', required=True, type=str, help='temp_id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def job_template_detail(**kwargs):
    resp = api.job_template_detail(kwargs['temp_id'], kwargs['timestamp'],
                                   kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--cluster_id', required=True, type=str, help='cluster_id')
@click.option('--cmd_line', type=str, help='cmd_line')
@click.option('--core_limit', type=int, help='core_limit')
@click.option('--host_name', type=str, help='host_name')
@click.option('--job_name', type=str, help='job_name')
@click.option('--job_priority')
@click.option('--resource_limit', type=str, help='resource_limit')
@click.option('--resources', type=str, help='resources')
@click.option('--run_user', type=str, help='run_user')
@click.option('--scheduler_queue_name', type=str, help='scheduler_queue_name')
@click.option('--stderr_redirect_path', type=str, help='stderr_redirect_path')
@click.option('--stdout_redirect_path', type=str, help='stdout_redirect_path')
@click.option('--temp_id', required=True, type=str, help='temp_id')
@click.option('--temp_name', required=True, type=str, help='temp_name')
@click.option('--user_id', required=True, type=str, help='user_id')
def job_template_update(**kwargs):
    resp = api.job_template_update(
        kwargs['timestamp'], kwargs['zone'], kwargs['cluster_id'],
        kwargs['cmd_line'], kwargs['core_limit'], kwargs['host_name'],
        kwargs['job_name'], kwargs['job_priority'], kwargs['resource_limit'],
        kwargs['resources'], kwargs['run_user'],
        kwargs['scheduler_queue_name'], kwargs['stderr_redirect_path'],
        kwargs['stdout_redirect_path'], kwargs['temp_id'], kwargs['temp_name'],
        kwargs['user_id'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--min_nodes_or_max_cores',
              required=True,
              type=int,
              help='min nodes or max cores')
@click.option('--op_interval',
              required=True,
              type=int,
              help='op interval(minutes)')
@click.option('--op_type',
              required=True,
              type=int,
              help='0:shrink,1:expand,default 0')
@click.option('--queue_id', required=True, type=str, help='the queue uuid')
@click.option('--run_now', type=int, help='0:NO,1:YES,default 0')
def add_ehpc_queue_strategy(**kwargs):
    resp = api.add_ehpc_queue_strategy(kwargs['timestamp'], kwargs['zone'],
                                       kwargs['cluster_id'],
                                       kwargs['min_nodes_or_max_cores'],
                                       kwargs['op_interval'],
                                       kwargs['op_type'], kwargs['queue_id'],
                                       kwargs['run_now'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--op_type',
              required=True,
              type=int,
              help='0:shrink,1:expand,default 0')
@click.option('--queue_id', required=True, type=str, help='the queue uuid')
@click.option('--zone', required=True, type=str, help='zone id')
def del_ehpc_queue_strategy(**kwargs):
    resp = api.del_ehpc_queue_strategy(kwargs['timestamp'],
                                       kwargs['cluster_id'], kwargs['op_type'],
                                       kwargs['queue_id'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--is_enabled',
              required=True,
              type=int,
              help='0:disable, 1:enable')
@click.option('--op_type',
              required=True,
              type=int,
              help='0:shrink,1:expand,default 0')
@click.option('--queue_id', required=True, type=str, help='the queue uuid')
@click.option('--run_now', type=int, help='0:NO,1:YES,default 0')
@click.option('--zone', required=True, type=str, help='zone id')
def enable_ehpc_queue_strategy(**kwargs):
    resp = api.enable_ehpc_queue_strategy(kwargs['timestamp'],
                                          kwargs['is_enabled'],
                                          kwargs['op_type'],
                                          kwargs['queue_id'],
                                          kwargs['run_now'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', required=True, type=str, help='ehpc cluster_id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--op_is_enabled', type=int, help='0:disable 1:enable')
@click.option('--op_type', type=int, help='0:shrink,1:expand.')
@click.option('--queue_ids')
@click.option('--reverse', type=int, help='0:asc, 1:desc.')
@click.option('--sort_key', type=str, help='sort key.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_ehpc_queue_strategy_list(**kwargs):
    resp = api.get_ehpc_queue_strategy_list(
        kwargs['cluster_id'], kwargs['limit'], kwargs['offset'],
        kwargs['op_is_enabled'], kwargs['op_type'],
        json.loads(kwargs['queue_ids']) if kwargs['queue_ids'] else None,
        kwargs['reverse'], kwargs['sort_key'], kwargs['timestamp'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', required=True, type=str, help='ehpc cluster_id')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--op_status', type=str, help='success/failed')
@click.option('--op_type', type=int, help='0:shrink,1:expand.')
@click.option('--queue_ids')
@click.option('--reverse', type=int, help='0:asc, 1:desc.')
@click.option('--sort_key', type=str, help='sort key.')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_ehpc_queue_strategy_log_list(**kwargs):
    resp = api.get_ehpc_queue_strategy_log_list(
        kwargs['cluster_id'], kwargs['limit'], kwargs['offset'],
        kwargs['op_status'], kwargs['op_type'],
        json.loads(kwargs['queue_ids']) if kwargs['queue_ids'] else None,
        kwargs['reverse'], kwargs['sort_key'], kwargs['timestamp'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', required=True, type=str, help='the cluster uuid')
@click.option('--min_nodes_or_max_cores',
              required=True,
              type=int,
              help='min nodes or max cores')
@click.option('--op_interval',
              required=True,
              type=int,
              help='op interval(minutes)')
@click.option('--op_type',
              required=True,
              type=int,
              help='0:shrink,1:expand,default 0')
@click.option('--queue_id', required=True, type=str, help='the queue uuid')
@click.option('--run_now', type=int, help='0:NO,1:YES,default 0')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_ehpc_queue_strategy(**kwargs):
    resp = api.modify_ehpc_queue_strategy(
        kwargs['timestamp'], kwargs['cluster_id'],
        kwargs['min_nodes_or_max_cores'], kwargs['op_interval'],
        kwargs['op_type'], kwargs['queue_id'], kwargs['run_now'],
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', type=str, help='The cluster of job file')
@click.option('--job_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def delete_simulation_jobs(**kwargs):
    resp = api.delete_simulation_jobs(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['job_ids']) if kwargs['job_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--sjob_id', required=True, type=str, help='ID of job')
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--timestamp', required=True)
@click.option('--zone', required=True, type=str, help='Zone ID')
def get_simulation_job_detail(**kwargs):
    resp = api.get_simulation_job_detail(kwargs['sjob_id'],
                                         kwargs['cluster_id'],
                                         kwargs['timestamp'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--cluster_id', type=str, help='Cluster Id')
@click.option('--cluster_type', type=str, help='in boss job list cluster_type')
@click.option('--end_time')
@click.option('--hpcqueue_id', type=str, help='job of queue')
@click.option('--job_status', type=str, help='Job Status')
@click.option('--limit', type=int, help='the limit for collections')
@click.option('--offset', type=int, help='the offset for collections')
@click.option('--owner', type=str, help='job list owner')
@click.option('--queue_name', type=str, help='the queue name to filter')
@click.option('--reverse', type=int, help='whether sort by sort_key reverse')
@click.option('--run_user', type=str, help='User who run Job')
@click.option('--search_word', type=str, help='the search key word')
@click.option('--sjob_id', type=str, help='in the boss of sjob_id')
@click.option('--software_list', type=str, help='software list')
@click.option('--sort_key', type=str, help='sort by sort_key')
@click.option('--start_time')
@click.option('--submit_type',
              type=int,
              help='[submit job type. 1:cli , 0:console]')
@click.option('--timestamp', required=True)
@click.option('--verbose', type=int, help='operation job verbose')
@click.option('--zone', required=True, type=str, help='Zone ID')
def list_simulation_jobs(**kwargs):
    resp = api.list_simulation_jobs(
        kwargs['cluster_id'], kwargs['cluster_type'], kwargs['end_time'],
        kwargs['hpcqueue_id'], kwargs['job_status'], kwargs['limit'],
        kwargs['offset'], kwargs['owner'], kwargs['queue_name'],
        kwargs['reverse'], kwargs['run_user'], kwargs['search_word'],
        kwargs['sjob_id'], kwargs['software_list'], kwargs['sort_key'],
        kwargs['start_time'], kwargs['submit_type'], kwargs['timestamp'],
        kwargs['verbose'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', type=str, help='The cluster of job file')
@click.option('--job_ids', required=True, type=str, help='hpc job id')
@click.option('--zone', required=True, type=str, help='zone id')
def stop_simulation_jobs(**kwargs):
    resp = api.stop_simulation_jobs(
        kwargs['timestamp'], kwargs['cluster_id'],
        json.loads(kwargs['job_ids']) if kwargs['job_ids'] else None,
        kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id', type=str, help='The cluster of job file')
@click.option('--cmd_line', type=str, help='The job command line')
@click.option('--core_limit', type=int, help='The job core limit')
@click.option('--input_file', type=str, help='The job input file path')
@click.option('--mem_limit', type=int, help='The job memory limit')
@click.option('--name', required=True, type=str, help='The job name')
@click.option('--resource_limit',
              type=str,
              help='The limit of resource used by job')
@click.option('--run_user',
              required=True,
              type=str,
              help='The run user of job file')
@click.option('--scheduler_queue_name', type=str, help='The job queue name')
@click.option('--time_limit', type=int, help='The job execution time limit')
@click.option('--zone', required=True, type=str, help='zone id')
def submit_simulation_job(**kwargs):
    resp = api.submit_simulation_job(
        kwargs['timestamp'], kwargs['cluster_id'], kwargs['cmd_line'],
        kwargs['core_limit'], kwargs['input_file'], kwargs['mem_limit'],
        kwargs['name'], kwargs['resource_limit'], kwargs['run_user'],
        kwargs['scheduler_queue_name'], kwargs['time_limit'], kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


@root.command()
@click.option('--timestamp', required=True)
@click.option('--cluster_id',
              required=True,
              type=str,
              help='the cluster_id of hpc cluster')
@click.option('--node_id',
              required=True,
              type=str,
              help='the description of hpc cluster')
@click.option('--node_name',
              required=True,
              type=str,
              help='the name of hpc cluster')
@click.option('--zone', required=True, type=str, help='zone id')
def modify_cluster_node(**kwargs):
    resp = api.modify_cluster_node(kwargs['timestamp'], kwargs['cluster_id'],
                                   kwargs['node_id'], kwargs['node_name'],
                                   kwargs['zone'])
    click.echo(
        json.dumps(resp,
                   sort_keys=True,
                   indent=2,
                   separators=(',', ': '),
                   ensure_ascii=False))


if __name__ == '__main__':
    sys.argv.append("--timestamp")
    sys.argv.append(time.strftime(ISO8601, time.gmtime()))
    zone = None
    with open(client_conf, "r") as f:
        config_data = yaml.safe_load(f)
        zone = config_data["zone"]
        f.close()
    sys.argv.append("--zone")
    sys.argv.append(zone)
    root(sys.argv[1:])
