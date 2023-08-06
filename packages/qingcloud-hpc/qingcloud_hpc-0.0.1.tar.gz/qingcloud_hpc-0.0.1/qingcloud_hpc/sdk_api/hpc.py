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

import json
from functools import partial

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from qingcloud_hpc.request import Request
from qingcloud_hpc.unpack import Unpacker
from qingcloud_hpc.error import (ParameterRequiredError, ParameterValueNotAllowedError,
                   OutOfLengthRangeError, OutOfValueRangeError)

# Hpc provides hpc Service API (API Version 2020-10-27)


class Hpc(object):
    def __init__(self, config):
        self.config = config
        self.client = Session()
        retries = Retry(total=self.config.connection_retries,
                        backoff_factor=1,
                        status_forcelist=[500, 502, 503, 504])
        self.client.mount(self.config.protocol + "://",
                          HTTPAdapter(max_retries=retries))
        if hasattr(self.config, "timeout") and self.config.timeout:
            self.client.send = partial(self.client.send,
                                       timeout=self.config.timeout)

    def get_cost_request(self,
                         cpu_core_num="",
                         duration=None,
                         paid_type="",
                         plan_name="",
                         prod_name="",
                         queue_type="",
                         timestamp="",
                         zone=""):
        operation = {
            "API": "get_cost",
            "Method": "GET",
            "URI": "/api/billing/cost",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cpu_core_num:
            operation["Params"].update({"cpu_core_num": cpu_core_num})

        if duration:
            operation["Params"].update({"duration": duration})

        if paid_type:
            operation["Params"].update({"paid_type": paid_type})

        if plan_name:
            operation["Params"].update({"plan_name": plan_name})

        if prod_name:
            operation["Params"].update({"prod_name": prod_name})

        if queue_type:
            operation["Params"].update({"queue_type": queue_type})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cost_validate(operation)
        return Request(self.config, operation)

    def get_cost(self,
                 cpu_core_num="",
                 duration=None,
                 paid_type="",
                 plan_name="",
                 prod_name="",
                 queue_type="",
                 timestamp="",
                 zone=""):
        req = self.get_cost_request(cpu_core_num=cpu_core_num,
                                    duration=duration,
                                    paid_type=paid_type,
                                    plan_name=plan_name,
                                    prod_name=prod_name,
                                    queue_type=queue_type,
                                    timestamp=timestamp,
                                    zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cost_validate(op):

        if op["Params"]["paid_type"] is None:
            return ParameterRequiredError("paid_type", "get_costInput")

        if "paid_type" in op["Params"] and op["Params"]["paid_type"]:

            paid_type_valid_values = ["Reserved", "PayForUsed"]
            if op["Params"]["paid_type"] not in paid_type_valid_values:
                return ParameterValueNotAllowedError("paid_type",
                                                     op["Params"]["paid_type"],
                                                     paid_type_valid_values)

        if op["Params"]["prod_name"] is None:
            return ParameterRequiredError("prod_name", "get_costInput")

        if "prod_name" in op["Params"] and op["Params"]["prod_name"]:

            prod_name_valid_values = [
                "shared_queue_job", "privated_queue", "simulation", "remoteapp"
            ]
            if op["Params"]["prod_name"] not in prod_name_valid_values:
                return ParameterValueNotAllowedError("prod_name",
                                                     op["Params"]["prod_name"],
                                                     prod_name_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_costInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_costInput")

        return None

    def get_meter_request(self,
                          aggregation="",
                          end_time="",
                          instance_id="",
                          metering_period="",
                          meters=list(),
                          start_time="",
                          time_zone="",
                          timestamp=""):
        operation = {
            "API": "get_meter",
            "Method": "GET",
            "URI": "/api/billing/getmeter",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if aggregation:
            operation["Params"].update({"aggregation": aggregation})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if instance_id:
            operation["Params"].update({"instance_id": instance_id})

        if metering_period:
            operation["Params"].update({"metering_period": metering_period})

        if meters != list() and meters:
            operation["Params"].update({"meters": meters})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if time_zone:
            operation["Params"].update({"time_zone": time_zone})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        self.get_meter_validate(operation)
        return Request(self.config, operation)

    def get_meter(self,
                  aggregation="",
                  end_time="",
                  instance_id="",
                  metering_period="",
                  meters=list(),
                  start_time="",
                  time_zone="",
                  timestamp=""):
        req = self.get_meter_request(aggregation=aggregation,
                                     end_time=end_time,
                                     instance_id=instance_id,
                                     metering_period=metering_period,
                                     meters=meters,
                                     start_time=start_time,
                                     time_zone=time_zone,
                                     timestamp=timestamp)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_meter_validate(op):
        if op["Params"]["aggregation"] is None:
            return ParameterRequiredError("aggregation", "get_meterInput")

        if op["Params"]["end_time"] is None:
            return ParameterRequiredError("end_time", "get_meterInput")

        if op["Params"]["instance_id"] is None:
            return ParameterRequiredError("instance_id", "get_meterInput")

        if op["Params"]["metering_period"] is None:
            return ParameterRequiredError("metering_period", "get_meterInput")

        if op["Params"]["start_time"] is None:
            return ParameterRequiredError("start_time", "get_meterInput")

        if op["Params"]["time_zone"] is None:
            return ParameterRequiredError("time_zone", "get_meterInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_meterInput")

        return None

    def get_product_billing_model_request(self,
                                          prod_name="",
                                          timestamp="",
                                          zone=""):
        operation = {
            "API": "get_product_billing_model",
            "Method": "GET",
            "URI": "/api/billing/productmodel",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if prod_name:
            operation["Params"].update({"prod_name": prod_name})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_product_billing_model_validate(operation)
        return Request(self.config, operation)

    def get_product_billing_model(self, prod_name="", timestamp="", zone=""):
        req = self.get_product_billing_model_request(prod_name=prod_name,
                                                     timestamp=timestamp,
                                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_product_billing_model_validate(op):
        if op["Params"]["prod_name"] is None:
            return ParameterRequiredError("prod_name",
                                          "get_product_billing_modelInput")

        if "prod_name" in op["Params"] and op["Params"]["prod_name"]:

            prod_name_valid_values = [
                "shared_queue_job", "privated_queue", "simulation", "remoteapp"
            ]
            if op["Params"]["prod_name"] not in prod_name_valid_values:
                return ParameterValueNotAllowedError("prod_name",
                                                     op["Params"]["prod_name"],
                                                     prod_name_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_product_billing_modelInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_product_billing_modelInput")

        return None

    def list_remoteapp_log_request(self,
                                   app_name="",
                                   app_state="",
                                   app_user_id="",
                                   duration_max=None,
                                   duration_min=None,
                                   end_time="",
                                   limit=None,
                                   offset=None,
                                   reverse=None,
                                   sort_key="",
                                   start_time="",
                                   timestamp="",
                                   zone=""):
        operation = {
            "API": "list_remoteapp_log",
            "Method": "GET",
            "URI": "/api/billing/remoteapp_log_list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if app_name:
            operation["Params"].update({"app_name": app_name})

        if app_state:
            operation["Params"].update({"app_state": app_state})

        if app_user_id:
            operation["Params"].update({"app_user_id": app_user_id})

        if duration_max:
            operation["Params"].update({"duration_max": duration_max})

        if duration_min:
            operation["Params"].update({"duration_min": duration_min})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_remoteapp_log_validate(operation)
        return Request(self.config, operation)

    def list_remoteapp_log(self,
                           app_name="",
                           app_state="",
                           app_user_id="",
                           duration_max=None,
                           duration_min=None,
                           end_time="",
                           limit=None,
                           offset=None,
                           reverse=None,
                           sort_key="",
                           start_time="",
                           timestamp="",
                           zone=""):
        req = self.list_remoteapp_log_request(app_name=app_name,
                                              app_state=app_state,
                                              app_user_id=app_user_id,
                                              duration_max=duration_max,
                                              duration_min=duration_min,
                                              end_time=end_time,
                                              limit=limit,
                                              offset=offset,
                                              reverse=reverse,
                                              sort_key=sort_key,
                                              start_time=start_time,
                                              timestamp=timestamp,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_remoteapp_log_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_remoteapp_logInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_remoteapp_logInput")

        return None

    def notify_request(self,
                       timestamp="",
                       access_sys_id="",
                       event="",
                       occurred_at="",
                       prod_inst_id_ext="",
                       user_id="",
                       zone=""):
        operation = {
            "API": "notify",
            "Method": "POST",
            "URI": "/api/billing/notify",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if access_sys_id:
            operation["Elements"].update({"access_sys_id": access_sys_id})
        if event:
            operation["Elements"].update({"event": event})
        if occurred_at:
            operation["Elements"].update({"occurred_at": occurred_at})
        if prod_inst_id_ext:
            operation["Elements"].update(
                {"prod_inst_id_ext": prod_inst_id_ext})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.notify_validate(operation)
        return Request(self.config, operation)

    def notify(self,
               timestamp="",
               access_sys_id="",
               event="",
               occurred_at="",
               prod_inst_id_ext="",
               user_id="",
               zone=""):
        req = self.notify_request(timestamp=timestamp,
                                  access_sys_id=access_sys_id,
                                  event=event,
                                  occurred_at=occurred_at,
                                  prod_inst_id_ext=prod_inst_id_ext,
                                  user_id=user_id,
                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def notify_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "notifyInput")

        if op["Elements"]["access_sys_id"] is None:
            return ParameterRequiredError("access_sys_id", "notifyInput")

        if op["Elements"]["event"] is None:
            return ParameterRequiredError("event", "notifyInput")

        if op["Elements"]["occurred_at"] is None:
            return ParameterRequiredError("occurred_at", "notifyInput")

        if op["Elements"]["prod_inst_id_ext"] is None:
            return ParameterRequiredError("prod_inst_id_ext", "notifyInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id", "notifyInput")

        return None

    def remoteapp_notify_request(self,
                                 timestamp="",
                                 access_sys_id="",
                                 event="",
                                 occurred_at="",
                                 prod_inst_id_ext="",
                                 user_id="",
                                 zone=""):
        operation = {
            "API": "remoteapp_notify",
            "Method": "POST",
            "URI": "/api/billing/remoteapp_notify",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if access_sys_id:
            operation["Elements"].update({"access_sys_id": access_sys_id})
        if event:
            operation["Elements"].update({"event": event})
        if occurred_at:
            operation["Elements"].update({"occurred_at": occurred_at})
        if prod_inst_id_ext:
            operation["Elements"].update(
                {"prod_inst_id_ext": prod_inst_id_ext})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.remoteapp_notify_validate(operation)
        return Request(self.config, operation)

    def remoteapp_notify(self,
                         timestamp="",
                         access_sys_id="",
                         event="",
                         occurred_at="",
                         prod_inst_id_ext="",
                         user_id="",
                         zone=""):
        req = self.remoteapp_notify_request(timestamp=timestamp,
                                            access_sys_id=access_sys_id,
                                            event=event,
                                            occurred_at=occurred_at,
                                            prod_inst_id_ext=prod_inst_id_ext,
                                            user_id=user_id,
                                            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def remoteapp_notify_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "remoteapp_notifyInput")

        if op["Elements"]["access_sys_id"] is None:
            return ParameterRequiredError("access_sys_id",
                                          "remoteapp_notifyInput")

        if op["Elements"]["event"] is None:
            return ParameterRequiredError("event", "remoteapp_notifyInput")

        if op["Elements"]["occurred_at"] is None:
            return ParameterRequiredError("occurred_at",
                                          "remoteapp_notifyInput")

        if op["Elements"]["prod_inst_id_ext"] is None:
            return ParameterRequiredError("prod_inst_id_ext",
                                          "remoteapp_notifyInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id", "remoteapp_notifyInput")

        return None

    def run_cmd_request(self,
                        timestamp="",
                        cmd="",
                        dispatcher="",
                        ip="",
                        user="",
                        zone=""):
        operation = {
            "API": "run_cmd",
            "Method": "POST",
            "URI": "/api/cli/runCmd",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cmd:
            operation["Elements"].update({"cmd": cmd})
        if dispatcher:
            operation["Elements"].update({"dispatcher": dispatcher})
        if ip:
            operation["Elements"].update({"ip": ip})
        if user:
            operation["Elements"].update({"user": user})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.run_cmd_validate(operation)
        return Request(self.config, operation)

    def run_cmd(self,
                timestamp="",
                cmd="",
                dispatcher="",
                ip="",
                user="",
                zone=""):
        req = self.run_cmd_request(timestamp=timestamp,
                                   cmd=cmd,
                                   dispatcher=dispatcher,
                                   ip=ip,
                                   user=user,
                                   zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def run_cmd_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "run_cmdInput")

        return None

    def add_cluster_nodes_request(self,
                                  timestamp="",
                                  cluster_id="",
                                  hpcqueue_id="",
                                  node_count="",
                                  node_name="",
                                  node_role="",
                                  private_ips=list(),
                                  zone=""):
        operation = {
            "API": "add_cluster_nodes",
            "Method": "POST",
            "URI": "/api/cluster/addNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if hpcqueue_id:
            operation["Elements"].update({"hpcqueue_id": hpcqueue_id})
        if node_count:
            operation["Elements"].update({"node_count": node_count})
        if node_name:
            operation["Elements"].update({"node_name": node_name})
        if node_role:
            operation["Elements"].update({"node_role": node_role})
        if private_ips:
            operation["Elements"].update({"private_ips": private_ips})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_cluster_nodes_validate(operation)
        return Request(self.config, operation)

    def add_cluster_nodes(self,
                          timestamp="",
                          cluster_id="",
                          hpcqueue_id="",
                          node_count="",
                          node_name="",
                          node_role="",
                          private_ips=list(),
                          zone=""):
        req = self.add_cluster_nodes_request(timestamp=timestamp,
                                             cluster_id=cluster_id,
                                             hpcqueue_id=hpcqueue_id,
                                             node_count=node_count,
                                             node_name=node_name,
                                             node_role=node_role,
                                             private_ips=private_ips,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_cluster_nodes_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "add_cluster_nodesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "add_cluster_nodesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_cluster_nodesInput")

        return None

    def add_cluster_nodes_fee_request(self,
                                      cluster_id="",
                                      node_count="",
                                      node_name="",
                                      node_role="",
                                      timestamp="",
                                      zone=""):
        operation = {
            "API": "add_cluster_nodes_fee",
            "Method": "GET",
            "URI": "/api/cluster/addNodesFee",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if node_count:
            operation["Params"].update({"node_count": node_count})

        if node_name:
            operation["Params"].update({"node_name": node_name})

        if node_role:
            operation["Params"].update({"node_role": node_role})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.add_cluster_nodes_fee_validate(operation)
        return Request(self.config, operation)

    def add_cluster_nodes_fee(self,
                              cluster_id="",
                              node_count="",
                              node_name="",
                              node_role="",
                              timestamp="",
                              zone=""):
        req = self.add_cluster_nodes_fee_request(cluster_id=cluster_id,
                                                 node_count=node_count,
                                                 node_name=node_name,
                                                 node_role=node_role,
                                                 timestamp=timestamp,
                                                 zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_cluster_nodes_fee_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "add_cluster_nodes_feeInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "add_cluster_nodes_feeInput")

        return None

    def associate_login_node_eip_request(self,
                                         timestamp="",
                                         cluster_id="",
                                         cluster_node="",
                                         eip_id="",
                                         zone=""):
        operation = {
            "API": "associate_login_node_eip",
            "Method": "POST",
            "URI": "/api/cluster/associateLoginNodeEip",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cluster_node:
            operation["Elements"].update({"cluster_node": cluster_node})
        if eip_id:
            operation["Elements"].update({"eip_id": eip_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.associate_login_node_eip_validate(operation)
        return Request(self.config, operation)

    def associate_login_node_eip(self,
                                 timestamp="",
                                 cluster_id="",
                                 cluster_node="",
                                 eip_id="",
                                 zone=""):
        req = self.associate_login_node_eip_request(timestamp=timestamp,
                                                    cluster_id=cluster_id,
                                                    cluster_node=cluster_node,
                                                    eip_id=eip_id,
                                                    zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def associate_login_node_eip_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "associate_login_node_eipInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "associate_login_node_eipInput")

        if op["Elements"]["cluster_node"] is None:
            return ParameterRequiredError("cluster_node",
                                          "associate_login_node_eipInput")

        if op["Elements"]["eip_id"] is None:
            return ParameterRequiredError("eip_id",
                                          "associate_login_node_eipInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "associate_login_node_eipInput")

        return None

    def create_cluster_request(self,
                               timestamp="",
                               charge_mode="",
                               cluster_conf=None,
                               cluster_name="",
                               cluster_type="",
                               deploy_mode="",
                               duration=None,
                               is_auto_renewal=None,
                               owner="",
                               zone=""):
        operation = {
            "API": "create_cluster",
            "Method": "POST",
            "URI": "/api/cluster/createCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if charge_mode:
            operation["Elements"].update({"charge_mode": charge_mode})
        if cluster_conf:
            operation["Elements"].update(
                {"cluster_conf": json.loads(cluster_conf)})
        if cluster_name:
            operation["Elements"].update({"cluster_name": cluster_name})
        if cluster_type:
            operation["Elements"].update({"cluster_type": cluster_type})
        if deploy_mode:
            operation["Elements"].update({"deploy_mode": deploy_mode})
        if duration:
            operation["Elements"].update({"duration": duration})
        if is_auto_renewal:
            operation["Elements"].update({"is_auto_renewal": is_auto_renewal})
        if owner:
            operation["Elements"].update({"owner": owner})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_cluster_validate(operation)
        return Request(self.config, operation)

    def create_cluster(self,
                       timestamp="",
                       charge_mode="",
                       cluster_conf=None,
                       cluster_name="",
                       cluster_type="",
                       deploy_mode="",
                       duration=None,
                       is_auto_renewal=None,
                       owner="",
                       zone=""):
        req = self.create_cluster_request(timestamp=timestamp,
                                          charge_mode=charge_mode,
                                          cluster_conf=cluster_conf,
                                          cluster_name=cluster_name,
                                          cluster_type=cluster_type,
                                          deploy_mode=deploy_mode,
                                          duration=duration,
                                          is_auto_renewal=is_auto_renewal,
                                          owner=owner,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "create_clusterInput")

        if "cluster_type" in op["Elements"] and op["Elements"]["cluster_type"]:

            cluster_type_valid_values = ["hpc", "ehpc"]
            if op["Elements"]["cluster_type"] not in cluster_type_valid_values:
                return ParameterValueNotAllowedError(
                    "cluster_type", op["Elements"]["cluster_type"],
                    cluster_type_valid_values)

        if "is_auto_renewal" in op["Elements"] and op["Elements"][
                "is_auto_renewal"]:

            is_auto_renewal_valid_values = ["0", "1"]
            if op["Elements"][
                    "is_auto_renewal"] not in is_auto_renewal_valid_values:
                return ParameterValueNotAllowedError(
                    "is_auto_renewal", op["Elements"]["is_auto_renewal"],
                    is_auto_renewal_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "create_clusterInput")

        return None

    def delete_cluster_request(self,
                               timestamp="",
                               cluster_ids=list(),
                               run_user="",
                               unlease="",
                               zone=""):
        operation = {
            "API": "delete_cluster",
            "Method": "POST",
            "URI": "/api/cluster/deleteCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_ids:
            operation["Elements"].update({"cluster_ids": cluster_ids})
        if run_user:
            operation["Elements"].update({"run_user": run_user})
        if unlease:
            operation["Elements"].update({"unlease": unlease})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.delete_cluster_validate(operation)
        return Request(self.config, operation)

    def delete_cluster(self,
                       timestamp="",
                       cluster_ids=list(),
                       run_user="",
                       unlease="",
                       zone=""):
        req = self.delete_cluster_request(timestamp=timestamp,
                                          cluster_ids=cluster_ids,
                                          run_user=run_user,
                                          unlease=unlease,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "delete_clusterInput")

        if op["Elements"]["cluster_ids"] is None:
            return ParameterRequiredError("cluster_ids", "delete_clusterInput")

        if op["Elements"]["run_user"] is None:
            return ParameterRequiredError("run_user", "delete_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_clusterInput")

        return None

    def delete_cluster_nodes_request(self,
                                     timestamp="",
                                     cluster_id="",
                                     node_ids=list(),
                                     zone=""):
        operation = {
            "API": "delete_cluster_nodes",
            "Method": "POST",
            "URI": "/api/cluster/deleteNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if node_ids:
            operation["Elements"].update({"node_ids": node_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.delete_cluster_nodes_validate(operation)
        return Request(self.config, operation)

    def delete_cluster_nodes(self,
                             timestamp="",
                             cluster_id="",
                             node_ids=list(),
                             zone=""):
        req = self.delete_cluster_nodes_request(timestamp=timestamp,
                                                cluster_id=cluster_id,
                                                node_ids=node_ids,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_cluster_nodes_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "delete_cluster_nodesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "delete_cluster_nodesInput")

        if op["Elements"]["node_ids"] is None:
            return ParameterRequiredError("node_ids",
                                          "delete_cluster_nodesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_cluster_nodesInput")

        return None

    def dissociate_login_node_eip_request(self,
                                          timestamp="",
                                          cluster_id="",
                                          eip_ids=list(),
                                          zone=""):
        operation = {
            "API": "dissociate_login_node_eip",
            "Method": "POST",
            "URI": "/api/cluster/dissociateLoginNodeEip",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if eip_ids:
            operation["Elements"].update({"eip_ids": eip_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.dissociate_login_node_eip_validate(operation)
        return Request(self.config, operation)

    def dissociate_login_node_eip(self,
                                  timestamp="",
                                  cluster_id="",
                                  eip_ids=list(),
                                  zone=""):
        req = self.dissociate_login_node_eip_request(timestamp=timestamp,
                                                     cluster_id=cluster_id,
                                                     eip_ids=eip_ids,
                                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def dissociate_login_node_eip_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "dissociate_login_node_eipInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "dissociate_login_node_eipInput")

        if op["Elements"]["eip_ids"] is None:
            return ParameterRequiredError("eip_ids",
                                          "dissociate_login_node_eipInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "dissociate_login_node_eipInput")

        return None

    def get_cluster_conf_request(self, cluster_type="", timestamp="", zone=""):
        operation = {
            "API": "get_cluster_conf",
            "Method": "GET",
            "URI": "/api/cluster/conf",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_type:
            operation["Params"].update({"cluster_type": cluster_type})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_conf_validate(operation)
        return Request(self.config, operation)

    def get_cluster_conf(self, cluster_type="", timestamp="", zone=""):
        req = self.get_cluster_conf_request(cluster_type=cluster_type,
                                            timestamp=timestamp,
                                            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_conf_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_cluster_confInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_cluster_confInput")

        return None

    def get_cluster_nodes_request(self,
                                  cluster_id="",
                                  health_status="",
                                  limit=None,
                                  node_role="",
                                  offset=None,
                                  reverse=None,
                                  search_word="",
                                  sort_key="",
                                  status="",
                                  timestamp="",
                                  verbose=None,
                                  zone=""):
        operation = {
            "API": "get_cluster_nodes",
            "Method": "GET",
            "URI": "/api/cluster/listNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if health_status:
            operation["Params"].update({"health_status": health_status})

        if limit:
            operation["Params"].update({"limit": limit})

        if node_role:
            operation["Params"].update({"node_role": node_role})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_nodes_validate(operation)
        return Request(self.config, operation)

    def get_cluster_nodes(self,
                          cluster_id="",
                          health_status="",
                          limit=None,
                          node_role="",
                          offset=None,
                          reverse=None,
                          search_word="",
                          sort_key="",
                          status="",
                          timestamp="",
                          verbose=None,
                          zone=""):
        req = self.get_cluster_nodes_request(cluster_id=cluster_id,
                                             health_status=health_status,
                                             limit=limit,
                                             node_role=node_role,
                                             offset=offset,
                                             reverse=reverse,
                                             search_word=search_word,
                                             sort_key=sort_key,
                                             status=status,
                                             timestamp=timestamp,
                                             verbose=verbose,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_nodes_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_cluster_nodesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_cluster_nodesInput")

        return None

    def get_hpc_cluster_detail_request(self,
                                       cluster_ids=list(),
                                       owner="",
                                       timestamp="",
                                       zone=""):
        operation = {
            "API": "get_hpc_cluster_detail",
            "Method": "GET",
            "URI": "/api/cluster/cluster_detail",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }
        if cluster_ids != list() and cluster_ids:
            operation["Params"].update({"cluster_ids": cluster_ids})

        if owner:
            operation["Params"].update({"owner": owner})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_hpc_cluster_detail_validate(operation)
        return Request(self.config, operation)

    def get_hpc_cluster_detail(self,
                               cluster_ids=list(),
                               owner="",
                               timestamp="",
                               zone=""):
        req = self.get_hpc_cluster_detail_request(cluster_ids=cluster_ids,
                                                  owner=owner,
                                                  timestamp=timestamp,
                                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_hpc_cluster_detail_validate(op):
        if op["Params"]["cluster_ids"] is None:
            return ParameterRequiredError("cluster_ids",
                                          "get_hpc_cluster_detailInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_hpc_cluster_detailInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_hpc_cluster_detailInput")

        return None

    def get_nas_info_request(self,
                             cluster_id="",
                             search_word="",
                             timestamp="",
                             zone=""):
        operation = {
            "API": "get_nas_info",
            "Method": "GET",
            "URI": "/api/cluster/nasInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_nas_info_validate(operation)
        return Request(self.config, operation)

    def get_nas_info(self,
                     cluster_id="",
                     search_word="",
                     timestamp="",
                     zone=""):
        req = self.get_nas_info_request(cluster_id=cluster_id,
                                        search_word=search_word,
                                        timestamp=timestamp,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_nas_info_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "get_nas_infoInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_nas_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_nas_infoInput")

        return None

    def list_cluster_request(self,
                             cluster_id="",
                             cluster_type="",
                             end_time="",
                             iam_cluster_ids="",
                             limit=None,
                             offset=None,
                             owner="",
                             reverse=None,
                             run_user="",
                             search_word="",
                             shared_status="",
                             sort_key="",
                             start_time="",
                             status="",
                             timestamp="",
                             verbose=None,
                             zone=""):
        operation = {
            "API": "list_cluster",
            "Method": "GET",
            "URI": "/api/cluster/list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if cluster_type:
            operation["Params"].update({"cluster_type": cluster_type})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if iam_cluster_ids:
            operation["Params"].update({"iam_cluster_ids": iam_cluster_ids})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if shared_status:
            operation["Params"].update({"shared_status": shared_status})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_cluster_validate(operation)
        return Request(self.config, operation)

    def list_cluster(self,
                     cluster_id="",
                     cluster_type="",
                     end_time="",
                     iam_cluster_ids="",
                     limit=None,
                     offset=None,
                     owner="",
                     reverse=None,
                     run_user="",
                     search_word="",
                     shared_status="",
                     sort_key="",
                     start_time="",
                     status="",
                     timestamp="",
                     verbose=None,
                     zone=""):
        req = self.list_cluster_request(cluster_id=cluster_id,
                                        cluster_type=cluster_type,
                                        end_time=end_time,
                                        iam_cluster_ids=iam_cluster_ids,
                                        limit=limit,
                                        offset=offset,
                                        owner=owner,
                                        reverse=reverse,
                                        run_user=run_user,
                                        search_word=search_word,
                                        shared_status=shared_status,
                                        sort_key=sort_key,
                                        start_time=start_time,
                                        status=status,
                                        timestamp=timestamp,
                                        verbose=verbose,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_cluster_validate(op):

        if "cluster_type" in op["Params"] and op["Params"]["cluster_type"]:

            cluster_type_valid_values = ["hpc", "ehpc"]
            if op["Params"]["cluster_type"] not in cluster_type_valid_values:
                return ParameterValueNotAllowedError(
                    "cluster_type", op["Params"]["cluster_type"],
                    cluster_type_valid_values)

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if "shared_status" in op["Params"] and op["Params"]["shared_status"]:

            shared_status_valid_values = [
                "not_shared", "shared_owner", "shared_member"
            ]
            if op["Params"]["shared_status"] not in shared_status_valid_values:
                return ParameterValueNotAllowedError(
                    "shared_status", op["Params"]["shared_status"],
                    shared_status_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_clusterInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_clusterInput")

        return None

    def modify_cluster_request(self,
                               timestamp="",
                               cluster_id="",
                               cluster_name="",
                               description="",
                               zone=""):
        operation = {
            "API": "modify_cluster",
            "Method": "POST",
            "URI": "/api/cluster/modifyCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cluster_name:
            operation["Elements"].update({"cluster_name": cluster_name})
        if description:
            operation["Elements"].update({"description": description})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_cluster_validate(operation)
        return Request(self.config, operation)

    def modify_cluster(self,
                       timestamp="",
                       cluster_id="",
                       cluster_name="",
                       description="",
                       zone=""):
        req = self.modify_cluster_request(timestamp=timestamp,
                                          cluster_id=cluster_id,
                                          cluster_name=cluster_name,
                                          description=description,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_clusterInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "modify_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_clusterInput")

        return None

    def modify_cluster_node_request(self,
                                    timestamp="",
                                    cluster_id="",
                                    node_id="",
                                    node_name="",
                                    zone=""):
        operation = {
            "API": "modify_cluster_node",
            "Method": "POST",
            "URI": "/api/cluster/modifyClusterNode",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if node_id:
            operation["Elements"].update({"node_id": node_id})
        if node_name:
            operation["Elements"].update({"node_name": node_name})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_cluster_node_validate(operation)
        return Request(self.config, operation)

    def modify_cluster_node(self,
                            timestamp="",
                            cluster_id="",
                            node_id="",
                            node_name="",
                            zone=""):
        req = self.modify_cluster_node_request(timestamp=timestamp,
                                               cluster_id=cluster_id,
                                               node_id=node_id,
                                               node_name=node_name,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_cluster_node_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["node_id"] is None:
            return ParameterRequiredError("node_id",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["node_name"] is None:
            return ParameterRequiredError("node_name",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_cluster_nodeInput")

        return None

    def resize_cluster_request(self,
                               timestamp="",
                               cluster_id="",
                               cpu="",
                               gpu="",
                               instance_class="",
                               memory="",
                               node_role="",
                               storage_size="",
                               zone=""):
        operation = {
            "API": "resize_cluster",
            "Method": "POST",
            "URI": "/api/cluster/resizeCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cpu:
            operation["Elements"].update({"cpu": cpu})
        if gpu:
            operation["Elements"].update({"gpu": gpu})
        if instance_class:
            operation["Elements"].update({"instance_class": instance_class})
        if memory:
            operation["Elements"].update({"memory": memory})
        if node_role:
            operation["Elements"].update({"node_role": node_role})
        if storage_size:
            operation["Elements"].update({"storage_size": storage_size})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.resize_cluster_validate(operation)
        return Request(self.config, operation)

    def resize_cluster(self,
                       timestamp="",
                       cluster_id="",
                       cpu="",
                       gpu="",
                       instance_class="",
                       memory="",
                       node_role="",
                       storage_size="",
                       zone=""):
        req = self.resize_cluster_request(timestamp=timestamp,
                                          cluster_id=cluster_id,
                                          cpu=cpu,
                                          gpu=gpu,
                                          instance_class=instance_class,
                                          memory=memory,
                                          node_role=node_role,
                                          storage_size=storage_size,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def resize_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "resize_clusterInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "resize_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "resize_clusterInput")

        return None

    def resize_cluster_fee_request(self,
                                   cluster_id="",
                                   cpu="",
                                   gpu="",
                                   instance_class="",
                                   memory="",
                                   node_role="",
                                   storage_size="",
                                   timestamp="",
                                   zone=""):
        operation = {
            "API": "resize_cluster_fee",
            "Method": "GET",
            "URI": "/api/cluster/resizeClusterFee",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if cpu:
            operation["Params"].update({"cpu": cpu})

        if gpu:
            operation["Params"].update({"gpu": gpu})

        if instance_class:
            operation["Params"].update({"instance_class": instance_class})

        if memory:
            operation["Params"].update({"memory": memory})

        if node_role:
            operation["Params"].update({"node_role": node_role})

        if storage_size:
            operation["Params"].update({"storage_size": storage_size})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.resize_cluster_fee_validate(operation)
        return Request(self.config, operation)

    def resize_cluster_fee(self,
                           cluster_id="",
                           cpu="",
                           gpu="",
                           instance_class="",
                           memory="",
                           node_role="",
                           storage_size="",
                           timestamp="",
                           zone=""):
        req = self.resize_cluster_fee_request(cluster_id=cluster_id,
                                              cpu=cpu,
                                              gpu=gpu,
                                              instance_class=instance_class,
                                              memory=memory,
                                              node_role=node_role,
                                              storage_size=storage_size,
                                              timestamp=timestamp,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def resize_cluster_fee_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "resize_cluster_feeInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "resize_cluster_feeInput")

        return None

    def restart_cluster_nodes_request(self,
                                      timestamp="",
                                      cluster_id="",
                                      node_ids=list(),
                                      zone=""):
        operation = {
            "API": "restart_cluster_nodes",
            "Method": "POST",
            "URI": "/api/cluster/restartNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if node_ids:
            operation["Elements"].update({"node_ids": node_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.restart_cluster_nodes_validate(operation)
        return Request(self.config, operation)

    def restart_cluster_nodes(self,
                              timestamp="",
                              cluster_id="",
                              node_ids=list(),
                              zone=""):
        req = self.restart_cluster_nodes_request(timestamp=timestamp,
                                                 cluster_id=cluster_id,
                                                 node_ids=node_ids,
                                                 zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def restart_cluster_nodes_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "restart_cluster_nodesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "restart_cluster_nodesInput")

        if op["Elements"]["node_ids"] is None:
            return ParameterRequiredError("node_ids",
                                          "restart_cluster_nodesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "restart_cluster_nodesInput")

        return None

    def resume_cluster_request(self,
                               timestamp="",
                               cluster_ids=list(),
                               owner="",
                               user_id="",
                               zone=""):
        operation = {
            "API": "resume_cluster",
            "Method": "POST",
            "URI": "/api/cluster/resumeCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_ids:
            operation["Elements"].update({"cluster_ids": cluster_ids})
        if owner:
            operation["Elements"].update({"owner": owner})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.resume_cluster_validate(operation)
        return Request(self.config, operation)

    def resume_cluster(self,
                       timestamp="",
                       cluster_ids=list(),
                       owner="",
                       user_id="",
                       zone=""):
        req = self.resume_cluster_request(timestamp=timestamp,
                                          cluster_ids=cluster_ids,
                                          owner=owner,
                                          user_id=user_id,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def resume_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "resume_clusterInput")

        if op["Elements"]["cluster_ids"] is None:
            return ParameterRequiredError("cluster_ids", "resume_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "resume_clusterInput")

        return None

    def start_cluster_request(self, timestamp="", cluster_ids=list(), zone=""):
        operation = {
            "API": "start_cluster",
            "Method": "POST",
            "URI": "/api/cluster/startCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_ids:
            operation["Elements"].update({"cluster_ids": cluster_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.start_cluster_validate(operation)
        return Request(self.config, operation)

    def start_cluster(self, timestamp="", cluster_ids=list(), zone=""):
        req = self.start_cluster_request(timestamp=timestamp,
                                         cluster_ids=cluster_ids,
                                         zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def start_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "start_clusterInput")

        if op["Elements"]["cluster_ids"] is None:
            return ParameterRequiredError("cluster_ids", "start_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "start_clusterInput")

        return None

    def stop_cluster_request(self, timestamp="", cluster_ids=list(), zone=""):
        operation = {
            "API": "stop_cluster",
            "Method": "POST",
            "URI": "/api/cluster/stopCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_ids:
            operation["Elements"].update({"cluster_ids": cluster_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.stop_cluster_validate(operation)
        return Request(self.config, operation)

    def stop_cluster(self, timestamp="", cluster_ids=list(), zone=""):
        req = self.stop_cluster_request(timestamp=timestamp,
                                        cluster_ids=cluster_ids,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def stop_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "stop_clusterInput")

        if op["Elements"]["cluster_ids"] is None:
            return ParameterRequiredError("cluster_ids", "stop_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "stop_clusterInput")

        return None

    def upgrade_cluster_request(self,
                                timestamp="",
                                app_version="",
                                clusters=list(),
                                owner="",
                                zone=""):
        operation = {
            "API": "upgrade_cluster",
            "Method": "POST",
            "URI": "/api/cluster/upgradeCluster",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if app_version:
            operation["Elements"].update({"app_version": app_version})
        if clusters:
            operation["Elements"].update({"clusters": clusters})
        if owner:
            operation["Elements"].update({"owner": owner})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.upgrade_cluster_validate(operation)
        return Request(self.config, operation)

    def upgrade_cluster(self,
                        timestamp="",
                        app_version="",
                        clusters=list(),
                        owner="",
                        zone=""):
        req = self.upgrade_cluster_request(timestamp=timestamp,
                                           app_version=app_version,
                                           clusters=clusters,
                                           owner=owner,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def upgrade_cluster_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "upgrade_clusterInput")

        if op["Elements"]["app_version"] is None:
            return ParameterRequiredError("app_version",
                                          "upgrade_clusterInput")

        if op["Elements"]["clusters"] is None:
            return ParameterRequiredError("clusters", "upgrade_clusterInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "upgrade_clusterInput")

        return None

    def enable_ehpc_subuser_stor_request(self,
                                         timestamp="",
                                         cluster_id="",
                                         enable=None,
                                         shared_dir="",
                                         zone=""):
        operation = {
            "API": "enable_ehpc_subuser_stor",
            "Method": "POST",
            "URI": "/api/epmr/enableEhpcSubuserStor",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if enable:
            operation["Elements"].update({"enable": enable})
        if shared_dir:
            operation["Elements"].update({"shared_dir": shared_dir})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.enable_ehpc_subuser_stor_validate(operation)
        return Request(self.config, operation)

    def enable_ehpc_subuser_stor(self,
                                 timestamp="",
                                 cluster_id="",
                                 enable=None,
                                 shared_dir="",
                                 zone=""):
        req = self.enable_ehpc_subuser_stor_request(timestamp=timestamp,
                                                    cluster_id=cluster_id,
                                                    enable=enable,
                                                    shared_dir=shared_dir,
                                                    zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def enable_ehpc_subuser_stor_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "enable_ehpc_subuser_storInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "enable_ehpc_subuser_storInput")

        if op["Elements"]["enable"] is None:
            return ParameterRequiredError("enable",
                                          "enable_ehpc_subuser_storInput")

        if "enable" in op["Elements"] and op["Elements"]["enable"]:

            enable_valid_values = ["0", "1"]
            if op["Elements"]["enable"] not in enable_valid_values:
                return ParameterValueNotAllowedError("enable",
                                                     op["Elements"]["enable"],
                                                     enable_valid_values)

        return None

    def get_ehpc_subuser_stor_enable_status_request(self,
                                                    cluster_id="",
                                                    limit=None,
                                                    offset=None,
                                                    run_user="",
                                                    timestamp="",
                                                    verbose=None,
                                                    zone=""):
        operation = {
            "API": "get_ehpc_subuser_stor_enable_status",
            "Method": "GET",
            "URI": "/api/epmr/getEhpcSubuserStorEnableStatus",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_ehpc_subuser_stor_enable_status_validate(operation)
        return Request(self.config, operation)

    def get_ehpc_subuser_stor_enable_status(self,
                                            cluster_id="",
                                            limit=None,
                                            offset=None,
                                            run_user="",
                                            timestamp="",
                                            verbose=None,
                                            zone=""):
        req = self.get_ehpc_subuser_stor_enable_status_request(
            cluster_id=cluster_id,
            limit=limit,
            offset=offset,
            run_user=run_user,
            timestamp=timestamp,
            verbose=verbose,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_ehpc_subuser_stor_enable_status_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError(
                "cluster_id", "get_ehpc_subuser_stor_enable_statusInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError(
                "timestamp", "get_ehpc_subuser_stor_enable_statusInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError(
                "zone", "get_ehpc_subuser_stor_enable_statusInput")

        return None

    def list_ehpc_subuser_stor_request(self,
                                       cluster_id="",
                                       limit=None,
                                       offset=None,
                                       run_user="",
                                       subuser_ids="",
                                       timestamp="",
                                       verbose=None,
                                       zone=""):
        operation = {
            "API": "list_ehpc_subuser_stor",
            "Method": "GET",
            "URI": "/api/epmr/listEhpcSubuserStor",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if subuser_ids:
            operation["Params"].update({"subuser_ids": subuser_ids})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_ehpc_subuser_stor_validate(operation)
        return Request(self.config, operation)

    def list_ehpc_subuser_stor(self,
                               cluster_id="",
                               limit=None,
                               offset=None,
                               run_user="",
                               subuser_ids="",
                               timestamp="",
                               verbose=None,
                               zone=""):
        req = self.list_ehpc_subuser_stor_request(cluster_id=cluster_id,
                                                  limit=limit,
                                                  offset=offset,
                                                  run_user=run_user,
                                                  subuser_ids=subuser_ids,
                                                  timestamp=timestamp,
                                                  verbose=verbose,
                                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_ehpc_subuser_stor_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "list_ehpc_subuser_storInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_ehpc_subuser_storInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "list_ehpc_subuser_storInput")

        return None

    def create_job_file_request(self,
                                timestamp="",
                                cluster_id="",
                                file_type="",
                                file_value="",
                                target_file="",
                                zone=""):
        operation = {
            "API": "create_job_file",
            "Method": "POST",
            "URI": "/api/job/createJobFile",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if file_type:
            operation["Elements"].update({"file_type": file_type})
        if file_value:
            operation["Elements"].update({"file_value": file_value})
        if target_file:
            operation["Elements"].update({"target_file": target_file})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_job_file_validate(operation)
        return Request(self.config, operation)

    def create_job_file(self,
                        timestamp="",
                        cluster_id="",
                        file_type="",
                        file_value="",
                        target_file="",
                        zone=""):
        req = self.create_job_file_request(timestamp=timestamp,
                                           cluster_id=cluster_id,
                                           file_type=file_type,
                                           file_value=file_value,
                                           target_file=target_file,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_job_file_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "create_job_fileInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "create_job_fileInput")

        if op["Elements"]["file_type"] is None:
            return ParameterRequiredError("file_type", "create_job_fileInput")

        if "file_type" in op["Elements"] and op["Elements"]["file_type"]:

            file_type_valid_values = ["plain", "tar"]
            if op["Elements"]["file_type"] not in file_type_valid_values:
                return ParameterValueNotAllowedError(
                    "file_type", op["Elements"]["file_type"],
                    file_type_valid_values)

        if op["Elements"]["file_value"] is None:
            return ParameterRequiredError("file_value", "create_job_fileInput")

        if op["Elements"]["target_file"] is None:
            return ParameterRequiredError("target_file",
                                          "create_job_fileInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "create_job_fileInput")

        return None

    def delete_jobs_request(self,
                            timestamp="",
                            cluster_id="",
                            job_ids=list(),
                            zone=""):
        operation = {
            "API": "delete_jobs",
            "Method": "POST",
            "URI": "/api/job/deleteJobs",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if job_ids:
            operation["Elements"].update({"job_ids": job_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.delete_jobs_validate(operation)
        return Request(self.config, operation)

    def delete_jobs(self,
                    timestamp="",
                    cluster_id="",
                    job_ids=list(),
                    zone=""):
        req = self.delete_jobs_request(timestamp=timestamp,
                                       cluster_id=cluster_id,
                                       job_ids=job_ids,
                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_jobs_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "delete_jobsInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "delete_jobsInput")

        if op["Elements"]["job_ids"] is None:
            return ParameterRequiredError("job_ids", "delete_jobsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_jobsInput")

        return None

    def get_job_detail_request(self,
                               job_uuid="",
                               cluster_id="",
                               timestamp="",
                               zone=""):
        operation = {
            "API": "get_job_detail",
            "Method": "GET",
            "URI": "/api/job/jobdetail/<job_uuid>",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }
        if job_uuid:
            operation["Properties"].update({"job_uuid": job_uuid})

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_job_detail_validate(operation)
        return Request(self.config, operation)

    def get_job_detail(self,
                       job_uuid="",
                       cluster_id="",
                       timestamp="",
                       zone=""):
        req = self.get_job_detail_request(job_uuid=job_uuid,
                                          cluster_id=cluster_id,
                                          timestamp=timestamp,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_job_detail_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_job_detailInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_job_detailInput")

        return None

    def get_job_monitor_request(self,
                                cluster_id="",
                                end_time=None,
                                job_id=None,
                                limit=None,
                                meters=None,
                                start_time=None,
                                zone=""):
        operation = {
            "API": "get_job_monitor",
            "Method": "GET",
            "URI": "/api/job/getJobMonitor",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if job_id:
            operation["Params"].update({"job_id": job_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if meters:
            operation["Params"].update({"meters": meters})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_job_monitor_validate(operation)
        return Request(self.config, operation)

    def get_job_monitor(self,
                        cluster_id="",
                        end_time=None,
                        job_id=None,
                        limit=None,
                        meters=None,
                        start_time=None,
                        zone=""):
        req = self.get_job_monitor_request(cluster_id=cluster_id,
                                           end_time=end_time,
                                           job_id=job_id,
                                           limit=limit,
                                           meters=meters,
                                           start_time=start_time,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_job_monitor_validate(op):

        if op["Params"]["end_time"] is None:
            return ParameterRequiredError("end_time", "get_job_monitorInput")

        if op["Params"]["job_id"] is None:
            return ParameterRequiredError("job_id", "get_job_monitorInput")

        if op["Params"]["meters"] is None:
            return ParameterRequiredError("meters", "get_job_monitorInput")

        if op["Params"]["start_time"] is None:
            return ParameterRequiredError("start_time", "get_job_monitorInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_job_monitorInput")

        return None

    def list_jobs_request(self,
                          cluster_id="",
                          cluster_type="",
                          end_time="",
                          hpcjob_uuid="",
                          hpcqueue_id="",
                          iamuser_name="",
                          job_status="",
                          limit=None,
                          offset=None,
                          owner="",
                          queue_name="",
                          reverse=None,
                          run_user="",
                          search_word="",
                          sort_key="",
                          start_time="",
                          submit_type=None,
                          timestamp="",
                          verbose=None,
                          zone=""):
        operation = {
            "API": "list_jobs",
            "Method": "GET",
            "URI": "/api/job/list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if cluster_type:
            operation["Params"].update({"cluster_type": cluster_type})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if hpcjob_uuid:
            operation["Params"].update({"hpcjob_uuid": hpcjob_uuid})

        if hpcqueue_id:
            operation["Params"].update({"hpcqueue_id": hpcqueue_id})

        if iamuser_name:
            operation["Params"].update({"iamuser_name": iamuser_name})

        if job_status:
            operation["Params"].update({"job_status": job_status})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if queue_name:
            operation["Params"].update({"queue_name": queue_name})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if submit_type:
            operation["Params"].update({"submit_type": submit_type})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_jobs_validate(operation)
        return Request(self.config, operation)

    def list_jobs(self,
                  cluster_id="",
                  cluster_type="",
                  end_time="",
                  hpcjob_uuid="",
                  hpcqueue_id="",
                  iamuser_name="",
                  job_status="",
                  limit=None,
                  offset=None,
                  owner="",
                  queue_name="",
                  reverse=None,
                  run_user="",
                  search_word="",
                  sort_key="",
                  start_time="",
                  submit_type=None,
                  timestamp="",
                  verbose=None,
                  zone=""):
        req = self.list_jobs_request(cluster_id=cluster_id,
                                     cluster_type=cluster_type,
                                     end_time=end_time,
                                     hpcjob_uuid=hpcjob_uuid,
                                     hpcqueue_id=hpcqueue_id,
                                     iamuser_name=iamuser_name,
                                     job_status=job_status,
                                     limit=limit,
                                     offset=offset,
                                     owner=owner,
                                     queue_name=queue_name,
                                     reverse=reverse,
                                     run_user=run_user,
                                     search_word=search_word,
                                     sort_key=sort_key,
                                     start_time=start_time,
                                     submit_type=submit_type,
                                     timestamp=timestamp,
                                     verbose=verbose,
                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_jobs_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_jobsInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_jobsInput")

        return None

    def push_job_metrics_request(self,
                                 timestamp="",
                                 jobs=list(),
                                 last_usage_time=None,
                                 this_usage_time=None,
                                 zone=""):
        operation = {
            "API": "push_job_metrics",
            "Method": "POST",
            "URI": "/api/job/pushJobMetrics",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if jobs:
            operation["Elements"].update({"jobs": jobs})
        if last_usage_time:
            operation["Elements"].update({"last_usage_time": last_usage_time})
        if this_usage_time:
            operation["Elements"].update({"this_usage_time": this_usage_time})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.push_job_metrics_validate(operation)
        return Request(self.config, operation)

    def push_job_metrics(self,
                         timestamp="",
                         jobs=list(),
                         last_usage_time=None,
                         this_usage_time=None,
                         zone=""):
        req = self.push_job_metrics_request(timestamp=timestamp,
                                            jobs=jobs,
                                            last_usage_time=last_usage_time,
                                            this_usage_time=this_usage_time,
                                            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def push_job_metrics_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "push_job_metricsInput")

        if op["Elements"]["jobs"] is None:
            return ParameterRequiredError("jobs", "push_job_metricsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "push_job_metricsInput")

        return None

    def recover_job_status_request(self,
                                   timestamp="",
                                   cluster_id="",
                                   hpcjob_ids=list(),
                                   zone=""):
        operation = {
            "API": "recover_job_status",
            "Method": "POST",
            "URI": "/api/job/recover/status",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if hpcjob_ids:
            operation["Elements"].update({"hpcjob_ids": hpcjob_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.recover_job_status_validate(operation)
        return Request(self.config, operation)

    def recover_job_status(self,
                           timestamp="",
                           cluster_id="",
                           hpcjob_ids=list(),
                           zone=""):
        req = self.recover_job_status_request(timestamp=timestamp,
                                              cluster_id=cluster_id,
                                              hpcjob_ids=hpcjob_ids,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def recover_job_status_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "recover_job_statusInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "recover_job_statusInput")

        if op["Elements"]["hpcjob_ids"] is None:
            return ParameterRequiredError("hpcjob_ids",
                                          "recover_job_statusInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "recover_job_statusInput")

        return None

    def resume_jobs_request(self,
                            timestamp="",
                            cluster_id="",
                            job_ids=list(),
                            zone=""):
        operation = {
            "API": "resume_jobs",
            "Method": "POST",
            "URI": "/api/job/resumeJobs",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if job_ids:
            operation["Elements"].update({"job_ids": job_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.resume_jobs_validate(operation)
        return Request(self.config, operation)

    def resume_jobs(self,
                    timestamp="",
                    cluster_id="",
                    job_ids=list(),
                    zone=""):
        req = self.resume_jobs_request(timestamp=timestamp,
                                       cluster_id=cluster_id,
                                       job_ids=job_ids,
                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def resume_jobs_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "resume_jobsInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "resume_jobsInput")

        if op["Elements"]["job_ids"] is None:
            return ParameterRequiredError("job_ids", "resume_jobsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "resume_jobsInput")

        return None

    def stop_jobs_request(self,
                          timestamp="",
                          cluster_id="",
                          job_ids=list(),
                          zone=""):
        operation = {
            "API": "stop_jobs",
            "Method": "POST",
            "URI": "/api/job/stopJobs",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if job_ids:
            operation["Elements"].update({"job_ids": job_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.stop_jobs_validate(operation)
        return Request(self.config, operation)

    def stop_jobs(self, timestamp="", cluster_id="", job_ids=list(), zone=""):
        req = self.stop_jobs_request(timestamp=timestamp,
                                     cluster_id=cluster_id,
                                     job_ids=job_ids,
                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def stop_jobs_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "stop_jobsInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "stop_jobsInput")

        if op["Elements"]["job_ids"] is None:
            return ParameterRequiredError("job_ids", "stop_jobsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "stop_jobsInput")

        return None

    def submit_job_request(self,
                           timestamp="",
                           cluster_id="",
                           cmd_line="",
                           core_limit=None,
                           hpcqueue_id="",
                           input_file="",
                           mem_limit=None,
                           name="",
                           resource_limit="",
                           run_user="",
                           scheduler_queue_name="",
                           stderr_redirect_path="",
                           stdout_redirect_path="",
                           time_limit=None,
                           zone=""):
        operation = {
            "API": "submit_job",
            "Method": "POST",
            "URI": "/api/job/submitJob",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cmd_line:
            operation["Elements"].update({"cmd_line": cmd_line})
        if core_limit:
            operation["Elements"].update({"core_limit": core_limit})
        if hpcqueue_id:
            operation["Elements"].update({"hpcqueue_id": hpcqueue_id})
        if input_file:
            operation["Elements"].update({"input_file": input_file})
        if mem_limit:
            operation["Elements"].update({"mem_limit": mem_limit})
        if name:
            operation["Elements"].update({"name": name})
        if resource_limit:
            operation["Elements"].update({"resource_limit": resource_limit})
        if run_user:
            operation["Elements"].update({"run_user": run_user})
        if scheduler_queue_name:
            operation["Elements"].update(
                {"scheduler_queue_name": scheduler_queue_name})
        if stderr_redirect_path:
            operation["Elements"].update(
                {"stderr_redirect_path": stderr_redirect_path})
        if stdout_redirect_path:
            operation["Elements"].update(
                {"stdout_redirect_path": stdout_redirect_path})
        if time_limit:
            operation["Elements"].update({"time_limit": time_limit})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.submit_job_validate(operation)
        return Request(self.config, operation)

    def submit_job(self,
                   timestamp="",
                   cluster_id="",
                   cmd_line="",
                   core_limit=None,
                   hpcqueue_id="",
                   input_file="",
                   mem_limit=None,
                   name="",
                   resource_limit="",
                   run_user="",
                   scheduler_queue_name="",
                   stderr_redirect_path="",
                   stdout_redirect_path="",
                   time_limit=None,
                   zone=""):
        req = self.submit_job_request(
            timestamp=timestamp,
            cluster_id=cluster_id,
            cmd_line=cmd_line,
            core_limit=core_limit,
            hpcqueue_id=hpcqueue_id,
            input_file=input_file,
            mem_limit=mem_limit,
            name=name,
            resource_limit=resource_limit,
            run_user=run_user,
            scheduler_queue_name=scheduler_queue_name,
            stderr_redirect_path=stderr_redirect_path,
            stdout_redirect_path=stdout_redirect_path,
            time_limit=time_limit,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def submit_job_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "submit_jobInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "submit_jobInput")

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "submit_jobInput")

        if op["Elements"]["run_user"] is None:
            return ParameterRequiredError("run_user", "submit_jobInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "submit_jobInput")

        return None

    def update_ehpc_job_status_request(self,
                                       timestamp="",
                                       app_cluster_id="",
                                       data=list(),
                                       zone=""):
        operation = {
            "API": "update_ehpc_job_status",
            "Method": "POST",
            "URI": "/api/hpc/update/ehpc/jobStatus",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if app_cluster_id:
            operation["Elements"].update({"app_cluster_id": app_cluster_id})
        if data:
            operation["Elements"].update({"data": data})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.update_ehpc_job_status_validate(operation)
        return Request(self.config, operation)

    def update_ehpc_job_status(self,
                               timestamp="",
                               app_cluster_id="",
                               data=list(),
                               zone=""):
        req = self.update_ehpc_job_status_request(
            timestamp=timestamp,
            app_cluster_id=app_cluster_id,
            data=data,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def update_ehpc_job_status_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "update_ehpc_job_statusInput")

        if op["Elements"]["app_cluster_id"] is None:
            return ParameterRequiredError("app_cluster_id",
                                          "update_ehpc_job_statusInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "update_ehpc_job_statusInput")

        return None

    def update_job_status_request(self,
                                  timestamp="",
                                  job_events=list(),
                                  zone=""):
        operation = {
            "API": "update_job_status",
            "Method": "POST",
            "URI": "/api/job/updateJobStatus",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if job_events:
            operation["Elements"].update({"job_events": job_events})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.update_job_status_validate(operation)
        return Request(self.config, operation)

    def update_job_status(self, timestamp="", job_events=list(), zone=""):
        req = self.update_job_status_request(timestamp=timestamp,
                                             job_events=job_events,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def update_job_status_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "update_job_statusInput")

        if op["Elements"]["job_events"] is None:
            return ParameterRequiredError("job_events",
                                          "update_job_statusInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "update_job_statusInput")

        return None

    def hello_world_request(self, timestamp="", zone=""):
        operation = {
            "API": "hello_world",
            "Method": "GET",
            "URI": "/api/hello",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.hello_world_validate(operation)
        return Request(self.config, operation)

    def hello_world(self, timestamp="", zone=""):
        req = self.hello_world_request(timestamp=timestamp, zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def hello_world_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "hello_worldInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "hello_worldInput")

        return None

    def list_operation_request(self,
                               action_describe="",
                               directive="",
                               end_time="",
                               job_action="",
                               job_ids="",
                               jobs="",
                               limit=None,
                               offset=None,
                               owner="",
                               resource_ids="",
                               reverse=None,
                               search_word="",
                               start_time="",
                               status="",
                               timestamp="",
                               verbose=None,
                               zone=""):
        operation = {
            "API": "list_operation",
            "Method": "GET",
            "URI": "/api/operation",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if action_describe:
            operation["Params"].update({"action_describe": action_describe})

        if directive:
            operation["Params"].update({"directive": directive})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if job_action:
            operation["Params"].update({"job_action": job_action})

        if job_ids:
            operation["Params"].update({"job_ids": job_ids})

        if jobs:
            operation["Params"].update({"jobs": jobs})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if resource_ids:
            operation["Params"].update({"resource_ids": resource_ids})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_operation_validate(operation)
        return Request(self.config, operation)

    def list_operation(self,
                       action_describe="",
                       directive="",
                       end_time="",
                       job_action="",
                       job_ids="",
                       jobs="",
                       limit=None,
                       offset=None,
                       owner="",
                       resource_ids="",
                       reverse=None,
                       search_word="",
                       start_time="",
                       status="",
                       timestamp="",
                       verbose=None,
                       zone=""):
        req = self.list_operation_request(action_describe=action_describe,
                                          directive=directive,
                                          end_time=end_time,
                                          job_action=job_action,
                                          job_ids=job_ids,
                                          jobs=jobs,
                                          limit=limit,
                                          offset=offset,
                                          owner=owner,
                                          resource_ids=resource_ids,
                                          reverse=reverse,
                                          search_word=search_word,
                                          start_time=start_time,
                                          status=status,
                                          timestamp=timestamp,
                                          verbose=verbose,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_operation_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_operationInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_operationInput")

        return None

    def simulation_operation_request(self,
                                     action_describe="",
                                     directive="",
                                     end_time="",
                                     job_action="",
                                     job_ids="",
                                     jobs="",
                                     limit=None,
                                     offset=None,
                                     owner="",
                                     resource_ids="",
                                     reverse=None,
                                     search_word="",
                                     start_time="",
                                     status="",
                                     timestamp="",
                                     verbose=None,
                                     zone=""):
        operation = {
            "API": "simulation_operation",
            "Method": "GET",
            "URI": "/api/operation/simulation",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if action_describe:
            operation["Params"].update({"action_describe": action_describe})

        if directive:
            operation["Params"].update({"directive": directive})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if job_action:
            operation["Params"].update({"job_action": job_action})

        if job_ids:
            operation["Params"].update({"job_ids": job_ids})

        if jobs:
            operation["Params"].update({"jobs": jobs})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if resource_ids:
            operation["Params"].update({"resource_ids": resource_ids})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.simulation_operation_validate(operation)
        return Request(self.config, operation)

    def simulation_operation(self,
                             action_describe="",
                             directive="",
                             end_time="",
                             job_action="",
                             job_ids="",
                             jobs="",
                             limit=None,
                             offset=None,
                             owner="",
                             resource_ids="",
                             reverse=None,
                             search_word="",
                             start_time="",
                             status="",
                             timestamp="",
                             verbose=None,
                             zone=""):
        req = self.simulation_operation_request(
            action_describe=action_describe,
            directive=directive,
            end_time=end_time,
            job_action=job_action,
            job_ids=job_ids,
            jobs=jobs,
            limit=limit,
            offset=offset,
            owner=owner,
            resource_ids=resource_ids,
            reverse=reverse,
            search_word=search_word,
            start_time=start_time,
            status=status,
            timestamp=timestamp,
            verbose=verbose,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def simulation_operation_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "simulation_operationInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "simulation_operationInput")

        return None

    def disable_hpc_request(self, timestamp="", user_id=""):
        operation = {
            "API": "disable_hpc",
            "Method": "POST",
            "URI": "/api/permission/disable",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        self.disable_hpc_validate(operation)
        return Request(self.config, operation)

    def disable_hpc(self, timestamp="", user_id=""):
        req = self.disable_hpc_request(timestamp=timestamp, user_id=user_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def disable_hpc_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "disable_hpcInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id", "disable_hpcInput")

        return None

    def enable_hpc_request(self, timestamp="", user_id=""):
        operation = {
            "API": "enable_hpc",
            "Method": "POST",
            "URI": "/api/permission/enable",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        self.enable_hpc_validate(operation)
        return Request(self.config, operation)

    def enable_hpc(self, timestamp="", user_id=""):
        req = self.enable_hpc_request(timestamp=timestamp, user_id=user_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def enable_hpc_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "enable_hpcInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id", "enable_hpcInput")

        return None

    def get_hpc_status_request(self, user_id="", timestamp=""):
        operation = {
            "API": "get_hpc_status",
            "Method": "GET",
            "URI": "/api/permission/<user_id>",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }
        if user_id:
            operation["Properties"].update({"user_id": user_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        self.get_hpc_status_validate(operation)
        return Request(self.config, operation)

    def get_hpc_status(self, user_id="", timestamp=""):
        req = self.get_hpc_status_request(user_id=user_id, timestamp=timestamp)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_hpc_status_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_hpc_statusInput")

        return None

    def add_member_request(self,
                           timestamp="",
                           member_infos=list(),
                           project_id="",
                           zone=""):
        operation = {
            "API": "add_member",
            "Method": "POST",
            "URI": "/api/project/addMember",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if member_infos:
            operation["Elements"].update({"member_infos": member_infos})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_member_validate(operation)
        return Request(self.config, operation)

    def add_member(self,
                   timestamp="",
                   member_infos=list(),
                   project_id="",
                   zone=""):
        req = self.add_member_request(timestamp=timestamp,
                                      member_infos=member_infos,
                                      project_id=project_id,
                                      zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_member_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_memberInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "add_memberInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_memberInput")

        return None

    def add_project_rule_request(self,
                                 timestamp="",
                                 project_id="",
                                 rule_group_id="",
                                 rule_id="",
                                 zone=""):
        operation = {
            "API": "add_project_rule",
            "Method": "POST",
            "URI": "/api/project/addRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if rule_id:
            operation["Elements"].update({"rule_id": rule_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_project_rule_validate(operation)
        return Request(self.config, operation)

    def add_project_rule(self,
                         timestamp="",
                         project_id="",
                         rule_group_id="",
                         rule_id="",
                         zone=""):
        req = self.add_project_rule_request(timestamp=timestamp,
                                            project_id=project_id,
                                            rule_group_id=rule_group_id,
                                            rule_id=rule_id,
                                            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_project_rule_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_project_ruleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "add_project_ruleInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "add_project_ruleInput")

        if op["Elements"]["rule_id"] is None:
            return ParameterRequiredError("rule_id", "add_project_ruleInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_project_ruleInput")

        return None

    def add_project_rule_group_request(self,
                                       timestamp="",
                                       project_id="",
                                       role_id="",
                                       rule_group_id="",
                                       zone=""):
        operation = {
            "API": "add_project_rule_group",
            "Method": "POST",
            "URI": "/api/project/addRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if role_id:
            operation["Elements"].update({"role_id": role_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def add_project_rule_group(self,
                               timestamp="",
                               project_id="",
                               role_id="",
                               rule_group_id="",
                               zone=""):
        req = self.add_project_rule_group_request(timestamp=timestamp,
                                                  project_id=project_id,
                                                  role_id=role_id,
                                                  rule_group_id=rule_group_id,
                                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_project_rule_group_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "add_project_rule_groupInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "add_project_rule_groupInput")

        if op["Elements"]["role_id"] is None:
            return ParameterRequiredError("role_id",
                                          "add_project_rule_groupInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "add_project_rule_groupInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "add_project_rule_groupInput")

        return None

    def add_resource_request(self,
                             timestamp="",
                             create_time="",
                             description="",
                             enabled=None,
                             owner="",
                             project_id="",
                             resource_id="",
                             resource_type="",
                             status_time="",
                             zone=""):
        operation = {
            "API": "add_resource",
            "Method": "POST",
            "URI": "/api/project/addResource",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if create_time:
            operation["Elements"].update({"create_time": create_time})
        if description:
            operation["Elements"].update({"description": description})
        if enabled:
            operation["Elements"].update({"enabled": enabled})
        if owner:
            operation["Elements"].update({"owner": owner})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if resource_id:
            operation["Elements"].update({"resource_id": resource_id})
        if resource_type:
            operation["Elements"].update({"resource_type": resource_type})
        if status_time:
            operation["Elements"].update({"status_time": status_time})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_resource_validate(operation)
        return Request(self.config, operation)

    def add_resource(self,
                     timestamp="",
                     create_time="",
                     description="",
                     enabled=None,
                     owner="",
                     project_id="",
                     resource_id="",
                     resource_type="",
                     status_time="",
                     zone=""):
        req = self.add_resource_request(timestamp=timestamp,
                                        create_time=create_time,
                                        description=description,
                                        enabled=enabled,
                                        owner=owner,
                                        project_id=project_id,
                                        resource_id=resource_id,
                                        resource_type=resource_type,
                                        status_time=status_time,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_resource_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_resourceInput")

        if "enabled" in op["Elements"] and op["Elements"]["enabled"]:

            enabled_valid_values = ["0", "1"]
            if op["Elements"]["enabled"] not in enabled_valid_values:
                return ParameterValueNotAllowedError("enabled",
                                                     op["Elements"]["enabled"],
                                                     enabled_valid_values)

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "add_resourceInput")

        if op["Elements"]["resource_id"] is None:
            return ParameterRequiredError("resource_id", "add_resourceInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_resourceInput")

        return None

    def create_project_request(self,
                               timestamp="",
                               description="",
                               enabled=None,
                               member_infos=list(),
                               project_name="",
                               resource_id="",
                               zone=""):
        operation = {
            "API": "create_project",
            "Method": "POST",
            "URI": "/api/project/create",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if enabled:
            operation["Elements"].update({"enabled": enabled})
        if member_infos:
            operation["Elements"].update({"member_infos": member_infos})
        if project_name:
            operation["Elements"].update({"project_name": project_name})
        if resource_id:
            operation["Elements"].update({"resource_id": resource_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_project_validate(operation)
        return Request(self.config, operation)

    def create_project(self,
                       timestamp="",
                       description="",
                       enabled=None,
                       member_infos=list(),
                       project_name="",
                       resource_id="",
                       zone=""):
        req = self.create_project_request(timestamp=timestamp,
                                          description=description,
                                          enabled=enabled,
                                          member_infos=member_infos,
                                          project_name=project_name,
                                          resource_id=resource_id,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_project_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "create_projectInput")

        if "enabled" in op["Elements"] and op["Elements"]["enabled"]:

            enabled_valid_values = ["0", "1"]
            if op["Elements"]["enabled"] not in enabled_valid_values:
                return ParameterValueNotAllowedError("enabled",
                                                     op["Elements"]["enabled"],
                                                     enabled_valid_values)

        if op["Elements"]["resource_id"] is None:
            return ParameterRequiredError("resource_id", "create_projectInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "create_projectInput")

        return None

    def create_project_role_request(self,
                                    timestamp="",
                                    create_time="",
                                    description="",
                                    owner="",
                                    project_id="",
                                    readonly=None,
                                    role_id="",
                                    role_name="",
                                    role_type="",
                                    status="",
                                    status_time="",
                                    zone=""):
        operation = {
            "API": "create_project_role",
            "Method": "POST",
            "URI": "/api/project/createRole",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if create_time:
            operation["Elements"].update({"create_time": create_time})
        if description:
            operation["Elements"].update({"description": description})
        if owner:
            operation["Elements"].update({"owner": owner})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if readonly:
            operation["Elements"].update({"readonly": readonly})
        if role_id:
            operation["Elements"].update({"role_id": role_id})
        if role_name:
            operation["Elements"].update({"role_name": role_name})
        if role_type:
            operation["Elements"].update({"role_type": role_type})
        if status:
            operation["Elements"].update({"status": status})
        if status_time:
            operation["Elements"].update({"status_time": status_time})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_project_role_validate(operation)
        return Request(self.config, operation)

    def create_project_role(self,
                            timestamp="",
                            create_time="",
                            description="",
                            owner="",
                            project_id="",
                            readonly=None,
                            role_id="",
                            role_name="",
                            role_type="",
                            status="",
                            status_time="",
                            zone=""):
        req = self.create_project_role_request(timestamp=timestamp,
                                               create_time=create_time,
                                               description=description,
                                               owner=owner,
                                               project_id=project_id,
                                               readonly=readonly,
                                               role_id=role_id,
                                               role_name=role_name,
                                               role_type=role_type,
                                               status=status,
                                               status_time=status_time,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_project_role_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "create_project_roleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "create_project_roleInput")

        if "readonly" in op["Elements"] and op["Elements"]["readonly"]:

            readonly_valid_values = ["0", "1"]
            if op["Elements"]["readonly"] not in readonly_valid_values:
                return ParameterValueNotAllowedError(
                    "readonly", op["Elements"]["readonly"],
                    readonly_valid_values)

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "create_project_roleInput")

        return None

    def create_project_rule_request(self,
                                    timestamp="",
                                    create_time="",
                                    description="",
                                    owner="",
                                    project_id="",
                                    readonly=None,
                                    rule_id="",
                                    status="",
                                    status_time="",
                                    zone=""):
        operation = {
            "API": "create_project_rule",
            "Method": "POST",
            "URI": "/api/project/createRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if create_time:
            operation["Elements"].update({"create_time": create_time})
        if description:
            operation["Elements"].update({"description": description})
        if owner:
            operation["Elements"].update({"owner": owner})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if readonly:
            operation["Elements"].update({"readonly": readonly})
        if rule_id:
            operation["Elements"].update({"rule_id": rule_id})
        if status:
            operation["Elements"].update({"status": status})
        if status_time:
            operation["Elements"].update({"status_time": status_time})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_project_rule_validate(operation)
        return Request(self.config, operation)

    def create_project_rule(self,
                            timestamp="",
                            create_time="",
                            description="",
                            owner="",
                            project_id="",
                            readonly=None,
                            rule_id="",
                            status="",
                            status_time="",
                            zone=""):
        req = self.create_project_rule_request(timestamp=timestamp,
                                               create_time=create_time,
                                               description=description,
                                               owner=owner,
                                               project_id=project_id,
                                               readonly=readonly,
                                               rule_id=rule_id,
                                               status=status,
                                               status_time=status_time,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_project_rule_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "create_project_ruleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "create_project_ruleInput")

        if "readonly" in op["Elements"] and op["Elements"]["readonly"]:

            readonly_valid_values = ["0", "1"]
            if op["Elements"]["readonly"] not in readonly_valid_values:
                return ParameterValueNotAllowedError(
                    "readonly", op["Elements"]["readonly"],
                    readonly_valid_values)

        if op["Elements"]["rule_id"] is None:
            return ParameterRequiredError("rule_id",
                                          "create_project_ruleInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "create_project_ruleInput")

        return None

    def create_project_rule_group_request(self,
                                          timestamp="",
                                          create_time="",
                                          description="",
                                          owner="",
                                          project_id="",
                                          readonly=None,
                                          rule_group_id="",
                                          status="",
                                          status_time="",
                                          zone=""):
        operation = {
            "API": "create_project_rule_group",
            "Method": "POST",
            "URI": "/api/project/createRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if create_time:
            operation["Elements"].update({"create_time": create_time})
        if description:
            operation["Elements"].update({"description": description})
        if owner:
            operation["Elements"].update({"owner": owner})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if readonly:
            operation["Elements"].update({"readonly": readonly})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if status:
            operation["Elements"].update({"status": status})
        if status_time:
            operation["Elements"].update({"status_time": status_time})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.create_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def create_project_rule_group(self,
                                  timestamp="",
                                  create_time="",
                                  description="",
                                  owner="",
                                  project_id="",
                                  readonly=None,
                                  rule_group_id="",
                                  status="",
                                  status_time="",
                                  zone=""):
        req = self.create_project_rule_group_request(
            timestamp=timestamp,
            create_time=create_time,
            description=description,
            owner=owner,
            project_id=project_id,
            readonly=readonly,
            rule_group_id=rule_group_id,
            status=status,
            status_time=status_time,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def create_project_rule_group_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "create_project_rule_groupInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "create_project_rule_groupInput")

        if "readonly" in op["Elements"] and op["Elements"]["readonly"]:

            readonly_valid_values = ["0", "1"]
            if op["Elements"]["readonly"] not in readonly_valid_values:
                return ParameterValueNotAllowedError(
                    "readonly", op["Elements"]["readonly"],
                    readonly_valid_values)

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "create_project_rule_groupInput")

        return None

    def del_member_request(self,
                           timestamp="",
                           member_id=list(),
                           project_id="",
                           zone=""):
        operation = {
            "API": "del_member",
            "Method": "POST",
            "URI": "/api/project/delMember",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if member_id:
            operation["Elements"].update({"member_id": member_id})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_member_validate(operation)
        return Request(self.config, operation)

    def del_member(self,
                   timestamp="",
                   member_id=list(),
                   project_id="",
                   zone=""):
        req = self.del_member_request(timestamp=timestamp,
                                      member_id=member_id,
                                      project_id=project_id,
                                      zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_member_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_memberInput")

        if op["Elements"]["member_id"] is None:
            return ParameterRequiredError("member_id", "del_memberInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "del_memberInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_memberInput")

        return None

    def del_project_rule_request(self,
                                 timestamp="",
                                 project_id="",
                                 rule_group_id="",
                                 rule_id="",
                                 zone=""):
        operation = {
            "API": "del_project_rule",
            "Method": "POST",
            "URI": "/api/project/delRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if rule_id:
            operation["Elements"].update({"rule_id": rule_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_project_rule_validate(operation)
        return Request(self.config, operation)

    def del_project_rule(self,
                         timestamp="",
                         project_id="",
                         rule_group_id="",
                         rule_id="",
                         zone=""):
        req = self.del_project_rule_request(timestamp=timestamp,
                                            project_id=project_id,
                                            rule_group_id=rule_group_id,
                                            rule_id=rule_id,
                                            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_project_rule_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_project_ruleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "del_project_ruleInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "del_project_ruleInput")

        if op["Elements"]["rule_id"] is None:
            return ParameterRequiredError("rule_id", "del_project_ruleInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_project_ruleInput")

        return None

    def del_project_rule_group_request(self,
                                       timestamp="",
                                       project_id="",
                                       role_id="",
                                       rule_group_id="",
                                       zone=""):
        operation = {
            "API": "del_project_rule_group",
            "Method": "POST",
            "URI": "/api/project/delRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if role_id:
            operation["Elements"].update({"role_id": role_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def del_project_rule_group(self,
                               timestamp="",
                               project_id="",
                               role_id="",
                               rule_group_id="",
                               zone=""):
        req = self.del_project_rule_group_request(timestamp=timestamp,
                                                  project_id=project_id,
                                                  role_id=role_id,
                                                  rule_group_id=rule_group_id,
                                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_project_rule_group_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "del_project_rule_groupInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "del_project_rule_groupInput")

        if op["Elements"]["role_id"] is None:
            return ParameterRequiredError("role_id",
                                          "del_project_rule_groupInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "del_project_rule_groupInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "del_project_rule_groupInput")

        return None

    def del_resource_request(self,
                             timestamp="",
                             project_id="",
                             resource_id=list(),
                             zone=""):
        operation = {
            "API": "del_resource",
            "Method": "POST",
            "URI": "/api/project/delResource",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if resource_id:
            operation["Elements"].update({"resource_id": resource_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_resource_validate(operation)
        return Request(self.config, operation)

    def del_resource(self,
                     timestamp="",
                     project_id="",
                     resource_id=list(),
                     zone=""):
        req = self.del_resource_request(timestamp=timestamp,
                                        project_id=project_id,
                                        resource_id=resource_id,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_resource_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_resourceInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "del_resourceInput")

        if op["Elements"]["resource_id"] is None:
            return ParameterRequiredError("resource_id", "del_resourceInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_resourceInput")

        return None

    def destroy_project_request(self,
                                timestamp="",
                                project_id=list(),
                                unlease="",
                                zone=""):
        operation = {
            "API": "destroy_project",
            "Method": "POST",
            "URI": "/api/project/destroy",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if unlease:
            operation["Elements"].update({"unlease": unlease})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.destroy_project_validate(operation)
        return Request(self.config, operation)

    def destroy_project(self,
                        timestamp="",
                        project_id=list(),
                        unlease="",
                        zone=""):
        req = self.destroy_project_request(timestamp=timestamp,
                                           project_id=project_id,
                                           unlease=unlease,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def destroy_project_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "destroy_projectInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "destroy_projectInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "destroy_projectInput")

        return None

    def destroy_project_role_request(self,
                                     timestamp="",
                                     project_id="",
                                     role_id=list(),
                                     unlease="",
                                     zone=""):
        operation = {
            "API": "destroy_project_role",
            "Method": "POST",
            "URI": "/api/project/destroyRole",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if role_id:
            operation["Elements"].update({"role_id": role_id})
        if unlease:
            operation["Elements"].update({"unlease": unlease})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.destroy_project_role_validate(operation)
        return Request(self.config, operation)

    def destroy_project_role(self,
                             timestamp="",
                             project_id="",
                             role_id=list(),
                             unlease="",
                             zone=""):
        req = self.destroy_project_role_request(timestamp=timestamp,
                                                project_id=project_id,
                                                role_id=role_id,
                                                unlease=unlease,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def destroy_project_role_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "destroy_project_roleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "destroy_project_roleInput")

        if op["Elements"]["role_id"] is None:
            return ParameterRequiredError("role_id",
                                          "destroy_project_roleInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "destroy_project_roleInput")

        return None

    def destroy_project_rule_request(self,
                                     timestamp="",
                                     project_id="",
                                     rule_id=list(),
                                     unlease="",
                                     zone=""):
        operation = {
            "API": "destroy_project_rule",
            "Method": "POST",
            "URI": "/api/project/destroyRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_id:
            operation["Elements"].update({"rule_id": rule_id})
        if unlease:
            operation["Elements"].update({"unlease": unlease})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.destroy_project_rule_validate(operation)
        return Request(self.config, operation)

    def destroy_project_rule(self,
                             timestamp="",
                             project_id="",
                             rule_id=list(),
                             unlease="",
                             zone=""):
        req = self.destroy_project_rule_request(timestamp=timestamp,
                                                project_id=project_id,
                                                rule_id=rule_id,
                                                unlease=unlease,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def destroy_project_rule_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "destroy_project_ruleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "destroy_project_ruleInput")

        if op["Elements"]["rule_id"] is None:
            return ParameterRequiredError("rule_id",
                                          "destroy_project_ruleInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "destroy_project_ruleInput")

        return None

    def destroy_project_rule_group_request(self,
                                           timestamp="",
                                           project_id="",
                                           rule_group_id=list(),
                                           unlease="",
                                           zone=""):
        operation = {
            "API": "destroy_project_rule_group",
            "Method": "POST",
            "URI": "/api/project/destroyRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if unlease:
            operation["Elements"].update({"unlease": unlease})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.destroy_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def destroy_project_rule_group(self,
                                   timestamp="",
                                   project_id="",
                                   rule_group_id=list(),
                                   unlease="",
                                   zone=""):
        req = self.destroy_project_rule_group_request(
            timestamp=timestamp,
            project_id=project_id,
            rule_group_id=rule_group_id,
            unlease=unlease,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def destroy_project_rule_group_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "destroy_project_rule_groupInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "destroy_project_rule_groupInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "destroy_project_rule_groupInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "destroy_project_rule_groupInput")

        return None

    def init_configuration_request(self, timestamp="", zone=""):
        operation = {
            "API": "init_configuration",
            "Method": "POST",
            "URI": "/api/project/initConfiguration",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if zone:
            operation["Elements"].update({"zone": zone})
        self.init_configuration_validate(operation)
        return Request(self.config, operation)

    def init_configuration(self, timestamp="", zone=""):
        req = self.init_configuration_request(timestamp=timestamp, zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def init_configuration_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "init_configurationInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "init_configurationInput")

        return None

    def list_member_request(self,
                            limit=None,
                            member_account="",
                            member_id="",
                            member_name="",
                            member_user="",
                            offset=None,
                            project_id="",
                            reverse=None,
                            role_type="",
                            run_user="",
                            search_word="",
                            sort_key="",
                            timestamp="",
                            verbose=None,
                            zone=""):
        operation = {
            "API": "list_member",
            "Method": "GET",
            "URI": "/api/project/listMember",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if member_account:
            operation["Params"].update({"member_account": member_account})

        if member_id:
            operation["Params"].update({"member_id": member_id})

        if member_name:
            operation["Params"].update({"member_name": member_name})

        if member_user:
            operation["Params"].update({"member_user": member_user})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if role_type:
            operation["Params"].update({"role_type": role_type})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_member_validate(operation)
        return Request(self.config, operation)

    def list_member(self,
                    limit=None,
                    member_account="",
                    member_id="",
                    member_name="",
                    member_user="",
                    offset=None,
                    project_id="",
                    reverse=None,
                    role_type="",
                    run_user="",
                    search_word="",
                    sort_key="",
                    timestamp="",
                    verbose=None,
                    zone=""):
        req = self.list_member_request(limit=limit,
                                       member_account=member_account,
                                       member_id=member_id,
                                       member_name=member_name,
                                       member_user=member_user,
                                       offset=offset,
                                       project_id=project_id,
                                       reverse=reverse,
                                       role_type=role_type,
                                       run_user=run_user,
                                       search_word=search_word,
                                       sort_key=sort_key,
                                       timestamp=timestamp,
                                       verbose=verbose,
                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_member_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_memberInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_memberInput")

        return None

    def list_project_request(self,
                             limit=None,
                             offset=None,
                             project_id="",
                             resource_id="",
                             reverse=None,
                             run_user="",
                             search_word="",
                             sort_key="",
                             status="",
                             timestamp="",
                             verbose=None,
                             zone=""):
        operation = {
            "API": "list_project",
            "Method": "GET",
            "URI": "/api/project/list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if resource_id:
            operation["Params"].update({"resource_id": resource_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_project_validate(operation)
        return Request(self.config, operation)

    def list_project(self,
                     limit=None,
                     offset=None,
                     project_id="",
                     resource_id="",
                     reverse=None,
                     run_user="",
                     search_word="",
                     sort_key="",
                     status="",
                     timestamp="",
                     verbose=None,
                     zone=""):
        req = self.list_project_request(limit=limit,
                                        offset=offset,
                                        project_id=project_id,
                                        resource_id=resource_id,
                                        reverse=reverse,
                                        run_user=run_user,
                                        search_word=search_word,
                                        sort_key=sort_key,
                                        status=status,
                                        timestamp=timestamp,
                                        verbose=verbose,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_project_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_projectInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_projectInput")

        return None

    def list_project_role_request(self,
                                  limit=None,
                                  offset=None,
                                  project_id="",
                                  reverse=None,
                                  run_user="",
                                  search_word="",
                                  sort_key="",
                                  status="",
                                  timestamp="",
                                  verbose=None,
                                  zone=""):
        operation = {
            "API": "list_project_role",
            "Method": "GET",
            "URI": "/api/project/listRole",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_project_role_validate(operation)
        return Request(self.config, operation)

    def list_project_role(self,
                          limit=None,
                          offset=None,
                          project_id="",
                          reverse=None,
                          run_user="",
                          search_word="",
                          sort_key="",
                          status="",
                          timestamp="",
                          verbose=None,
                          zone=""):
        req = self.list_project_role_request(limit=limit,
                                             offset=offset,
                                             project_id=project_id,
                                             reverse=reverse,
                                             run_user=run_user,
                                             search_word=search_word,
                                             sort_key=sort_key,
                                             status=status,
                                             timestamp=timestamp,
                                             verbose=verbose,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_project_role_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_project_roleInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_project_roleInput")

        return None

    def list_project_rule_request(self,
                                  limit=None,
                                  offset=None,
                                  project_id="",
                                  reverse=None,
                                  run_user="",
                                  search_word="",
                                  sort_key="",
                                  status="",
                                  timestamp="",
                                  verbose=None,
                                  zone=""):
        operation = {
            "API": "list_project_rule",
            "Method": "GET",
            "URI": "/api/project/listRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_project_rule_validate(operation)
        return Request(self.config, operation)

    def list_project_rule(self,
                          limit=None,
                          offset=None,
                          project_id="",
                          reverse=None,
                          run_user="",
                          search_word="",
                          sort_key="",
                          status="",
                          timestamp="",
                          verbose=None,
                          zone=""):
        req = self.list_project_rule_request(limit=limit,
                                             offset=offset,
                                             project_id=project_id,
                                             reverse=reverse,
                                             run_user=run_user,
                                             search_word=search_word,
                                             sort_key=sort_key,
                                             status=status,
                                             timestamp=timestamp,
                                             verbose=verbose,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_project_rule_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_project_ruleInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_project_ruleInput")

        return None

    def list_project_rule_group_request(self,
                                        limit=None,
                                        offset=None,
                                        project_id="",
                                        reverse=None,
                                        run_user="",
                                        search_word="",
                                        sort_key="",
                                        status="",
                                        timestamp="",
                                        verbose=None,
                                        zone=""):
        operation = {
            "API": "list_project_rule_group",
            "Method": "GET",
            "URI": "/api/project/listRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def list_project_rule_group(self,
                                limit=None,
                                offset=None,
                                project_id="",
                                reverse=None,
                                run_user="",
                                search_word="",
                                sort_key="",
                                status="",
                                timestamp="",
                                verbose=None,
                                zone=""):
        req = self.list_project_rule_group_request(limit=limit,
                                                   offset=offset,
                                                   project_id=project_id,
                                                   reverse=reverse,
                                                   run_user=run_user,
                                                   search_word=search_word,
                                                   sort_key=sort_key,
                                                   status=status,
                                                   timestamp=timestamp,
                                                   verbose=verbose,
                                                   zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_project_rule_group_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_project_rule_groupInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "list_project_rule_groupInput")

        return None

    def list_resource_request(self,
                              limit=None,
                              offset=None,
                              project_id="",
                              resource_id="",
                              reverse=None,
                              run_user="",
                              search_word="",
                              sort_key="",
                              timestamp="",
                              verbose=None,
                              zone=""):
        operation = {
            "API": "list_resource",
            "Method": "GET",
            "URI": "/api/project/listResource",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if project_id:
            operation["Params"].update({"project_id": project_id})

        if resource_id:
            operation["Params"].update({"resource_id": resource_id})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_resource_validate(operation)
        return Request(self.config, operation)

    def list_resource(self,
                      limit=None,
                      offset=None,
                      project_id="",
                      resource_id="",
                      reverse=None,
                      run_user="",
                      search_word="",
                      sort_key="",
                      timestamp="",
                      verbose=None,
                      zone=""):
        req = self.list_resource_request(limit=limit,
                                         offset=offset,
                                         project_id=project_id,
                                         resource_id=resource_id,
                                         reverse=reverse,
                                         run_user=run_user,
                                         search_word=search_word,
                                         sort_key=sort_key,
                                         timestamp=timestamp,
                                         verbose=verbose,
                                         zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_resource_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_resourceInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_resourceInput")

        return None

    def modify_member_request(self,
                              timestamp="",
                              description="",
                              enabled=None,
                              member_id="",
                              member_name="",
                              project_id="",
                              role="",
                              role_type="",
                              zone=""):
        operation = {
            "API": "modify_member",
            "Method": "POST",
            "URI": "/api/project/modifyMember",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if enabled:
            operation["Elements"].update({"enabled": enabled})
        if member_id:
            operation["Elements"].update({"member_id": member_id})
        if member_name:
            operation["Elements"].update({"member_name": member_name})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if role:
            operation["Elements"].update({"role": role})
        if role_type:
            operation["Elements"].update({"role_type": role_type})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_member_validate(operation)
        return Request(self.config, operation)

    def modify_member(self,
                      timestamp="",
                      description="",
                      enabled=None,
                      member_id="",
                      member_name="",
                      project_id="",
                      role="",
                      role_type="",
                      zone=""):
        req = self.modify_member_request(timestamp=timestamp,
                                         description=description,
                                         enabled=enabled,
                                         member_id=member_id,
                                         member_name=member_name,
                                         project_id=project_id,
                                         role=role,
                                         role_type=role_type,
                                         zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_member_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_memberInput")

        if "enabled" in op["Elements"] and op["Elements"]["enabled"]:

            enabled_valid_values = ["0", "1"]
            if op["Elements"]["enabled"] not in enabled_valid_values:
                return ParameterValueNotAllowedError("enabled",
                                                     op["Elements"]["enabled"],
                                                     enabled_valid_values)

        if op["Elements"]["member_id"] is None:
            return ParameterRequiredError("member_id", "modify_memberInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "modify_memberInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_memberInput")

        return None

    def modify_project_request(self,
                               timestamp="",
                               description="",
                               enabled=None,
                               project_id="",
                               project_name="",
                               zone=""):
        operation = {
            "API": "modify_project",
            "Method": "POST",
            "URI": "/api/project/modify",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if enabled:
            operation["Elements"].update({"enabled": enabled})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if project_name:
            operation["Elements"].update({"project_name": project_name})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_project_validate(operation)
        return Request(self.config, operation)

    def modify_project(self,
                       timestamp="",
                       description="",
                       enabled=None,
                       project_id="",
                       project_name="",
                       zone=""):
        req = self.modify_project_request(timestamp=timestamp,
                                          description=description,
                                          enabled=enabled,
                                          project_id=project_id,
                                          project_name=project_name,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_project_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_projectInput")

        if "enabled" in op["Elements"] and op["Elements"]["enabled"]:

            enabled_valid_values = ["0", "1"]
            if op["Elements"]["enabled"] not in enabled_valid_values:
                return ParameterValueNotAllowedError("enabled",
                                                     op["Elements"]["enabled"],
                                                     enabled_valid_values)

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "modify_projectInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_projectInput")

        return None

    def modify_project_role_request(self,
                                    timestamp="",
                                    description="",
                                    project_id="",
                                    role_id="",
                                    status="",
                                    zone=""):
        operation = {
            "API": "modify_project_role",
            "Method": "POST",
            "URI": "/api/project/modifyRole",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if role_id:
            operation["Elements"].update({"role_id": role_id})
        if status:
            operation["Elements"].update({"status": status})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_project_role_validate(operation)
        return Request(self.config, operation)

    def modify_project_role(self,
                            timestamp="",
                            description="",
                            project_id="",
                            role_id="",
                            status="",
                            zone=""):
        req = self.modify_project_role_request(timestamp=timestamp,
                                               description=description,
                                               project_id=project_id,
                                               role_id=role_id,
                                               status=status,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_project_role_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_project_roleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "modify_project_roleInput")

        if op["Elements"]["role_id"] is None:
            return ParameterRequiredError("role_id",
                                          "modify_project_roleInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_project_roleInput")

        return None

    def modify_project_rule_request(self,
                                    timestamp="",
                                    description="",
                                    project_id="",
                                    rule_id="",
                                    status="",
                                    zone=""):
        operation = {
            "API": "modify_project_rule",
            "Method": "POST",
            "URI": "/api/project/modifyRule",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_id:
            operation["Elements"].update({"rule_id": rule_id})
        if status:
            operation["Elements"].update({"status": status})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_project_rule_validate(operation)
        return Request(self.config, operation)

    def modify_project_rule(self,
                            timestamp="",
                            description="",
                            project_id="",
                            rule_id="",
                            status="",
                            zone=""):
        req = self.modify_project_rule_request(timestamp=timestamp,
                                               description=description,
                                               project_id=project_id,
                                               rule_id=rule_id,
                                               status=status,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_project_rule_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_project_ruleInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "modify_project_ruleInput")

        if op["Elements"]["rule_id"] is None:
            return ParameterRequiredError("rule_id",
                                          "modify_project_ruleInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_project_ruleInput")

        return None

    def modify_project_rule_group_request(self,
                                          timestamp="",
                                          description="",
                                          project_id="",
                                          rule_group_id="",
                                          status="",
                                          zone=""):
        operation = {
            "API": "modify_project_rule_group",
            "Method": "POST",
            "URI": "/api/project/modifyRuleGroup",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if rule_group_id:
            operation["Elements"].update({"rule_group_id": rule_group_id})
        if status:
            operation["Elements"].update({"status": status})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_project_rule_group_validate(operation)
        return Request(self.config, operation)

    def modify_project_rule_group(self,
                                  timestamp="",
                                  description="",
                                  project_id="",
                                  rule_group_id="",
                                  status="",
                                  zone=""):
        req = self.modify_project_rule_group_request(
            timestamp=timestamp,
            description=description,
            project_id=project_id,
            rule_group_id=rule_group_id,
            status=status,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_project_rule_group_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_project_rule_groupInput")

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id",
                                          "modify_project_rule_groupInput")

        if op["Elements"]["rule_group_id"] is None:
            return ParameterRequiredError("rule_group_id",
                                          "modify_project_rule_groupInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["enabled", "distabled"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "modify_project_rule_groupInput")

        return None

    def modify_resource_request(self,
                                timestamp="",
                                description="",
                                enabled=None,
                                project_id="",
                                resource_id="",
                                zone=""):
        operation = {
            "API": "modify_resource",
            "Method": "POST",
            "URI": "/api/project/modifyResourse",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if description:
            operation["Elements"].update({"description": description})
        if enabled:
            operation["Elements"].update({"enabled": enabled})
        if project_id:
            operation["Elements"].update({"project_id": project_id})
        if resource_id:
            operation["Elements"].update({"resource_id": resource_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_resource_validate(operation)
        return Request(self.config, operation)

    def modify_resource(self,
                        timestamp="",
                        description="",
                        enabled=None,
                        project_id="",
                        resource_id="",
                        zone=""):
        req = self.modify_resource_request(timestamp=timestamp,
                                           description=description,
                                           enabled=enabled,
                                           project_id=project_id,
                                           resource_id=resource_id,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_resource_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_resourceInput")

        if "enabled" in op["Elements"] and op["Elements"]["enabled"]:

            enabled_valid_values = ["0", "1"]
            if op["Elements"]["enabled"] not in enabled_valid_values:
                return ParameterValueNotAllowedError("enabled",
                                                     op["Elements"]["enabled"],
                                                     enabled_valid_values)

        if op["Elements"]["project_id"] is None:
            return ParameterRequiredError("project_id", "modify_resourceInput")

        if op["Elements"]["resource_id"] is None:
            return ParameterRequiredError("resource_id",
                                          "modify_resourceInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_resourceInput")

        return None

    def add_ehpc_queue_request(self,
                               timestamp="",
                               allow_accounts="",
                               cluster_id="",
                               default_queue=None,
                               deny_accounts="",
                               max_time="",
                               min_node=None,
                               name="",
                               status=None,
                               user_group="",
                               zone=""):
        operation = {
            "API": "add_ehpc_queue",
            "Method": "POST",
            "URI": "/api/queue/ehpc/addQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if allow_accounts:
            operation["Elements"].update({"allow_accounts": allow_accounts})
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if default_queue:
            operation["Elements"].update({"default_queue": default_queue})
        if deny_accounts:
            operation["Elements"].update({"deny_accounts": deny_accounts})
        if max_time:
            operation["Elements"].update({"max_time": max_time})
        if min_node:
            operation["Elements"].update({"min_node": min_node})
        if name:
            operation["Elements"].update({"name": name})
        if status:
            operation["Elements"].update({"status": status})
        if user_group:
            operation["Elements"].update({"user_group": user_group})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_ehpc_queue_validate(operation)
        return Request(self.config, operation)

    def add_ehpc_queue(self,
                       timestamp="",
                       allow_accounts="",
                       cluster_id="",
                       default_queue=None,
                       deny_accounts="",
                       max_time="",
                       min_node=None,
                       name="",
                       status=None,
                       user_group="",
                       zone=""):
        req = self.add_ehpc_queue_request(timestamp=timestamp,
                                          allow_accounts=allow_accounts,
                                          cluster_id=cluster_id,
                                          default_queue=default_queue,
                                          deny_accounts=deny_accounts,
                                          max_time=max_time,
                                          min_node=min_node,
                                          name=name,
                                          status=status,
                                          user_group=user_group,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_ehpc_queue_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_ehpc_queueInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "add_ehpc_queueInput")

        if "default_queue" in op["Elements"] and op["Elements"][
                "default_queue"]:

            default_queue_valid_values = ["0", "1"]
            if op["Elements"][
                    "default_queue"] not in default_queue_valid_values:
                return ParameterValueNotAllowedError(
                    "default_queue", op["Elements"]["default_queue"],
                    default_queue_valid_values)

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "add_ehpc_queueInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["0", "1"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_ehpc_queueInput")

        return None

    def add_ehpc_queue_nodes_request(self,
                                     timestamp="",
                                     cluster_id="",
                                     hpcqueue_id="",
                                     nodelist=list(),
                                     zone=""):
        operation = {
            "API": "add_ehpc_queue_nodes",
            "Method": "POST",
            "URI": "/api/queue/ehpc/addNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if hpcqueue_id:
            operation["Elements"].update({"hpcqueue_id": hpcqueue_id})
        if nodelist:
            operation["Elements"].update({"nodelist": nodelist})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_ehpc_queue_nodes_validate(operation)
        return Request(self.config, operation)

    def add_ehpc_queue_nodes(self,
                             timestamp="",
                             cluster_id="",
                             hpcqueue_id="",
                             nodelist=list(),
                             zone=""):
        req = self.add_ehpc_queue_nodes_request(timestamp=timestamp,
                                                cluster_id=cluster_id,
                                                hpcqueue_id=hpcqueue_id,
                                                nodelist=nodelist,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_ehpc_queue_nodes_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "add_ehpc_queue_nodesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "add_ehpc_queue_nodesInput")

        if op["Elements"]["hpcqueue_id"] is None:
            return ParameterRequiredError("hpcqueue_id",
                                          "add_ehpc_queue_nodesInput")

        if op["Elements"]["nodelist"] is None:
            return ParameterRequiredError("nodelist",
                                          "add_ehpc_queue_nodesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_ehpc_queue_nodesInput")

        return None

    def add_phy_queue_request(self,
                              timestamp="",
                              belong=None,
                              categories="",
                              hpq_name="",
                              scheduler_queue_name="",
                              type_id="",
                              user_group="",
                              zone=""):
        operation = {
            "API": "add_phy_queue",
            "Method": "POST",
            "URI": "/api/queue/hpc/addPhyQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if belong:
            operation["Elements"].update({"belong": belong})
        if categories:
            operation["Elements"].update({"categories": categories})
        if hpq_name:
            operation["Elements"].update({"hpq_name": hpq_name})
        if scheduler_queue_name:
            operation["Elements"].update(
                {"scheduler_queue_name": scheduler_queue_name})
        if type_id:
            operation["Elements"].update({"type_id": type_id})
        if user_group:
            operation["Elements"].update({"user_group": user_group})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_phy_queue_validate(operation)
        return Request(self.config, operation)

    def add_phy_queue(self,
                      timestamp="",
                      belong=None,
                      categories="",
                      hpq_name="",
                      scheduler_queue_name="",
                      type_id="",
                      user_group="",
                      zone=""):
        req = self.add_phy_queue_request(
            timestamp=timestamp,
            belong=belong,
            categories=categories,
            hpq_name=hpq_name,
            scheduler_queue_name=scheduler_queue_name,
            type_id=type_id,
            user_group=user_group,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_phy_queue_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_phy_queueInput")

        if op["Elements"]["belong"] is None:
            return ParameterRequiredError("belong", "add_phy_queueInput")

        if "belong" in op["Elements"] and op["Elements"]["belong"]:

            belong_valid_values = ["0", "1"]
            if op["Elements"]["belong"] not in belong_valid_values:
                return ParameterValueNotAllowedError("belong",
                                                     op["Elements"]["belong"],
                                                     belong_valid_values)

        if op["Elements"]["categories"] is None:
            return ParameterRequiredError("categories", "add_phy_queueInput")

        if op["Elements"]["hpq_name"] is None:
            return ParameterRequiredError("hpq_name", "add_phy_queueInput")

        if op["Elements"]["scheduler_queue_name"] is None:
            return ParameterRequiredError("scheduler_queue_name",
                                          "add_phy_queueInput")

        if op["Elements"]["type_id"] is None:
            return ParameterRequiredError("type_id", "add_phy_queueInput")

        if op["Elements"]["user_group"] is None:
            return ParameterRequiredError("user_group", "add_phy_queueInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_phy_queueInput")

        return None

    def add_queue_type_request(self,
                               timestamp="",
                               cpu_num=None,
                               gpu_num=None,
                               mem_size=None,
                               name="",
                               node_num=None,
                               zone=""):
        operation = {
            "API": "add_queue_type",
            "Method": "POST",
            "URI": "/api/queue/queuetype/addQueueType",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cpu_num:
            operation["Elements"].update({"cpu_num": cpu_num})
        if gpu_num:
            operation["Elements"].update({"gpu_num": gpu_num})
        if mem_size:
            operation["Elements"].update({"mem_size": mem_size})
        if name:
            operation["Elements"].update({"name": name})
        if node_num:
            operation["Elements"].update({"node_num": node_num})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_queue_type_validate(operation)
        return Request(self.config, operation)

    def add_queue_type(self,
                       timestamp="",
                       cpu_num=None,
                       gpu_num=None,
                       mem_size=None,
                       name="",
                       node_num=None,
                       zone=""):
        req = self.add_queue_type_request(timestamp=timestamp,
                                          cpu_num=cpu_num,
                                          gpu_num=gpu_num,
                                          mem_size=mem_size,
                                          name=name,
                                          node_num=node_num,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_queue_type_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_queue_typeInput")

        if op["Elements"]["cpu_num"] is None:
            return ParameterRequiredError("cpu_num", "add_queue_typeInput")

        if op["Elements"]["gpu_num"] is None:
            return ParameterRequiredError("gpu_num", "add_queue_typeInput")

        if op["Elements"]["mem_size"] is None:
            return ParameterRequiredError("mem_size", "add_queue_typeInput")

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "add_queue_typeInput")

        if op["Elements"]["node_num"] is None:
            return ParameterRequiredError("node_num", "add_queue_typeInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_queue_typeInput")

        return None

    def bind_private_queue_request(self,
                                   timestamp="",
                                   cluster_id="",
                                   duration=None,
                                   is_auto_renewal=None,
                                   name="",
                                   paid_type="",
                                   type_id="",
                                   zone=""):
        operation = {
            "API": "bind_private_queue",
            "Method": "POST",
            "URI": "/api/queue/bindPrivateQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if duration:
            operation["Elements"].update({"duration": duration})
        if is_auto_renewal:
            operation["Elements"].update({"is_auto_renewal": is_auto_renewal})
        if name:
            operation["Elements"].update({"name": name})
        if paid_type:
            operation["Elements"].update({"paid_type": paid_type})
        if type_id:
            operation["Elements"].update({"type_id": type_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.bind_private_queue_validate(operation)
        return Request(self.config, operation)

    def bind_private_queue(self,
                           timestamp="",
                           cluster_id="",
                           duration=None,
                           is_auto_renewal=None,
                           name="",
                           paid_type="",
                           type_id="",
                           zone=""):
        req = self.bind_private_queue_request(timestamp=timestamp,
                                              cluster_id=cluster_id,
                                              duration=duration,
                                              is_auto_renewal=is_auto_renewal,
                                              name=name,
                                              paid_type=paid_type,
                                              type_id=type_id,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def bind_private_queue_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "bind_private_queueInput")

        if "is_auto_renewal" in op["Elements"] and op["Elements"][
                "is_auto_renewal"]:

            is_auto_renewal_valid_values = ["0", "1"]
            if op["Elements"][
                    "is_auto_renewal"] not in is_auto_renewal_valid_values:
                return ParameterValueNotAllowedError(
                    "is_auto_renewal", op["Elements"]["is_auto_renewal"],
                    is_auto_renewal_valid_values)

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "bind_private_queueInput")

        if op["Elements"]["paid_type"] is None:
            return ParameterRequiredError("paid_type",
                                          "bind_private_queueInput")

        if "paid_type" in op["Elements"] and op["Elements"]["paid_type"]:

            paid_type_valid_values = ["Reserved", "PayForUsed"]
            if op["Elements"]["paid_type"] not in paid_type_valid_values:
                return ParameterValueNotAllowedError(
                    "paid_type", op["Elements"]["paid_type"],
                    paid_type_valid_values)

        if op["Elements"]["type_id"] is None:
            return ParameterRequiredError("type_id", "bind_private_queueInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "bind_private_queueInput")

        return None

    def del_ehpc_queues_request(self,
                                timestamp="",
                                cluster_id="",
                                queue_ids=list(),
                                zone=""):
        operation = {
            "API": "del_ehpc_queues",
            "Method": "POST",
            "URI": "/api/queue/ehpc/delQueues",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if queue_ids:
            operation["Elements"].update({"queue_ids": queue_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_ehpc_queues_validate(operation)
        return Request(self.config, operation)

    def del_ehpc_queues(self,
                        timestamp="",
                        cluster_id="",
                        queue_ids=list(),
                        zone=""):
        req = self.del_ehpc_queues_request(timestamp=timestamp,
                                           cluster_id=cluster_id,
                                           queue_ids=queue_ids,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_ehpc_queues_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_ehpc_queuesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "del_ehpc_queuesInput")

        if op["Elements"]["queue_ids"] is None:
            return ParameterRequiredError("queue_ids", "del_ehpc_queuesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_ehpc_queuesInput")

        return None

    def del_phy_queues_request(self, timestamp="", hpq_ids=list(), zone=""):
        operation = {
            "API": "del_phy_queues",
            "Method": "POST",
            "URI": "/api/queue/hpc/delPhyQueues",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if hpq_ids:
            operation["Elements"].update({"hpq_ids": hpq_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_phy_queues_validate(operation)
        return Request(self.config, operation)

    def del_phy_queues(self, timestamp="", hpq_ids=list(), zone=""):
        req = self.del_phy_queues_request(timestamp=timestamp,
                                          hpq_ids=hpq_ids,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_phy_queues_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_phy_queuesInput")

        if op["Elements"]["hpq_ids"] is None:
            return ParameterRequiredError("hpq_ids", "del_phy_queuesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_phy_queuesInput")

        return None

    def del_queue_types_request(self, timestamp="", type_ids=list(), zone=""):
        operation = {
            "API": "del_queue_types",
            "Method": "POST",
            "URI": "/api/queue/queuetype/delQueueTypes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if type_ids:
            operation["Elements"].update({"type_ids": type_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_queue_types_validate(operation)
        return Request(self.config, operation)

    def del_queue_types(self, timestamp="", type_ids=list(), zone=""):
        req = self.del_queue_types_request(timestamp=timestamp,
                                           type_ids=type_ids,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_queue_types_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "del_queue_typesInput")

        if op["Elements"]["type_ids"] is None:
            return ParameterRequiredError("type_ids", "del_queue_typesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "del_queue_typesInput")

        return None

    def describe_queue_request(self,
                               cluster_id="",
                               id="",
                               owner="",
                               timestamp="",
                               zone=""):
        operation = {
            "API": "describe_queue",
            "Method": "GET",
            "URI": "/api/queue/describeQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if id:
            operation["Params"].update({"id": id})

        if owner:
            operation["Params"].update({"owner": owner})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.describe_queue_validate(operation)
        return Request(self.config, operation)

    def describe_queue(self,
                       cluster_id="",
                       id="",
                       owner="",
                       timestamp="",
                       zone=""):
        req = self.describe_queue_request(cluster_id=cluster_id,
                                          id=id,
                                          owner=owner,
                                          timestamp=timestamp,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def describe_queue_validate(op):

        if op["Params"]["id"] is None:
            return ParameterRequiredError("id", "describe_queueInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "describe_queueInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "describe_queueInput")

        return None

    def get_current_queue_request(self,
                                  belong=None,
                                  cluster_id="",
                                  limit=None,
                                  offset=None,
                                  owner="",
                                  reverse=None,
                                  search_word="",
                                  sort_key="",
                                  timestamp="",
                                  zone=""):
        operation = {
            "API": "get_current_queue",
            "Method": "GET",
            "URI": "/api/queue/getCurrentQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if belong:
            operation["Params"].update({"belong": belong})

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_current_queue_validate(operation)
        return Request(self.config, operation)

    def get_current_queue(self,
                          belong=None,
                          cluster_id="",
                          limit=None,
                          offset=None,
                          owner="",
                          reverse=None,
                          search_word="",
                          sort_key="",
                          timestamp="",
                          zone=""):
        req = self.get_current_queue_request(belong=belong,
                                             cluster_id=cluster_id,
                                             limit=limit,
                                             offset=offset,
                                             owner=owner,
                                             reverse=reverse,
                                             search_word=search_word,
                                             sort_key=sort_key,
                                             timestamp=timestamp,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_current_queue_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_current_queueInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_current_queueInput")

        return None

    def get_ehpc_queue_list_request(self,
                                    cluster_id="",
                                    is_active=None,
                                    limit=None,
                                    name="",
                                    offset=None,
                                    queue_ids=list(),
                                    reverse=None,
                                    search_word="",
                                    sort_key="",
                                    timestamp="",
                                    zone=""):
        operation = {
            "API": "get_ehpc_queue_list",
            "Method": "GET",
            "URI": "/api/queue/ehpc/getQueueList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if is_active:
            operation["Params"].update({"is_active": is_active})

        if limit:
            operation["Params"].update({"limit": limit})

        if name:
            operation["Params"].update({"name": name})

        if offset:
            operation["Params"].update({"offset": offset})

        if queue_ids != list() and queue_ids:
            operation["Params"].update({"queue_ids": queue_ids})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_ehpc_queue_list_validate(operation)
        return Request(self.config, operation)

    def get_ehpc_queue_list(self,
                            cluster_id="",
                            is_active=None,
                            limit=None,
                            name="",
                            offset=None,
                            queue_ids=list(),
                            reverse=None,
                            search_word="",
                            sort_key="",
                            timestamp="",
                            zone=""):
        req = self.get_ehpc_queue_list_request(cluster_id=cluster_id,
                                               is_active=is_active,
                                               limit=limit,
                                               name=name,
                                               offset=offset,
                                               queue_ids=queue_ids,
                                               reverse=reverse,
                                               search_word=search_word,
                                               sort_key=sort_key,
                                               timestamp=timestamp,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_ehpc_queue_list_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_ehpc_queue_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_ehpc_queue_listInput")

        return None

    def get_phy_queues_request(self,
                               hpq_ids=list(),
                               hpq_name="",
                               limit=None,
                               offset=None,
                               reverse=None,
                               search_word="",
                               sort_key="",
                               timestamp="",
                               zone=""):
        operation = {
            "API": "get_phy_queues",
            "Method": "GET",
            "URI": "/api/queue/hpc/getPhyQueues",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }
        if hpq_ids != list() and hpq_ids:
            operation["Params"].update({"hpq_ids": hpq_ids})

        if hpq_name:
            operation["Params"].update({"hpq_name": hpq_name})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_phy_queues_validate(operation)
        return Request(self.config, operation)

    def get_phy_queues(self,
                       hpq_ids=list(),
                       hpq_name="",
                       limit=None,
                       offset=None,
                       reverse=None,
                       search_word="",
                       sort_key="",
                       timestamp="",
                       zone=""):
        req = self.get_phy_queues_request(hpq_ids=hpq_ids,
                                          hpq_name=hpq_name,
                                          limit=limit,
                                          offset=offset,
                                          reverse=reverse,
                                          search_word=search_word,
                                          sort_key=sort_key,
                                          timestamp=timestamp,
                                          zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_phy_queues_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_phy_queuesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_phy_queuesInput")

        return None

    def get_queue_nodes_request(self,
                                hpcqueue_id="",
                                limit=None,
                                offset=None,
                                search_word="",
                                timestamp="",
                                zone=""):
        operation = {
            "API": "get_queue_nodes",
            "Method": "GET",
            "URI": "/api/queue/getQueueNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if hpcqueue_id:
            operation["Params"].update({"hpcqueue_id": hpcqueue_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_queue_nodes_validate(operation)
        return Request(self.config, operation)

    def get_queue_nodes(self,
                        hpcqueue_id="",
                        limit=None,
                        offset=None,
                        search_word="",
                        timestamp="",
                        zone=""):
        req = self.get_queue_nodes_request(hpcqueue_id=hpcqueue_id,
                                           limit=limit,
                                           offset=offset,
                                           search_word=search_word,
                                           timestamp=timestamp,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_queue_nodes_validate(op):
        if op["Params"]["hpcqueue_id"] is None:
            return ParameterRequiredError("hpcqueue_id",
                                          "get_queue_nodesInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_queue_nodesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_queue_nodesInput")

        return None

    def get_queue_type_list_request(self,
                                    limit=None,
                                    name="",
                                    offset=None,
                                    reverse=None,
                                    search_word="",
                                    sort_key="",
                                    timestamp="",
                                    type_ids=list(),
                                    zone=""):
        operation = {
            "API": "get_queue_type_list",
            "Method": "GET",
            "URI": "/api/queue/queuetype/queueTypeList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if name:
            operation["Params"].update({"name": name})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if type_ids != list() and type_ids:
            operation["Params"].update({"type_ids": type_ids})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_queue_type_list_validate(operation)
        return Request(self.config, operation)

    def get_queue_type_list(self,
                            limit=None,
                            name="",
                            offset=None,
                            reverse=None,
                            search_word="",
                            sort_key="",
                            timestamp="",
                            type_ids=list(),
                            zone=""):
        req = self.get_queue_type_list_request(limit=limit,
                                               name=name,
                                               offset=offset,
                                               reverse=reverse,
                                               search_word=search_word,
                                               sort_key=sort_key,
                                               timestamp=timestamp,
                                               type_ids=type_ids,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_queue_type_list_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_queue_type_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_queue_type_listInput")

        return None

    def get_queue_types_request(self,
                                limit=None,
                                offset=None,
                                timestamp="",
                                zone=""):
        operation = {
            "API": "get_queue_types",
            "Method": "GET",
            "URI": "/api/queue/getQueueTypes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_queue_types_validate(operation)
        return Request(self.config, operation)

    def get_queue_types(self, limit=None, offset=None, timestamp="", zone=""):
        req = self.get_queue_types_request(limit=limit,
                                           offset=offset,
                                           timestamp=timestamp,
                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_queue_types_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_queue_typesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_queue_typesInput")

        return None

    def is_available_queue_request(self,
                                   scheduler_queue_name="",
                                   timestamp="",
                                   user_id="",
                                   zone=""):
        operation = {
            "API": "is_available_queue",
            "Method": "GET",
            "URI": "/api/queue/isAvailableQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if scheduler_queue_name:
            operation["Params"].update(
                {"scheduler_queue_name": scheduler_queue_name})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.is_available_queue_validate(operation)
        return Request(self.config, operation)

    def is_available_queue(self,
                           scheduler_queue_name="",
                           timestamp="",
                           user_id="",
                           zone=""):
        req = self.is_available_queue_request(
            scheduler_queue_name=scheduler_queue_name,
            timestamp=timestamp,
            user_id=user_id,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def is_available_queue_validate(op):
        if op["Params"]["scheduler_queue_name"] is None:
            return ParameterRequiredError("scheduler_queue_name",
                                          "is_available_queueInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "is_available_queueInput")

        if op["Params"]["user_id"] is None:
            return ParameterRequiredError("user_id", "is_available_queueInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "is_available_queueInput")

        return None

    def modify_ehpc_queue_request(self,
                                  timestamp="",
                                  allow_accounts="",
                                  cluster_id="",
                                  default_queue=None,
                                  deny_accounts="",
                                  hpcqueue_id="",
                                  max_time="",
                                  min_node=None,
                                  name="",
                                  status=None,
                                  user_group="",
                                  zone=""):
        operation = {
            "API": "modify_ehpc_queue",
            "Method": "POST",
            "URI": "/api/queue/ehpc/modifyQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if allow_accounts:
            operation["Elements"].update({"allow_accounts": allow_accounts})
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if default_queue:
            operation["Elements"].update({"default_queue": default_queue})
        if deny_accounts:
            operation["Elements"].update({"deny_accounts": deny_accounts})
        if hpcqueue_id:
            operation["Elements"].update({"hpcqueue_id": hpcqueue_id})
        if max_time:
            operation["Elements"].update({"max_time": max_time})
        if min_node:
            operation["Elements"].update({"min_node": min_node})
        if name:
            operation["Elements"].update({"name": name})
        if status:
            operation["Elements"].update({"status": status})
        if user_group:
            operation["Elements"].update({"user_group": user_group})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_ehpc_queue_validate(operation)
        return Request(self.config, operation)

    def modify_ehpc_queue(self,
                          timestamp="",
                          allow_accounts="",
                          cluster_id="",
                          default_queue=None,
                          deny_accounts="",
                          hpcqueue_id="",
                          max_time="",
                          min_node=None,
                          name="",
                          status=None,
                          user_group="",
                          zone=""):
        req = self.modify_ehpc_queue_request(timestamp=timestamp,
                                             allow_accounts=allow_accounts,
                                             cluster_id=cluster_id,
                                             default_queue=default_queue,
                                             deny_accounts=deny_accounts,
                                             hpcqueue_id=hpcqueue_id,
                                             max_time=max_time,
                                             min_node=min_node,
                                             name=name,
                                             status=status,
                                             user_group=user_group,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_ehpc_queue_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_ehpc_queueInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "modify_ehpc_queueInput")

        if "default_queue" in op["Elements"] and op["Elements"][
                "default_queue"]:

            default_queue_valid_values = ["0", "1"]
            if op["Elements"][
                    "default_queue"] not in default_queue_valid_values:
                return ParameterValueNotAllowedError(
                    "default_queue", op["Elements"]["default_queue"],
                    default_queue_valid_values)

        if op["Elements"]["hpcqueue_id"] is None:
            return ParameterRequiredError("hpcqueue_id",
                                          "modify_ehpc_queueInput")

        if "status" in op["Elements"] and op["Elements"]["status"]:

            status_valid_values = ["0", "1"]
            if op["Elements"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Elements"]["status"],
                                                     status_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_ehpc_queueInput")

        return None

    def remove_ehpc_queue_nodes_request(self,
                                        timestamp="",
                                        cluster_id="",
                                        hpcqueue_id="",
                                        nodelist=list(),
                                        zone=""):
        operation = {
            "API": "remove_ehpc_queue_nodes",
            "Method": "POST",
            "URI": "/api/queue/ehpc/removeNodes",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if hpcqueue_id:
            operation["Elements"].update({"hpcqueue_id": hpcqueue_id})
        if nodelist:
            operation["Elements"].update({"nodelist": nodelist})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.remove_ehpc_queue_nodes_validate(operation)
        return Request(self.config, operation)

    def remove_ehpc_queue_nodes(self,
                                timestamp="",
                                cluster_id="",
                                hpcqueue_id="",
                                nodelist=list(),
                                zone=""):
        req = self.remove_ehpc_queue_nodes_request(timestamp=timestamp,
                                                   cluster_id=cluster_id,
                                                   hpcqueue_id=hpcqueue_id,
                                                   nodelist=nodelist,
                                                   zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def remove_ehpc_queue_nodes_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "remove_ehpc_queue_nodesInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "remove_ehpc_queue_nodesInput")

        if op["Elements"]["hpcqueue_id"] is None:
            return ParameterRequiredError("hpcqueue_id",
                                          "remove_ehpc_queue_nodesInput")

        if op["Elements"]["nodelist"] is None:
            return ParameterRequiredError("nodelist",
                                          "remove_ehpc_queue_nodesInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "remove_ehpc_queue_nodesInput")

        return None

    def unbind_private_queue_request(self, timestamp="", ids=list(), zone=""):
        operation = {
            "API": "unbind_private_queue",
            "Method": "POST",
            "URI": "/api/queue/unbindPrivateQueue",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if ids:
            operation["Elements"].update({"ids": ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.unbind_private_queue_validate(operation)
        return Request(self.config, operation)

    def unbind_private_queue(self, timestamp="", ids=list(), zone=""):
        req = self.unbind_private_queue_request(timestamp=timestamp,
                                                ids=ids,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def unbind_private_queue_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "unbind_private_queueInput")

        if op["Elements"]["ids"] is None:
            return ParameterRequiredError("ids", "unbind_private_queueInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "unbind_private_queueInput")

        return None

    def update_queue_name_request(self, timestamp="", id="", name="", zone=""):
        operation = {
            "API": "update_queue_name",
            "Method": "POST",
            "URI": "/api/queue/updateQueueName",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if id:
            operation["Elements"].update({"id": id})
        if name:
            operation["Elements"].update({"name": name})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.update_queue_name_validate(operation)
        return Request(self.config, operation)

    def update_queue_name(self, timestamp="", id="", name="", zone=""):
        req = self.update_queue_name_request(timestamp=timestamp,
                                             id=id,
                                             name=name,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def update_queue_name_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "update_queue_nameInput")

        if op["Elements"]["id"] is None:
            return ParameterRequiredError("id", "update_queue_nameInput")

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "update_queue_nameInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "update_queue_nameInput")

        return None

    def get_cluster_bill_info_request(self,
                                      cluster_id="",
                                      limit=None,
                                      offset=None,
                                      owner="",
                                      reverse=None,
                                      search_word="",
                                      sort_key="",
                                      timestamp="",
                                      zone=""):
        operation = {
            "API": "get_cluster_bill_info",
            "Method": "GET",
            "URI": "/api/rent/cluster/billInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_bill_info_validate(operation)
        return Request(self.config, operation)

    def get_cluster_bill_info(self,
                              cluster_id="",
                              limit=None,
                              offset=None,
                              owner="",
                              reverse=None,
                              search_word="",
                              sort_key="",
                              timestamp="",
                              zone=""):
        req = self.get_cluster_bill_info_request(cluster_id=cluster_id,
                                                 limit=limit,
                                                 offset=offset,
                                                 owner=owner,
                                                 reverse=reverse,
                                                 search_word=search_word,
                                                 sort_key=sort_key,
                                                 timestamp=timestamp,
                                                 zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_bill_info_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_cluster_bill_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_cluster_bill_infoInput")

        return None

    def get_cluster_private_resource_info_request(self,
                                                  cluster_id="",
                                                  limit=None,
                                                  offset=None,
                                                  paid_type="",
                                                  reverse=None,
                                                  search_word="",
                                                  sort_key="",
                                                  timestamp="",
                                                  zone=""):
        operation = {
            "API": "get_cluster_private_resource_info",
            "Method": "GET",
            "URI": "/api/rent/cluster/privateResourceInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if paid_type:
            operation["Params"].update({"paid_type": paid_type})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_private_resource_info_validate(operation)
        return Request(self.config, operation)

    def get_cluster_private_resource_info(self,
                                          cluster_id="",
                                          limit=None,
                                          offset=None,
                                          paid_type="",
                                          reverse=None,
                                          search_word="",
                                          sort_key="",
                                          timestamp="",
                                          zone=""):
        req = self.get_cluster_private_resource_info_request(
            cluster_id=cluster_id,
            limit=limit,
            offset=offset,
            paid_type=paid_type,
            reverse=reverse,
            search_word=search_word,
            sort_key=sort_key,
            timestamp=timestamp,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_private_resource_info_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError(
                "cluster_id", "get_cluster_private_resource_infoInput")

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError(
                "timestamp", "get_cluster_private_resource_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError(
                "zone", "get_cluster_private_resource_infoInput")

        return None

    def get_cluster_share_resource_info_request(self,
                                                cluster_id="",
                                                limit=None,
                                                offset=None,
                                                reverse=None,
                                                search_word="",
                                                sort_key="",
                                                timestamp="",
                                                zone=""):
        operation = {
            "API": "get_cluster_share_resource_info",
            "Method": "GET",
            "URI": "/api/rent/cluster/shareResourceInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_share_resource_info_validate(operation)
        return Request(self.config, operation)

    def get_cluster_share_resource_info(self,
                                        cluster_id="",
                                        limit=None,
                                        offset=None,
                                        reverse=None,
                                        search_word="",
                                        sort_key="",
                                        timestamp="",
                                        zone=""):
        req = self.get_cluster_share_resource_info_request(
            cluster_id=cluster_id,
            limit=limit,
            offset=offset,
            reverse=reverse,
            search_word=search_word,
            sort_key=sort_key,
            timestamp=timestamp,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_share_resource_info_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError(
                "cluster_id", "get_cluster_share_resource_infoInput")

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError(
                "timestamp", "get_cluster_share_resource_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError(
                "zone", "get_cluster_share_resource_infoInput")

        return None

    def get_hpc_free_info_request(self,
                                  end_time="",
                                  limit=None,
                                  offset=None,
                                  resource_type="",
                                  start_time="",
                                  timestamp="",
                                  user_id="",
                                  zone=""):
        operation = {
            "API": "get_hpc_free_info",
            "Method": "GET",
            "URI": "/api/rent/hpc/freeInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if resource_type:
            operation["Params"].update({"resource_type": resource_type})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_hpc_free_info_validate(operation)
        return Request(self.config, operation)

    def get_hpc_free_info(self,
                          end_time="",
                          limit=None,
                          offset=None,
                          resource_type="",
                          start_time="",
                          timestamp="",
                          user_id="",
                          zone=""):
        req = self.get_hpc_free_info_request(end_time=end_time,
                                             limit=limit,
                                             offset=offset,
                                             resource_type=resource_type,
                                             start_time=start_time,
                                             timestamp=timestamp,
                                             user_id=user_id,
                                             zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_hpc_free_info_validate(op):

        if op["Params"]["resource_type"] is None:
            return ParameterRequiredError("resource_type",
                                          "get_hpc_free_infoInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_hpc_free_infoInput")

        if op["Params"]["user_id"] is None:
            return ParameterRequiredError("user_id", "get_hpc_free_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_hpc_free_infoInput")

        return None

    def get_remoteapp_bill_info_request(self,
                                        limit=None,
                                        offset=None,
                                        reverse=None,
                                        search_word="",
                                        sort_key="",
                                        timestamp="",
                                        user_id="",
                                        zone=""):
        operation = {
            "API": "get_remoteapp_bill_info",
            "Method": "GET",
            "URI": "/api/rent/remoteapp/billInfo",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_remoteapp_bill_info_validate(operation)
        return Request(self.config, operation)

    def get_remoteapp_bill_info(self,
                                limit=None,
                                offset=None,
                                reverse=None,
                                search_word="",
                                sort_key="",
                                timestamp="",
                                user_id="",
                                zone=""):
        req = self.get_remoteapp_bill_info_request(limit=limit,
                                                   offset=offset,
                                                   reverse=reverse,
                                                   search_word=search_word,
                                                   sort_key=sort_key,
                                                   timestamp=timestamp,
                                                   user_id=user_id,
                                                   zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_remoteapp_bill_info_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_remoteapp_bill_infoInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_remoteapp_bill_infoInput")

        return None

    def add_software_request(self,
                             limit=None,
                             offset=None,
                             search_word="",
                             timestamp="",
                             zone="",
                             class_id="",
                             deploy_mode=None,
                             description="",
                             icon="",
                             ini_cmd="",
                             new_class=None,
                             new_class_name="",
                             software_mess="",
                             sw_name="",
                             sw_type=None,
                             sw_ver=""):
        operation = {
            "API": "add_software",
            "Method": "POST",
            "URI": "/api/software/addSoftware",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if class_id:
            operation["Elements"].update({"class_id": class_id})
        if deploy_mode:
            operation["Elements"].update({"deploy_mode": deploy_mode})
        if description:
            operation["Elements"].update({"description": description})
        if icon:
            operation["Elements"].update({"icon": icon})
        if ini_cmd:
            operation["Elements"].update({"ini_cmd": ini_cmd})
        if new_class:
            operation["Elements"].update({"new_class": new_class})
        if new_class_name:
            operation["Elements"].update({"new_class_name": new_class_name})
        if software_mess:
            operation["Elements"].update({"software_mess": software_mess})
        if sw_name:
            operation["Elements"].update({"sw_name": sw_name})
        if sw_type:
            operation["Elements"].update({"sw_type": sw_type})
        if sw_ver:
            operation["Elements"].update({"sw_ver": sw_ver})
        self.add_software_validate(operation)
        return Request(self.config, operation)

    def add_software(self,
                     limit=None,
                     offset=None,
                     search_word="",
                     timestamp="",
                     zone="",
                     class_id="",
                     deploy_mode=None,
                     description="",
                     icon="",
                     ini_cmd="",
                     new_class=None,
                     new_class_name="",
                     software_mess="",
                     sw_name="",
                     sw_type=None,
                     sw_ver=""):
        req = self.add_software_request(limit=limit,
                                        offset=offset,
                                        search_word=search_word,
                                        timestamp=timestamp,
                                        zone=zone,
                                        class_id=class_id,
                                        deploy_mode=deploy_mode,
                                        description=description,
                                        icon=icon,
                                        ini_cmd=ini_cmd,
                                        new_class=new_class,
                                        new_class_name=new_class_name,
                                        software_mess=software_mess,
                                        sw_name=sw_name,
                                        sw_type=sw_type,
                                        sw_ver=sw_ver)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_software_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "add_softwareInput")

        if op["Elements"]["icon"] is None:
            return ParameterRequiredError("icon", "add_softwareInput")

        if op["Elements"]["ini_cmd"] is None:
            return ParameterRequiredError("ini_cmd", "add_softwareInput")

        if op["Elements"]["sw_name"] is None:
            return ParameterRequiredError("sw_name", "add_softwareInput")

        if op["Elements"]["sw_type"] is None:
            return ParameterRequiredError("sw_type", "add_softwareInput")

        if op["Elements"]["sw_ver"] is None:
            return ParameterRequiredError("sw_ver", "add_softwareInput")

        return None

    def apply_software_request(self,
                               timestamp="",
                               zone="",
                               email="",
                               phone="",
                               platform=None,
                               reason="",
                               sw_name=""):
        operation = {
            "API": "apply_software",
            "Method": "POST",
            "URI": "/api/software/apply",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if email:
            operation["Elements"].update({"email": email})
        if phone:
            operation["Elements"].update({"phone": phone})
        if platform:
            operation["Elements"].update({"platform": platform})
        if reason:
            operation["Elements"].update({"reason": reason})
        if sw_name:
            operation["Elements"].update({"sw_name": sw_name})
        self.apply_software_validate(operation)
        return Request(self.config, operation)

    def apply_software(self,
                       timestamp="",
                       zone="",
                       email="",
                       phone="",
                       platform=None,
                       reason="",
                       sw_name=""):
        req = self.apply_software_request(timestamp=timestamp,
                                          zone=zone,
                                          email=email,
                                          phone=phone,
                                          platform=platform,
                                          reason=reason,
                                          sw_name=sw_name)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def apply_software_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "apply_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "apply_softwareInput")

        if op["Elements"]["email"] is None:
            return ParameterRequiredError("email", "apply_softwareInput")

        if op["Elements"]["phone"] is None:
            return ParameterRequiredError("phone", "apply_softwareInput")

        if op["Elements"]["reason"] is None:
            return ParameterRequiredError("reason", "apply_softwareInput")

        return None

    def delete_class_request(self,
                             limit=None,
                             offset=None,
                             search_word="",
                             timestamp="",
                             zone="",
                             class_id=""):
        operation = {
            "API": "delete_class",
            "Method": "POST",
            "URI": "/api/software/deleteclass",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if class_id:
            operation["Elements"].update({"class_id": class_id})
        self.delete_class_validate(operation)
        return Request(self.config, operation)

    def delete_class(self,
                     limit=None,
                     offset=None,
                     search_word="",
                     timestamp="",
                     zone="",
                     class_id=""):
        req = self.delete_class_request(limit=limit,
                                        offset=offset,
                                        search_word=search_word,
                                        timestamp=timestamp,
                                        zone=zone,
                                        class_id=class_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_class_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "delete_classInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_classInput")

        if op["Elements"]["class_id"] is None:
            return ParameterRequiredError("class_id", "delete_classInput")

        return None

    def delete_software_request(self,
                                limit=None,
                                offset=None,
                                search_word="",
                                timestamp="",
                                zone="",
                                hpcsw_id=""):
        operation = {
            "API": "delete_software",
            "Method": "POST",
            "URI": "/api/software/delete",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if hpcsw_id:
            operation["Elements"].update({"hpcsw_id": hpcsw_id})
        self.delete_software_validate(operation)
        return Request(self.config, operation)

    def delete_software(self,
                        limit=None,
                        offset=None,
                        search_word="",
                        timestamp="",
                        zone="",
                        hpcsw_id=""):
        req = self.delete_software_request(limit=limit,
                                           offset=offset,
                                           search_word=search_word,
                                           timestamp=timestamp,
                                           zone=zone,
                                           hpcsw_id=hpcsw_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_software_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "delete_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_softwareInput")

        if op["Elements"]["hpcsw_id"] is None:
            return ParameterRequiredError("hpcsw_id", "delete_softwareInput")

        return None

    def get_apply_request(self,
                          apply_type="",
                          is_apply=None,
                          limit=None,
                          offset=None,
                          owner="",
                          platform=None,
                          reverse=None,
                          search_word="",
                          sort_key="",
                          status="",
                          timestamp="",
                          user_id="",
                          zone=""):
        operation = {
            "API": "get_apply",
            "Method": "GET",
            "URI": "/api/software/applylist",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if apply_type:
            operation["Params"].update({"apply_type": apply_type})

        if is_apply:
            operation["Params"].update({"is_apply": is_apply})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if platform:
            operation["Params"].update({"platform": platform})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_apply_validate(operation)
        return Request(self.config, operation)

    def get_apply(self,
                  apply_type="",
                  is_apply=None,
                  limit=None,
                  offset=None,
                  owner="",
                  platform=None,
                  reverse=None,
                  search_word="",
                  sort_key="",
                  status="",
                  timestamp="",
                  user_id="",
                  zone=""):
        req = self.get_apply_request(apply_type=apply_type,
                                     is_apply=is_apply,
                                     limit=limit,
                                     offset=offset,
                                     owner=owner,
                                     platform=platform,
                                     reverse=reverse,
                                     search_word=search_word,
                                     sort_key=sort_key,
                                     status=status,
                                     timestamp=timestamp,
                                     user_id=user_id,
                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_apply_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_applyInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_applyInput")

        return None

    def get_cluster_software_list_request(self,
                                          cluster_id="",
                                          timestamp="",
                                          zone=""):
        operation = {
            "API": "get_cluster_software_list",
            "Method": "GET",
            "URI": "/api/software/cluster/list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_cluster_software_list_validate(operation)
        return Request(self.config, operation)

    def get_cluster_software_list(self, cluster_id="", timestamp="", zone=""):
        req = self.get_cluster_software_list_request(cluster_id=cluster_id,
                                                     timestamp=timestamp,
                                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_cluster_software_list_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "get_cluster_software_listInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_cluster_software_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_cluster_software_listInput")

        return None

    def get_graphics_request(self,
                             apply_type="",
                             is_apply=None,
                             limit=None,
                             offset=None,
                             owner="",
                             reverse=None,
                             sort_key="",
                             timestamp="",
                             user_id="",
                             zone=""):
        operation = {
            "API": "get_graphics",
            "Method": "GET",
            "URI": "/api/software/graphics",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if apply_type:
            operation["Params"].update({"apply_type": apply_type})

        if is_apply:
            operation["Params"].update({"is_apply": is_apply})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_graphics_validate(operation)
        return Request(self.config, operation)

    def get_graphics(self,
                     apply_type="",
                     is_apply=None,
                     limit=None,
                     offset=None,
                     owner="",
                     reverse=None,
                     sort_key="",
                     timestamp="",
                     user_id="",
                     zone=""):
        req = self.get_graphics_request(apply_type=apply_type,
                                        is_apply=is_apply,
                                        limit=limit,
                                        offset=offset,
                                        owner=owner,
                                        reverse=reverse,
                                        sort_key=sort_key,
                                        timestamp=timestamp,
                                        user_id=user_id,
                                        zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_graphics_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_graphicsInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_graphicsInput")

        return None

    def get_list_request(self,
                         class_id="",
                         deploy_mode=None,
                         hpcsw_id="",
                         limit=None,
                         offset=None,
                         owner="",
                         platform=None,
                         reverse=None,
                         search_word="",
                         sort_key="",
                         status=None,
                         sw_type="",
                         timestamp="",
                         user_id="",
                         zone=""):
        operation = {
            "API": "get_list",
            "Method": "GET",
            "URI": "/api/software/list",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if class_id:
            operation["Params"].update({"class_id": class_id})

        if deploy_mode:
            operation["Params"].update({"deploy_mode": deploy_mode})

        if hpcsw_id:
            operation["Params"].update({"hpcsw_id": hpcsw_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if platform:
            operation["Params"].update({"platform": platform})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if status:
            operation["Params"].update({"status": status})

        if sw_type:
            operation["Params"].update({"sw_type": sw_type})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_list_validate(operation)
        return Request(self.config, operation)

    def get_list(self,
                 class_id="",
                 deploy_mode=None,
                 hpcsw_id="",
                 limit=None,
                 offset=None,
                 owner="",
                 platform=None,
                 reverse=None,
                 search_word="",
                 sort_key="",
                 status=None,
                 sw_type="",
                 timestamp="",
                 user_id="",
                 zone=""):
        req = self.get_list_request(class_id=class_id,
                                    deploy_mode=deploy_mode,
                                    hpcsw_id=hpcsw_id,
                                    limit=limit,
                                    offset=offset,
                                    owner=owner,
                                    platform=platform,
                                    reverse=reverse,
                                    search_word=search_word,
                                    sort_key=sort_key,
                                    status=status,
                                    sw_type=sw_type,
                                    timestamp=timestamp,
                                    user_id=user_id,
                                    zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_list_validate(op):

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if "status" in op["Params"] and op["Params"]["status"]:

            status_valid_values = ["0", "1"]
            if op["Params"]["status"] not in status_valid_values:
                return ParameterValueNotAllowedError("status",
                                                     op["Params"]["status"],
                                                     status_valid_values)

        if "sw_type" in op["Params"] and op["Params"]["sw_type"]:

            sw_type_valid_values = ["0", "1"]
            if op["Params"]["sw_type"] not in sw_type_valid_values:
                return ParameterValueNotAllowedError("sw_type",
                                                     op["Params"]["sw_type"],
                                                     sw_type_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "get_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_listInput")

        return None

    def get_remoteapp_link_request(self,
                                   hpcsw_id="",
                                   nas_mount_point="",
                                   timestamp="",
                                   zone=""):
        operation = {
            "API": "get_remoteapp_link",
            "Method": "GET",
            "URI": "/api/software/remoteapp/link",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if hpcsw_id:
            operation["Params"].update({"hpcsw_id": hpcsw_id})

        if nas_mount_point:
            operation["Params"].update({"nas_mount_point": nas_mount_point})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_remoteapp_link_validate(operation)
        return Request(self.config, operation)

    def get_remoteapp_link(self,
                           hpcsw_id="",
                           nas_mount_point="",
                           timestamp="",
                           zone=""):
        req = self.get_remoteapp_link_request(hpcsw_id=hpcsw_id,
                                              nas_mount_point=nas_mount_point,
                                              timestamp=timestamp,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_remoteapp_link_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_remoteapp_linkInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_remoteapp_linkInput")

        return None

    def install_cluster_softwares_request(self,
                                          timestamp="",
                                          cluster_id="",
                                          sw_ids=list(),
                                          zone=""):
        operation = {
            "API": "install_cluster_softwares",
            "Method": "POST",
            "URI": "/api/software/cluster/install",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if sw_ids:
            operation["Elements"].update({"sw_ids": sw_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.install_cluster_softwares_validate(operation)
        return Request(self.config, operation)

    def install_cluster_softwares(self,
                                  timestamp="",
                                  cluster_id="",
                                  sw_ids=list(),
                                  zone=""):
        req = self.install_cluster_softwares_request(timestamp=timestamp,
                                                     cluster_id=cluster_id,
                                                     sw_ids=sw_ids,
                                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def install_cluster_softwares_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "install_cluster_softwaresInput")

        return None

    def list_class_request(self, class_id="", timestamp="", zone=""):
        operation = {
            "API": "list_class",
            "Method": "GET",
            "URI": "/api/software/class",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if class_id:
            operation["Params"].update({"class_id": class_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_class_validate(operation)
        return Request(self.config, operation)

    def list_class(self, class_id="", timestamp="", zone=""):
        req = self.list_class_request(class_id=class_id,
                                      timestamp=timestamp,
                                      zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_class_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_classInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_classInput")

        return None

    def mark_request(self,
                     timestamp="",
                     zone="",
                     mark=None,
                     sw_name="",
                     user_id=""):
        operation = {
            "API": "mark",
            "Method": "POST",
            "URI": "/api/software/mark",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if mark:
            operation["Elements"].update({"mark": mark})
        if sw_name:
            operation["Elements"].update({"sw_name": sw_name})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        self.mark_validate(operation)
        return Request(self.config, operation)

    def mark(self, timestamp="", zone="", mark=None, sw_name="", user_id=""):
        req = self.mark_request(timestamp=timestamp,
                                zone=zone,
                                mark=mark,
                                sw_name=sw_name,
                                user_id=user_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def mark_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "markInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "markInput")

        if op["Elements"]["mark"] is None:
            return ParameterRequiredError("mark", "markInput")

        if "mark" in op["Elements"] and op["Elements"]["mark"]:

            mark_valid_values = ["0", "1"]
            if op["Elements"]["mark"] not in mark_valid_values:
                return ParameterValueNotAllowedError("mark",
                                                     op["Elements"]["mark"],
                                                     mark_valid_values)

        if op["Elements"]["sw_name"] is None:
            return ParameterRequiredError("sw_name", "markInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id", "markInput")

        return None

    def modify_software_request(self,
                                limit=None,
                                offset=None,
                                search_word="",
                                timestamp="",
                                zone="",
                                class_id="",
                                hpcsw_id="",
                                ini_cmd="",
                                sw_name=""):
        operation = {
            "API": "modify_software",
            "Method": "POST",
            "URI": "/api/software/modify",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if class_id:
            operation["Elements"].update({"class_id": class_id})
        if hpcsw_id:
            operation["Elements"].update({"hpcsw_id": hpcsw_id})
        if ini_cmd:
            operation["Elements"].update({"ini_cmd": ini_cmd})
        if sw_name:
            operation["Elements"].update({"sw_name": sw_name})
        self.modify_software_validate(operation)
        return Request(self.config, operation)

    def modify_software(self,
                        limit=None,
                        offset=None,
                        search_word="",
                        timestamp="",
                        zone="",
                        class_id="",
                        hpcsw_id="",
                        ini_cmd="",
                        sw_name=""):
        req = self.modify_software_request(limit=limit,
                                           offset=offset,
                                           search_word=search_word,
                                           timestamp=timestamp,
                                           zone=zone,
                                           class_id=class_id,
                                           hpcsw_id=hpcsw_id,
                                           ini_cmd=ini_cmd,
                                           sw_name=sw_name)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_software_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_softwareInput")

        if op["Elements"]["hpcsw_id"] is None:
            return ParameterRequiredError("hpcsw_id", "modify_softwareInput")

        return None

    def start_software_request(self,
                               timestamp="",
                               zone="",
                               hpcsw_id="",
                               user_visible=None):
        operation = {
            "API": "start_software",
            "Method": "POST",
            "URI": "/api/software/start",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if hpcsw_id:
            operation["Elements"].update({"hpcsw_id": hpcsw_id})
        if user_visible:
            operation["Elements"].update({"user_visible": user_visible})
        self.start_software_validate(operation)
        return Request(self.config, operation)

    def start_software(self,
                       timestamp="",
                       zone="",
                       hpcsw_id="",
                       user_visible=None):
        req = self.start_software_request(timestamp=timestamp,
                                          zone=zone,
                                          hpcsw_id=hpcsw_id,
                                          user_visible=user_visible)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def start_software_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "start_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "start_softwareInput")

        if op["Elements"]["hpcsw_id"] is None:
            return ParameterRequiredError("hpcsw_id", "start_softwareInput")

        if op["Elements"]["user_visible"] is None:
            return ParameterRequiredError("user_visible",
                                          "start_softwareInput")

        return None

    def stop_software_request(self,
                              timestamp="",
                              zone="",
                              hpcsw_id="",
                              user_visible=None):
        operation = {
            "API": "stop_software",
            "Method": "POST",
            "URI": "/api/software/stop",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if hpcsw_id:
            operation["Elements"].update({"hpcsw_id": hpcsw_id})
        if user_visible:
            operation["Elements"].update({"user_visible": user_visible})
        self.stop_software_validate(operation)
        return Request(self.config, operation)

    def stop_software(self,
                      timestamp="",
                      zone="",
                      hpcsw_id="",
                      user_visible=None):
        req = self.stop_software_request(timestamp=timestamp,
                                         zone=zone,
                                         hpcsw_id=hpcsw_id,
                                         user_visible=user_visible)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def stop_software_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "stop_softwareInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "stop_softwareInput")

        if op["Elements"]["hpcsw_id"] is None:
            return ParameterRequiredError("hpcsw_id", "stop_softwareInput")

        if op["Elements"]["user_visible"] is None:
            return ParameterRequiredError("user_visible", "stop_softwareInput")

        return None

    def uninstall_cluster_softwares_request(self,
                                            timestamp="",
                                            cluster_id="",
                                            sw_ids=list(),
                                            zone=""):
        operation = {
            "API": "uninstall_cluster_softwares",
            "Method": "POST",
            "URI": "/api/software/cluster/uninstall",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if sw_ids:
            operation["Elements"].update({"sw_ids": sw_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.uninstall_cluster_softwares_validate(operation)
        return Request(self.config, operation)

    def uninstall_cluster_softwares(self,
                                    timestamp="",
                                    cluster_id="",
                                    sw_ids=list(),
                                    zone=""):
        req = self.uninstall_cluster_softwares_request(timestamp=timestamp,
                                                       cluster_id=cluster_id,
                                                       sw_ids=sw_ids,
                                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def uninstall_cluster_softwares_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "uninstall_cluster_softwaresInput")

        return None

    def update_apply_request(self,
                             timestamp="",
                             zone="",
                             is_apply=None,
                             notify_email="",
                             reason="",
                             reason_id="",
                             sw_name=""):
        operation = {
            "API": "update_apply",
            "Method": "POST",
            "URI": "/api/software/applyupdate",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if is_apply:
            operation["Elements"].update({"is_apply": is_apply})
        if notify_email:
            operation["Elements"].update({"notify_email": notify_email})
        if reason:
            operation["Elements"].update({"reason": reason})
        if reason_id:
            operation["Elements"].update({"reason_id": reason_id})
        if sw_name:
            operation["Elements"].update({"sw_name": sw_name})
        self.update_apply_validate(operation)
        return Request(self.config, operation)

    def update_apply(self,
                     timestamp="",
                     zone="",
                     is_apply=None,
                     notify_email="",
                     reason="",
                     reason_id="",
                     sw_name=""):
        req = self.update_apply_request(timestamp=timestamp,
                                        zone=zone,
                                        is_apply=is_apply,
                                        notify_email=notify_email,
                                        reason=reason,
                                        reason_id=reason_id,
                                        sw_name=sw_name)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def update_apply_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "update_applyInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "update_applyInput")

        if op["Elements"]["is_apply"] is None:
            return ParameterRequiredError("is_apply", "update_applyInput")

        if op["Elements"]["reason"] is None:
            return ParameterRequiredError("reason", "update_applyInput")

        if op["Elements"]["reason_id"] is None:
            return ParameterRequiredError("reason_id", "update_applyInput")

        if op["Elements"]["sw_name"] is None:
            return ParameterRequiredError("sw_name", "update_applyInput")

        return None

    def list_subusers_request(self,
                              hpc_status="",
                              limit=None,
                              offset=None,
                              reverse=None,
                              search_word="",
                              timestamp="",
                              zone=""):
        operation = {
            "API": "list_subusers",
            "Method": "GET",
            "URI": "/api/subuser",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if hpc_status:
            operation["Params"].update({"hpc_status": hpc_status})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_subusers_validate(operation)
        return Request(self.config, operation)

    def list_subusers(self,
                      hpc_status="",
                      limit=None,
                      offset=None,
                      reverse=None,
                      search_word="",
                      timestamp="",
                      zone=""):
        req = self.list_subusers_request(hpc_status=hpc_status,
                                         limit=limit,
                                         offset=offset,
                                         reverse=reverse,
                                         search_word=search_word,
                                         timestamp=timestamp,
                                         zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_subusers_validate(op):

        if "hpc_status" in op["Params"] and op["Params"]["hpc_status"]:

            hpc_status_valid_values = ["enable", "disable"]
            if op["Params"]["hpc_status"] not in hpc_status_valid_values:
                return ParameterValueNotAllowedError(
                    "hpc_status", op["Params"]["hpc_status"],
                    hpc_status_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_subusersInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_subusersInput")

        return None

    def add_user_request(self,
                         timestamp="",
                         cluster_id="",
                         password="",
                         username="",
                         zone=""):
        operation = {
            "API": "add_user",
            "Method": "POST",
            "URI": "/api/user/addUser",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if password:
            operation["Elements"].update({"password": password})
        if username:
            operation["Elements"].update({"username": username})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.add_user_validate(operation)
        return Request(self.config, operation)

    def add_user(self,
                 timestamp="",
                 cluster_id="",
                 password="",
                 username="",
                 zone=""):
        req = self.add_user_request(timestamp=timestamp,
                                    cluster_id=cluster_id,
                                    password=password,
                                    username=username,
                                    zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_user_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "add_userInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "add_userInput")

        if op["Elements"]["password"] is None:
            return ParameterRequiredError("password", "add_userInput")

        if op["Elements"]["username"] is None:
            return ParameterRequiredError("username", "add_userInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "add_userInput")

        return None

    def delete_user_request(self,
                            timestamp="",
                            cluster_id="",
                            username="",
                            zone=""):
        operation = {
            "API": "delete_user",
            "Method": "POST",
            "URI": "/api/user/deleteUser",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if username:
            operation["Elements"].update({"username": username})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.delete_user_validate(operation)
        return Request(self.config, operation)

    def delete_user(self, timestamp="", cluster_id="", username="", zone=""):
        req = self.delete_user_request(timestamp=timestamp,
                                       cluster_id=cluster_id,
                                       username=username,
                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_user_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "delete_userInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "delete_userInput")

        if op["Elements"]["username"] is None:
            return ParameterRequiredError("username", "delete_userInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "delete_userInput")

        return None

    def describe_hpc_login_account_user_request(self,
                                                timestamp="",
                                                user_id="",
                                                zone=""):
        operation = {
            "API": "describe_hpc_login_account_user",
            "Method": "GET",
            "URI": "/api/user/account",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.describe_hpc_login_account_user_validate(operation)
        return Request(self.config, operation)

    def describe_hpc_login_account_user(self,
                                        timestamp="",
                                        user_id="",
                                        zone=""):
        req = self.describe_hpc_login_account_user_request(timestamp=timestamp,
                                                           user_id=user_id,
                                                           zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def describe_hpc_login_account_user_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError(
                "timestamp", "describe_hpc_login_account_userInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError(
                "zone", "describe_hpc_login_account_userInput")

        return None

    def list_users_request(self,
                           cluster_id="",
                           limit=None,
                           offset=None,
                           reverse=None,
                           search_word="",
                           sort_key="",
                           timestamp="",
                           user_id="",
                           zone=""):
        operation = {
            "API": "list_users",
            "Method": "GET",
            "URI": "/api/user",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_users_validate(operation)
        return Request(self.config, operation)

    def list_users(self,
                   cluster_id="",
                   limit=None,
                   offset=None,
                   reverse=None,
                   search_word="",
                   sort_key="",
                   timestamp="",
                   user_id="",
                   zone=""):
        req = self.list_users_request(cluster_id=cluster_id,
                                      limit=limit,
                                      offset=offset,
                                      reverse=reverse,
                                      search_word=search_word,
                                      sort_key=sort_key,
                                      timestamp=timestamp,
                                      user_id=user_id,
                                      zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_users_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "list_usersInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_usersInput")

        return None

    def modify_user_request(self,
                            timestamp="",
                            cluster_id="",
                            new_password="",
                            username="",
                            zone=""):
        operation = {
            "API": "modify_user",
            "Method": "POST",
            "URI": "/api/user/modifyUser",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if new_password:
            operation["Elements"].update({"new_password": new_password})
        if username:
            operation["Elements"].update({"username": username})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_user_validate(operation)
        return Request(self.config, operation)

    def modify_user(self,
                    timestamp="",
                    cluster_id="",
                    new_password="",
                    username="",
                    zone=""):
        req = self.modify_user_request(timestamp=timestamp,
                                       cluster_id=cluster_id,
                                       new_password=new_password,
                                       username=username,
                                       zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_user_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp", "modify_userInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id", "modify_userInput")

        if op["Elements"]["new_password"] is None:
            return ParameterRequiredError("new_password", "modify_userInput")

        if op["Elements"]["username"] is None:
            return ParameterRequiredError("username", "modify_userInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_userInput")

        return None

    def file_create_template_request(self,
                                     timestamp="",
                                     zone="",
                                     file_name="",
                                     format="",
                                     text=""):
        operation = {
            "API": "file_create_template",
            "Method": "POST",
            "URI": "/api/filetemplate/createFileTemp",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if file_name:
            operation["Elements"].update({"file_name": file_name})
        if format:
            operation["Elements"].update({"format": format})
        if text:
            operation["Elements"].update({"text": text})
        self.file_create_template_validate(operation)
        return Request(self.config, operation)

    def file_create_template(self,
                             timestamp="",
                             zone="",
                             file_name="",
                             format="",
                             text=""):
        req = self.file_create_template_request(timestamp=timestamp,
                                                zone=zone,
                                                file_name=file_name,
                                                format=format,
                                                text=text)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def file_create_template_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "file_create_templateInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "file_create_templateInput")

        if op["Elements"]["file_name"] is None:
            return ParameterRequiredError("file_name",
                                          "file_create_templateInput")

        if op["Elements"]["format"] is None:
            return ParameterRequiredError("format",
                                          "file_create_templateInput")

        return None

    def file_list_templates_request(self,
                                    limit=None,
                                    offset=None,
                                    timestamp="",
                                    zone=""):
        operation = {
            "API": "file_list_templates",
            "Method": "GET",
            "URI": "/api/filetemplate/tempList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.file_list_templates_validate(operation)
        return Request(self.config, operation)

    def file_list_templates(self,
                            limit=None,
                            offset=None,
                            timestamp="",
                            zone=""):
        req = self.file_list_templates_request(limit=limit,
                                               offset=offset,
                                               timestamp=timestamp,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def file_list_templates_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "file_list_templatesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "file_list_templatesInput")

        return None

    def file_template_delete_request(self, file_id="", timestamp="", zone=""):
        operation = {
            "API": "file_template_delete",
            "Method": "GET",
            "URI": "/api/filetemplate/tempDelete",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if file_id:
            operation["Params"].update({"file_id": file_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.file_template_delete_validate(operation)
        return Request(self.config, operation)

    def file_template_delete(self, file_id="", timestamp="", zone=""):
        req = self.file_template_delete_request(file_id=file_id,
                                                timestamp=timestamp,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def file_template_delete_validate(op):
        if op["Params"]["file_id"] is None:
            return ParameterRequiredError("file_id",
                                          "file_template_deleteInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "file_template_deleteInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "file_template_deleteInput")

        return None

    def file_template_detail_request(self, file_id="", timestamp="", zone=""):
        operation = {
            "API": "file_template_detail",
            "Method": "GET",
            "URI": "/api/filetemplate/tempDetail",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if file_id:
            operation["Params"].update({"file_id": file_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.file_template_detail_validate(operation)
        return Request(self.config, operation)

    def file_template_detail(self, file_id="", timestamp="", zone=""):
        req = self.file_template_detail_request(file_id=file_id,
                                                timestamp=timestamp,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def file_template_detail_validate(op):
        if op["Params"]["file_id"] is None:
            return ParameterRequiredError("file_id",
                                          "file_template_detailInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "file_template_detailInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "file_template_detailInput")

        return None

    def file_template_update_request(self,
                                     timestamp="",
                                     zone="",
                                     file_id="",
                                     file_name="",
                                     format="",
                                     text=""):
        operation = {
            "API": "file_template_update",
            "Method": "POST",
            "URI": "/api/filetemplate/updateFileTemp",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if file_id:
            operation["Elements"].update({"file_id": file_id})
        if file_name:
            operation["Elements"].update({"file_name": file_name})
        if format:
            operation["Elements"].update({"format": format})
        if text:
            operation["Elements"].update({"text": text})
        self.file_template_update_validate(operation)
        return Request(self.config, operation)

    def file_template_update(self,
                             timestamp="",
                             zone="",
                             file_id="",
                             file_name="",
                             format="",
                             text=""):
        req = self.file_template_update_request(timestamp=timestamp,
                                                zone=zone,
                                                file_id=file_id,
                                                file_name=file_name,
                                                format=format,
                                                text=text)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def file_template_update_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "file_template_updateInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "file_template_updateInput")

        if op["Elements"]["file_id"] is None:
            return ParameterRequiredError("file_id",
                                          "file_template_updateInput")

        if op["Elements"]["file_name"] is None:
            return ParameterRequiredError("file_name",
                                          "file_template_updateInput")

        if op["Elements"]["format"] is None:
            return ParameterRequiredError("format",
                                          "file_template_updateInput")

        return None

    def get_charge_records_request(self,
                                   end_time="",
                                   limit=None,
                                   offset=None,
                                   resource="",
                                   start_time="",
                                   timestamp="",
                                   user_id="",
                                   zone=""):
        operation = {
            "API": "get_charge_records",
            "Method": "GET",
            "URI": "/api/iaas/getChargeRecords",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if resource:
            operation["Params"].update({"resource": resource})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_charge_records_validate(operation)
        return Request(self.config, operation)

    def get_charge_records(self,
                           end_time="",
                           limit=None,
                           offset=None,
                           resource="",
                           start_time="",
                           timestamp="",
                           user_id="",
                           zone=""):
        req = self.get_charge_records_request(end_time=end_time,
                                              limit=limit,
                                              offset=offset,
                                              resource=resource,
                                              start_time=start_time,
                                              timestamp=timestamp,
                                              user_id=user_id,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_charge_records_validate(op):

        if op["Params"]["resource"] is None:
            return ParameterRequiredError("resource",
                                          "get_charge_recordsInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_charge_recordsInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "get_charge_recordsInput")

        return None

    def job_create_template_request(self,
                                    timestamp="",
                                    zone="",
                                    cluster_id="",
                                    cmd_line="",
                                    cmd_line_type="",
                                    core_limit=None,
                                    host_name="",
                                    job_name="",
                                    job_priority=None,
                                    resource_limit="",
                                    resources="",
                                    run_user="",
                                    scheduler_queue_name="",
                                    stderr_redirect_path="",
                                    stderr_redirect_path_type="",
                                    stdout_redirect_path="",
                                    stdout_redirect_path_type="",
                                    temp_name="",
                                    user_id=""):
        operation = {
            "API": "job_create_template",
            "Method": "POST",
            "URI": "/api/jobtemplate/createJobTemp",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cmd_line:
            operation["Elements"].update({"cmd_line": cmd_line})
        if cmd_line_type:
            operation["Elements"].update({"cmd_line_type": cmd_line_type})
        if core_limit:
            operation["Elements"].update({"core_limit": core_limit})
        if host_name:
            operation["Elements"].update({"host_name": host_name})
        if job_name:
            operation["Elements"].update({"job_name": job_name})
        if job_priority:
            operation["Elements"].update({"job_priority": job_priority})
        if resource_limit:
            operation["Elements"].update({"resource_limit": resource_limit})
        if resources:
            operation["Elements"].update({"resources": resources})
        if run_user:
            operation["Elements"].update({"run_user": run_user})
        if scheduler_queue_name:
            operation["Elements"].update(
                {"scheduler_queue_name": scheduler_queue_name})
        if stderr_redirect_path:
            operation["Elements"].update(
                {"stderr_redirect_path": stderr_redirect_path})
        if stderr_redirect_path_type:
            operation["Elements"].update(
                {"stderr_redirect_path_type": stderr_redirect_path_type})
        if stdout_redirect_path:
            operation["Elements"].update(
                {"stdout_redirect_path": stdout_redirect_path})
        if stdout_redirect_path_type:
            operation["Elements"].update(
                {"stdout_redirect_path_type": stdout_redirect_path_type})
        if temp_name:
            operation["Elements"].update({"temp_name": temp_name})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        self.job_create_template_validate(operation)
        return Request(self.config, operation)

    def job_create_template(self,
                            timestamp="",
                            zone="",
                            cluster_id="",
                            cmd_line="",
                            cmd_line_type="",
                            core_limit=None,
                            host_name="",
                            job_name="",
                            job_priority=None,
                            resource_limit="",
                            resources="",
                            run_user="",
                            scheduler_queue_name="",
                            stderr_redirect_path="",
                            stderr_redirect_path_type="",
                            stdout_redirect_path="",
                            stdout_redirect_path_type="",
                            temp_name="",
                            user_id=""):
        req = self.job_create_template_request(
            timestamp=timestamp,
            zone=zone,
            cluster_id=cluster_id,
            cmd_line=cmd_line,
            cmd_line_type=cmd_line_type,
            core_limit=core_limit,
            host_name=host_name,
            job_name=job_name,
            job_priority=job_priority,
            resource_limit=resource_limit,
            resources=resources,
            run_user=run_user,
            scheduler_queue_name=scheduler_queue_name,
            stderr_redirect_path=stderr_redirect_path,
            stderr_redirect_path_type=stderr_redirect_path_type,
            stdout_redirect_path=stdout_redirect_path,
            stdout_redirect_path_type=stdout_redirect_path_type,
            temp_name=temp_name,
            user_id=user_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def job_create_template_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "job_create_templateInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "job_create_templateInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "job_create_templateInput")

        if op["Elements"]["temp_name"] is None:
            return ParameterRequiredError("temp_name",
                                          "job_create_templateInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id",
                                          "job_create_templateInput")

        return None

    def job_list_templates_request(self,
                                   cluster_id="",
                                   limit=None,
                                   offset=None,
                                   search_word="",
                                   timestamp="",
                                   user_id="",
                                   zone=""):
        operation = {
            "API": "job_list_templates",
            "Method": "GET",
            "URI": "/api/jobtemplate/tempList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if user_id:
            operation["Params"].update({"user_id": user_id})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.job_list_templates_validate(operation)
        return Request(self.config, operation)

    def job_list_templates(self,
                           cluster_id="",
                           limit=None,
                           offset=None,
                           search_word="",
                           timestamp="",
                           user_id="",
                           zone=""):
        req = self.job_list_templates_request(cluster_id=cluster_id,
                                              limit=limit,
                                              offset=offset,
                                              search_word=search_word,
                                              timestamp=timestamp,
                                              user_id=user_id,
                                              zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def job_list_templates_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "job_list_templatesInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "job_list_templatesInput")

        if op["Params"]["user_id"] is None:
            return ParameterRequiredError("user_id", "job_list_templatesInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "job_list_templatesInput")

        return None

    def job_template_delete_request(self, temp_id="", timestamp="", zone=""):
        operation = {
            "API": "job_template_delete",
            "Method": "GET",
            "URI": "/api/jobtemplate/tempDelete",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if temp_id:
            operation["Params"].update({"temp_id": temp_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.job_template_delete_validate(operation)
        return Request(self.config, operation)

    def job_template_delete(self, temp_id="", timestamp="", zone=""):
        req = self.job_template_delete_request(temp_id=temp_id,
                                               timestamp=timestamp,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def job_template_delete_validate(op):
        if op["Params"]["temp_id"] is None:
            return ParameterRequiredError("temp_id",
                                          "job_template_deleteInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "job_template_deleteInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "job_template_deleteInput")

        return None

    def job_template_detail_request(self, temp_id="", timestamp="", zone=""):
        operation = {
            "API": "job_template_detail",
            "Method": "GET",
            "URI": "/api/jobtemplate/tempDetail",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if temp_id:
            operation["Params"].update({"temp_id": temp_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.job_template_detail_validate(operation)
        return Request(self.config, operation)

    def job_template_detail(self, temp_id="", timestamp="", zone=""):
        req = self.job_template_detail_request(temp_id=temp_id,
                                               timestamp=timestamp,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def job_template_detail_validate(op):
        if op["Params"]["temp_id"] is None:
            return ParameterRequiredError("temp_id",
                                          "job_template_detailInput")

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "job_template_detailInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "job_template_detailInput")

        return None

    def job_template_update_request(self,
                                    timestamp="",
                                    zone="",
                                    cluster_id="",
                                    cmd_line="",
                                    core_limit=None,
                                    host_name="",
                                    job_name="",
                                    job_priority=None,
                                    resource_limit="",
                                    resources="",
                                    run_user="",
                                    scheduler_queue_name="",
                                    stderr_redirect_path="",
                                    stdout_redirect_path="",
                                    temp_id="",
                                    temp_name="",
                                    user_id=""):
        operation = {
            "API": "job_template_update",
            "Method": "POST",
            "URI": "/api/jobtemplate/updateJobTemp",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cmd_line:
            operation["Elements"].update({"cmd_line": cmd_line})
        if core_limit:
            operation["Elements"].update({"core_limit": core_limit})
        if host_name:
            operation["Elements"].update({"host_name": host_name})
        if job_name:
            operation["Elements"].update({"job_name": job_name})
        if job_priority:
            operation["Elements"].update({"job_priority": job_priority})
        if resource_limit:
            operation["Elements"].update({"resource_limit": resource_limit})
        if resources:
            operation["Elements"].update({"resources": resources})
        if run_user:
            operation["Elements"].update({"run_user": run_user})
        if scheduler_queue_name:
            operation["Elements"].update(
                {"scheduler_queue_name": scheduler_queue_name})
        if stderr_redirect_path:
            operation["Elements"].update(
                {"stderr_redirect_path": stderr_redirect_path})
        if stdout_redirect_path:
            operation["Elements"].update(
                {"stdout_redirect_path": stdout_redirect_path})
        if temp_id:
            operation["Elements"].update({"temp_id": temp_id})
        if temp_name:
            operation["Elements"].update({"temp_name": temp_name})
        if user_id:
            operation["Elements"].update({"user_id": user_id})
        self.job_template_update_validate(operation)
        return Request(self.config, operation)

    def job_template_update(self,
                            timestamp="",
                            zone="",
                            cluster_id="",
                            cmd_line="",
                            core_limit=None,
                            host_name="",
                            job_name="",
                            job_priority=None,
                            resource_limit="",
                            resources="",
                            run_user="",
                            scheduler_queue_name="",
                            stderr_redirect_path="",
                            stdout_redirect_path="",
                            temp_id="",
                            temp_name="",
                            user_id=""):
        req = self.job_template_update_request(
            timestamp=timestamp,
            zone=zone,
            cluster_id=cluster_id,
            cmd_line=cmd_line,
            core_limit=core_limit,
            host_name=host_name,
            job_name=job_name,
            job_priority=job_priority,
            resource_limit=resource_limit,
            resources=resources,
            run_user=run_user,
            scheduler_queue_name=scheduler_queue_name,
            stderr_redirect_path=stderr_redirect_path,
            stdout_redirect_path=stdout_redirect_path,
            temp_id=temp_id,
            temp_name=temp_name,
            user_id=user_id)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def job_template_update_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "job_template_updateInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "job_template_updateInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "job_template_updateInput")

        if op["Elements"]["temp_id"] is None:
            return ParameterRequiredError("temp_id",
                                          "job_template_updateInput")

        if op["Elements"]["temp_name"] is None:
            return ParameterRequiredError("temp_name",
                                          "job_template_updateInput")

        if op["Elements"]["user_id"] is None:
            return ParameterRequiredError("user_id",
                                          "job_template_updateInput")

        return None

    def add_ehpc_queue_strategy_request(self,
                                        timestamp="",
                                        zone="",
                                        cluster_id="",
                                        min_nodes_or_max_cores=None,
                                        op_interval=None,
                                        op_type=None,
                                        queue_id="",
                                        run_now=None):
        operation = {
            "API": "add_ehpc_queue_strategy",
            "Method": "POST",
            "URI": "/api/queue/ehpc/addStrategy",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if min_nodes_or_max_cores:
            operation["Elements"].update(
                {"min_nodes_or_max_cores": min_nodes_or_max_cores})
        if op_interval:
            operation["Elements"].update({"op_interval": op_interval})
        if op_type:
            operation["Elements"].update({"op_type": op_type})
        if queue_id:
            operation["Elements"].update({"queue_id": queue_id})
        if run_now:
            operation["Elements"].update({"run_now": run_now})
        self.add_ehpc_queue_strategy_validate(operation)
        return Request(self.config, operation)

    def add_ehpc_queue_strategy(self,
                                timestamp="",
                                zone="",
                                cluster_id="",
                                min_nodes_or_max_cores=None,
                                op_interval=None,
                                op_type=None,
                                queue_id="",
                                run_now=None):
        req = self.add_ehpc_queue_strategy_request(
            timestamp=timestamp,
            zone=zone,
            cluster_id=cluster_id,
            min_nodes_or_max_cores=min_nodes_or_max_cores,
            op_interval=op_interval,
            op_type=op_type,
            queue_id=queue_id,
            run_now=run_now)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def add_ehpc_queue_strategy_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "add_ehpc_queue_strategyInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "add_ehpc_queue_strategyInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "add_ehpc_queue_strategyInput")

        if op["Elements"]["min_nodes_or_max_cores"] is None:
            return ParameterRequiredError("min_nodes_or_max_cores",
                                          "add_ehpc_queue_strategyInput")

        if op["Elements"]["op_interval"] is None:
            return ParameterRequiredError("op_interval",
                                          "add_ehpc_queue_strategyInput")

        if op["Elements"]["op_type"] is None:
            return ParameterRequiredError("op_type",
                                          "add_ehpc_queue_strategyInput")

        if op["Elements"]["queue_id"] is None:
            return ParameterRequiredError("queue_id",
                                          "add_ehpc_queue_strategyInput")

        return None

    def del_ehpc_queue_strategy_request(self,
                                        timestamp="",
                                        cluster_id="",
                                        op_type=None,
                                        queue_id="",
                                        zone=""):
        operation = {
            "API": "del_ehpc_queue_strategy",
            "Method": "POST",
            "URI": "/api/queue/ehpc/delStrategy",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if op_type:
            operation["Elements"].update({"op_type": op_type})
        if queue_id:
            operation["Elements"].update({"queue_id": queue_id})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.del_ehpc_queue_strategy_validate(operation)
        return Request(self.config, operation)

    def del_ehpc_queue_strategy(self,
                                timestamp="",
                                cluster_id="",
                                op_type=None,
                                queue_id="",
                                zone=""):
        req = self.del_ehpc_queue_strategy_request(timestamp=timestamp,
                                                   cluster_id=cluster_id,
                                                   op_type=op_type,
                                                   queue_id=queue_id,
                                                   zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def del_ehpc_queue_strategy_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "del_ehpc_queue_strategyInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "del_ehpc_queue_strategyInput")

        if op["Elements"]["op_type"] is None:
            return ParameterRequiredError("op_type",
                                          "del_ehpc_queue_strategyInput")

        if "op_type" in op["Elements"] and op["Elements"]["op_type"]:

            op_type_valid_values = ["0", "1"]
            if op["Elements"]["op_type"] not in op_type_valid_values:
                return ParameterValueNotAllowedError("op_type",
                                                     op["Elements"]["op_type"],
                                                     op_type_valid_values)

        if op["Elements"]["queue_id"] is None:
            return ParameterRequiredError("queue_id",
                                          "del_ehpc_queue_strategyInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "del_ehpc_queue_strategyInput")

        return None

    def enable_ehpc_queue_strategy_request(self,
                                           timestamp="",
                                           is_enabled=None,
                                           op_type=None,
                                           queue_id="",
                                           run_now=None,
                                           zone=""):
        operation = {
            "API": "enable_ehpc_queue_strategy",
            "Method": "POST",
            "URI": "/api/queue/ehpc/enableStrategy",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if is_enabled:
            operation["Elements"].update({"is_enabled": is_enabled})
        if op_type:
            operation["Elements"].update({"op_type": op_type})
        if queue_id:
            operation["Elements"].update({"queue_id": queue_id})
        if run_now:
            operation["Elements"].update({"run_now": run_now})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.enable_ehpc_queue_strategy_validate(operation)
        return Request(self.config, operation)

    def enable_ehpc_queue_strategy(self,
                                   timestamp="",
                                   is_enabled=None,
                                   op_type=None,
                                   queue_id="",
                                   run_now=None,
                                   zone=""):
        req = self.enable_ehpc_queue_strategy_request(timestamp=timestamp,
                                                      is_enabled=is_enabled,
                                                      op_type=op_type,
                                                      queue_id=queue_id,
                                                      run_now=run_now,
                                                      zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def enable_ehpc_queue_strategy_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "enable_ehpc_queue_strategyInput")

        if op["Elements"]["is_enabled"] is None:
            return ParameterRequiredError("is_enabled",
                                          "enable_ehpc_queue_strategyInput")

        if "is_enabled" in op["Elements"] and op["Elements"]["is_enabled"]:

            is_enabled_valid_values = ["0", "1"]
            if op["Elements"]["is_enabled"] not in is_enabled_valid_values:
                return ParameterValueNotAllowedError(
                    "is_enabled", op["Elements"]["is_enabled"],
                    is_enabled_valid_values)

        if op["Elements"]["op_type"] is None:
            return ParameterRequiredError("op_type",
                                          "enable_ehpc_queue_strategyInput")

        if "op_type" in op["Elements"] and op["Elements"]["op_type"]:

            op_type_valid_values = ["0", "1"]
            if op["Elements"]["op_type"] not in op_type_valid_values:
                return ParameterValueNotAllowedError("op_type",
                                                     op["Elements"]["op_type"],
                                                     op_type_valid_values)

        if op["Elements"]["queue_id"] is None:
            return ParameterRequiredError("queue_id",
                                          "enable_ehpc_queue_strategyInput")

        if "run_now" in op["Elements"] and op["Elements"]["run_now"]:

            run_now_valid_values = ["0", "1"]
            if op["Elements"]["run_now"] not in run_now_valid_values:
                return ParameterValueNotAllowedError("run_now",
                                                     op["Elements"]["run_now"],
                                                     run_now_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "enable_ehpc_queue_strategyInput")

        return None

    def get_ehpc_queue_strategy_list_request(self,
                                             cluster_id="",
                                             limit=None,
                                             offset=None,
                                             op_is_enabled=None,
                                             op_type=None,
                                             queue_ids=list(),
                                             reverse=None,
                                             sort_key="",
                                             timestamp="",
                                             zone=""):
        operation = {
            "API": "get_ehpc_queue_strategy_list",
            "Method": "GET",
            "URI": "/api/queue/ehpc/getStrategyList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if op_is_enabled:
            operation["Params"].update({"op_is_enabled": op_is_enabled})

        if op_type:
            operation["Params"].update({"op_type": op_type})

        if queue_ids != list() and queue_ids:
            operation["Params"].update({"queue_ids": queue_ids})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_ehpc_queue_strategy_list_validate(operation)
        return Request(self.config, operation)

    def get_ehpc_queue_strategy_list(self,
                                     cluster_id="",
                                     limit=None,
                                     offset=None,
                                     op_is_enabled=None,
                                     op_type=None,
                                     queue_ids=list(),
                                     reverse=None,
                                     sort_key="",
                                     timestamp="",
                                     zone=""):
        req = self.get_ehpc_queue_strategy_list_request(
            cluster_id=cluster_id,
            limit=limit,
            offset=offset,
            op_is_enabled=op_is_enabled,
            op_type=op_type,
            queue_ids=queue_ids,
            reverse=reverse,
            sort_key=sort_key,
            timestamp=timestamp,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_ehpc_queue_strategy_list_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "get_ehpc_queue_strategy_listInput")

        if "op_is_enabled" in op["Params"] and op["Params"]["op_is_enabled"]:

            op_is_enabled_valid_values = ["0", "1"]
            if op["Params"]["op_is_enabled"] not in op_is_enabled_valid_values:
                return ParameterValueNotAllowedError(
                    "op_is_enabled", op["Params"]["op_is_enabled"],
                    op_is_enabled_valid_values)

        if "op_type" in op["Params"] and op["Params"]["op_type"]:

            op_type_valid_values = ["0", "1"]
            if op["Params"]["op_type"] not in op_type_valid_values:
                return ParameterValueNotAllowedError("op_type",
                                                     op["Params"]["op_type"],
                                                     op_type_valid_values)

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_ehpc_queue_strategy_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_ehpc_queue_strategy_listInput")

        return None

    def get_ehpc_queue_strategy_log_list_request(self,
                                                 cluster_id="",
                                                 limit=None,
                                                 offset=None,
                                                 op_status="",
                                                 op_type=None,
                                                 queue_ids=list(),
                                                 reverse=None,
                                                 sort_key="",
                                                 timestamp="",
                                                 zone=""):
        operation = {
            "API": "get_ehpc_queue_strategy_log_list",
            "Method": "GET",
            "URI": "/api/queue/ehpc/getStrategyLogList",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if op_status:
            operation["Params"].update({"op_status": op_status})

        if op_type:
            operation["Params"].update({"op_type": op_type})

        if queue_ids != list() and queue_ids:
            operation["Params"].update({"queue_ids": queue_ids})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_ehpc_queue_strategy_log_list_validate(operation)
        return Request(self.config, operation)

    def get_ehpc_queue_strategy_log_list(self,
                                         cluster_id="",
                                         limit=None,
                                         offset=None,
                                         op_status="",
                                         op_type=None,
                                         queue_ids=list(),
                                         reverse=None,
                                         sort_key="",
                                         timestamp="",
                                         zone=""):
        req = self.get_ehpc_queue_strategy_log_list_request(
            cluster_id=cluster_id,
            limit=limit,
            offset=offset,
            op_status=op_status,
            op_type=op_type,
            queue_ids=queue_ids,
            reverse=reverse,
            sort_key=sort_key,
            timestamp=timestamp,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_ehpc_queue_strategy_log_list_validate(op):
        if op["Params"]["cluster_id"] is None:
            return ParameterRequiredError(
                "cluster_id", "get_ehpc_queue_strategy_log_listInput")

        if "op_type" in op["Params"] and op["Params"]["op_type"]:

            op_type_valid_values = ["0", "1"]
            if op["Params"]["op_type"] not in op_type_valid_values:
                return ParameterValueNotAllowedError("op_type",
                                                     op["Params"]["op_type"],
                                                     op_type_valid_values)

        if "reverse" in op["Params"] and op["Params"]["reverse"]:

            reverse_valid_values = ["0", "1"]
            if op["Params"]["reverse"] not in reverse_valid_values:
                return ParameterValueNotAllowedError("reverse",
                                                     op["Params"]["reverse"],
                                                     reverse_valid_values)

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError(
                "timestamp", "get_ehpc_queue_strategy_log_listInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError(
                "zone", "get_ehpc_queue_strategy_log_listInput")

        return None

    def modify_ehpc_queue_strategy_request(self,
                                           timestamp="",
                                           cluster_id="",
                                           min_nodes_or_max_cores=None,
                                           op_interval=None,
                                           op_type=None,
                                           queue_id="",
                                           run_now=None,
                                           zone=""):
        operation = {
            "API": "modify_ehpc_queue_strategy",
            "Method": "POST",
            "URI": "/api/queue/ehpc/modifyStrategy",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if min_nodes_or_max_cores:
            operation["Elements"].update(
                {"min_nodes_or_max_cores": min_nodes_or_max_cores})
        if op_interval:
            operation["Elements"].update({"op_interval": op_interval})
        if op_type:
            operation["Elements"].update({"op_type": op_type})
        if queue_id:
            operation["Elements"].update({"queue_id": queue_id})
        if run_now:
            operation["Elements"].update({"run_now": run_now})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_ehpc_queue_strategy_validate(operation)
        return Request(self.config, operation)

    def modify_ehpc_queue_strategy(self,
                                   timestamp="",
                                   cluster_id="",
                                   min_nodes_or_max_cores=None,
                                   op_interval=None,
                                   op_type=None,
                                   queue_id="",
                                   run_now=None,
                                   zone=""):
        req = self.modify_ehpc_queue_strategy_request(
            timestamp=timestamp,
            cluster_id=cluster_id,
            min_nodes_or_max_cores=min_nodes_or_max_cores,
            op_interval=op_interval,
            op_type=op_type,
            queue_id=queue_id,
            run_now=run_now,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_ehpc_queue_strategy_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_ehpc_queue_strategyInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "modify_ehpc_queue_strategyInput")

        if op["Elements"]["min_nodes_or_max_cores"] is None:
            return ParameterRequiredError("min_nodes_or_max_cores",
                                          "modify_ehpc_queue_strategyInput")

        if op["Elements"]["op_interval"] is None:
            return ParameterRequiredError("op_interval",
                                          "modify_ehpc_queue_strategyInput")

        if op["Elements"]["op_type"] is None:
            return ParameterRequiredError("op_type",
                                          "modify_ehpc_queue_strategyInput")

        if "op_type" in op["Elements"] and op["Elements"]["op_type"]:

            op_type_valid_values = ["0", "1"]
            if op["Elements"]["op_type"] not in op_type_valid_values:
                return ParameterValueNotAllowedError("op_type",
                                                     op["Elements"]["op_type"],
                                                     op_type_valid_values)

        if op["Elements"]["queue_id"] is None:
            return ParameterRequiredError("queue_id",
                                          "modify_ehpc_queue_strategyInput")

        if "run_now" in op["Elements"] and op["Elements"]["run_now"]:

            run_now_valid_values = ["0", "1"]
            if op["Elements"]["run_now"] not in run_now_valid_values:
                return ParameterValueNotAllowedError("run_now",
                                                     op["Elements"]["run_now"],
                                                     run_now_valid_values)

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "modify_ehpc_queue_strategyInput")

        return None

    def delete_simulation_jobs_request(self,
                                       timestamp="",
                                       cluster_id="",
                                       job_ids=list(),
                                       zone=""):
        operation = {
            "API": "delete_simulation_jobs",
            "Method": "POST",
            "URI": "/api/simulation/deleteJobs",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if job_ids:
            operation["Elements"].update({"job_ids": job_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.delete_simulation_jobs_validate(operation)
        return Request(self.config, operation)

    def delete_simulation_jobs(self,
                               timestamp="",
                               cluster_id="",
                               job_ids=list(),
                               zone=""):
        req = self.delete_simulation_jobs_request(timestamp=timestamp,
                                                  cluster_id=cluster_id,
                                                  job_ids=job_ids,
                                                  zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def delete_simulation_jobs_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "delete_simulation_jobsInput")

        if op["Elements"]["job_ids"] is None:
            return ParameterRequiredError("job_ids",
                                          "delete_simulation_jobsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "delete_simulation_jobsInput")

        return None

    def get_simulation_job_detail_request(self,
                                          sjob_id="",
                                          cluster_id="",
                                          timestamp="",
                                          zone=""):
        operation = {
            "API": "get_simulation_job_detail",
            "Method": "GET",
            "URI": "/api/simulation/jobdetail/<sjob_id>",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }
        if sjob_id:
            operation["Properties"].update({"sjob_id": sjob_id})

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.get_simulation_job_detail_validate(operation)
        return Request(self.config, operation)

    def get_simulation_job_detail(self,
                                  sjob_id="",
                                  cluster_id="",
                                  timestamp="",
                                  zone=""):
        req = self.get_simulation_job_detail_request(sjob_id=sjob_id,
                                                     cluster_id=cluster_id,
                                                     timestamp=timestamp,
                                                     zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def get_simulation_job_detail_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "get_simulation_job_detailInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone",
                                          "get_simulation_job_detailInput")

        return None

    def list_simulation_jobs_request(self,
                                     cluster_id="",
                                     cluster_type="",
                                     end_time="",
                                     hpcqueue_id="",
                                     job_status="",
                                     limit=None,
                                     offset=None,
                                     owner="",
                                     queue_name="",
                                     reverse=None,
                                     run_user="",
                                     search_word="",
                                     sjob_id="",
                                     software_list="",
                                     sort_key="",
                                     start_time="",
                                     submit_type=None,
                                     timestamp="",
                                     verbose=None,
                                     zone=""):
        operation = {
            "API": "list_simulation_jobs",
            "Method": "GET",
            "URI": "/api/simulation/list/job",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if cluster_id:
            operation["Params"].update({"cluster_id": cluster_id})

        if cluster_type:
            operation["Params"].update({"cluster_type": cluster_type})

        if end_time:
            operation["Params"].update({"end_time": end_time})

        if hpcqueue_id:
            operation["Params"].update({"hpcqueue_id": hpcqueue_id})

        if job_status:
            operation["Params"].update({"job_status": job_status})

        if limit:
            operation["Params"].update({"limit": limit})

        if offset:
            operation["Params"].update({"offset": offset})

        if owner:
            operation["Params"].update({"owner": owner})

        if queue_name:
            operation["Params"].update({"queue_name": queue_name})

        if reverse:
            operation["Params"].update({"reverse": reverse})

        if run_user:
            operation["Params"].update({"run_user": run_user})

        if search_word:
            operation["Params"].update({"search_word": search_word})

        if sjob_id:
            operation["Params"].update({"sjob_id": sjob_id})

        if software_list:
            operation["Params"].update({"software_list": software_list})

        if sort_key:
            operation["Params"].update({"sort_key": sort_key})

        if start_time:
            operation["Params"].update({"start_time": start_time})

        if submit_type:
            operation["Params"].update({"submit_type": submit_type})

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        if verbose:
            operation["Params"].update({"verbose": verbose})

        if zone:
            operation["Params"].update({"zone": zone})

        operation["Elements"] = dict()
        self.list_simulation_jobs_validate(operation)
        return Request(self.config, operation)

    def list_simulation_jobs(self,
                             cluster_id="",
                             cluster_type="",
                             end_time="",
                             hpcqueue_id="",
                             job_status="",
                             limit=None,
                             offset=None,
                             owner="",
                             queue_name="",
                             reverse=None,
                             run_user="",
                             search_word="",
                             sjob_id="",
                             software_list="",
                             sort_key="",
                             start_time="",
                             submit_type=None,
                             timestamp="",
                             verbose=None,
                             zone=""):
        req = self.list_simulation_jobs_request(cluster_id=cluster_id,
                                                cluster_type=cluster_type,
                                                end_time=end_time,
                                                hpcqueue_id=hpcqueue_id,
                                                job_status=job_status,
                                                limit=limit,
                                                offset=offset,
                                                owner=owner,
                                                queue_name=queue_name,
                                                reverse=reverse,
                                                run_user=run_user,
                                                search_word=search_word,
                                                sjob_id=sjob_id,
                                                software_list=software_list,
                                                sort_key=sort_key,
                                                start_time=start_time,
                                                submit_type=submit_type,
                                                timestamp=timestamp,
                                                verbose=verbose,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_simulation_jobs_validate(op):

        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "list_simulation_jobsInput")

        if op["Params"]["zone"] is None:
            return ParameterRequiredError("zone", "list_simulation_jobsInput")

        return None

    def stop_simulation_jobs_request(self,
                                     timestamp="",
                                     cluster_id="",
                                     job_ids=list(),
                                     zone=""):
        operation = {
            "API": "stop_simulation_jobs",
            "Method": "POST",
            "URI": "/api/simulation/stopJobs",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if job_ids:
            operation["Elements"].update({"job_ids": job_ids})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.stop_simulation_jobs_validate(operation)
        return Request(self.config, operation)

    def stop_simulation_jobs(self,
                             timestamp="",
                             cluster_id="",
                             job_ids=list(),
                             zone=""):
        req = self.stop_simulation_jobs_request(timestamp=timestamp,
                                                cluster_id=cluster_id,
                                                job_ids=job_ids,
                                                zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def stop_simulation_jobs_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "stop_simulation_jobsInput")

        if op["Elements"]["job_ids"] is None:
            return ParameterRequiredError("job_ids",
                                          "stop_simulation_jobsInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "stop_simulation_jobsInput")

        return None

    def submit_simulation_job_request(self,
                                      timestamp="",
                                      cluster_id="",
                                      cmd_line="",
                                      core_limit=None,
                                      input_file="",
                                      mem_limit=None,
                                      name="",
                                      resource_limit="",
                                      run_user="",
                                      scheduler_queue_name="",
                                      time_limit=None,
                                      zone=""):
        operation = {
            "API": "submit_simulation_job",
            "Method": "POST",
            "URI": "/api/simulation/submitJob",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if cmd_line:
            operation["Elements"].update({"cmd_line": cmd_line})
        if core_limit:
            operation["Elements"].update({"core_limit": core_limit})
        if input_file:
            operation["Elements"].update({"input_file": input_file})
        if mem_limit:
            operation["Elements"].update({"mem_limit": mem_limit})
        if name:
            operation["Elements"].update({"name": name})
        if resource_limit:
            operation["Elements"].update({"resource_limit": resource_limit})
        if run_user:
            operation["Elements"].update({"run_user": run_user})
        if scheduler_queue_name:
            operation["Elements"].update(
                {"scheduler_queue_name": scheduler_queue_name})
        if time_limit:
            operation["Elements"].update({"time_limit": time_limit})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.submit_simulation_job_validate(operation)
        return Request(self.config, operation)

    def submit_simulation_job(self,
                              timestamp="",
                              cluster_id="",
                              cmd_line="",
                              core_limit=None,
                              input_file="",
                              mem_limit=None,
                              name="",
                              resource_limit="",
                              run_user="",
                              scheduler_queue_name="",
                              time_limit=None,
                              zone=""):
        req = self.submit_simulation_job_request(
            timestamp=timestamp,
            cluster_id=cluster_id,
            cmd_line=cmd_line,
            core_limit=core_limit,
            input_file=input_file,
            mem_limit=mem_limit,
            name=name,
            resource_limit=resource_limit,
            run_user=run_user,
            scheduler_queue_name=scheduler_queue_name,
            time_limit=time_limit,
            zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def submit_simulation_job_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "submit_simulation_jobInput")

        if op["Elements"]["name"] is None:
            return ParameterRequiredError("name", "submit_simulation_jobInput")

        if op["Elements"]["run_user"] is None:
            return ParameterRequiredError("run_user",
                                          "submit_simulation_jobInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "submit_simulation_jobInput")

        return None

    def modify_cluster_node_request(self,
                                    timestamp="",
                                    cluster_id="",
                                    node_id="",
                                    node_name="",
                                    zone=""):
        operation = {
            "API": "modify_cluster_node",
            "Method": "POST",
            "URI": "/api/cluster/modifyClusterNode",
            "Headers": {
                "Host": self.config.host,
            },
            "Params": {},
            "Properties": {},
            "Body": None
        }

        if timestamp:
            operation["Params"].update({"timestamp": timestamp})

        operation["Elements"] = dict()
        if cluster_id:
            operation["Elements"].update({"cluster_id": cluster_id})
        if node_id:
            operation["Elements"].update({"node_id": node_id})
        if node_name:
            operation["Elements"].update({"node_name": node_name})
        if zone:
            operation["Elements"].update({"zone": zone})
        self.modify_cluster_node_validate(operation)
        return Request(self.config, operation)

    def modify_cluster_node(self,
                            timestamp="",
                            cluster_id="",
                            node_id="",
                            node_name="",
                            zone=""):
        req = self.modify_cluster_node_request(timestamp=timestamp,
                                               cluster_id=cluster_id,
                                               node_id=node_id,
                                               node_name=node_name,
                                               zone=zone)
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def modify_cluster_node_validate(op):
        if op["Params"]["timestamp"] is None:
            return ParameterRequiredError("timestamp",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["cluster_id"] is None:
            return ParameterRequiredError("cluster_id",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["node_id"] is None:
            return ParameterRequiredError("node_id",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["node_name"] is None:
            return ParameterRequiredError("node_name",
                                          "modify_cluster_nodeInput")

        if op["Elements"]["zone"] is None:
            return ParameterRequiredError("zone", "modify_cluster_nodeInput")

        return None
