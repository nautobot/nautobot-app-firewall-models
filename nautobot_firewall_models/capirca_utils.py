"""Management command to bootstrap dummy data for firewall model plugin."""

from nautobot_firewall_models.utils import model_to_json
from django.utils.module_loading import import_string

from capirca.lib.naming import Naming
from capirca.lib import policy
from django.core.exceptions import ValidationError

from nautobot_firewall_models.constants import CAPIRCA_OS_MAPPER, ACTION_MAP, LOGGING_MAP, CAPIRCA_MAPPER


def clean_list(_list, remove_empty=False):
    if remove_empty:
        _list = [i for i in _list if i]
    _list = list(set(_list))
    return _list


class PolicyToCapirca:
    def __init__(self, policy_obj, platform, *args, **kwargs):
        """Overload init to account for computed field."""
        self.policy_name = str(policy_obj)
        self.platform = CAPIRCA_OS_MAPPER.get(platform, platform)
        self.policy_obj = policy_obj.policy_details()
        self.address = {}
        self.service = {}
        self.policy = []
        self.pol_file = ""
        self.svc_file = ""
        self.net_file = ""
        self.cfg_file = ""

    def _get_address_details(self, data):
        if not data["status"]["value"] == "active":
            return {}
        if data.get("ip_range"):
            raise ValidationError(
                f"The ip_range object `{data['ip_range']['display']}` was attempted which is not supported by Capirca."
            )
        elif data.get("fqdn"):
            raise ValidationError(
                f"The fqdn object `{data['fqdn']['display']}` was attempted which is not supported by Capirca."
            )
        name = data["name"]
        if data.get("prefix"):
            value = data["prefix"]["prefix"]
        elif data.get("ip_address"):
            value = data["ip_address"]["address"]
        if not self.address.get(name):
            self.address[name] = [value]
        return name

    def _get_address_group_details(self, data):
        if not data["status"]["value"] == "active":
            return {}

        name = data["name"]
        address_group = []
        for address in data["address_objects"]:
            address_group.append(self._get_address_details(address))

        if not self.address.get("name"):
            self.address[name] = address_group

        return name

    def _get_service_details(self, data):
        if not data["status"]["value"] == "active":
            return {}
        ip_protocol = data["ip_protocol"].lower()
        if not ip_protocol in ["tcp", "udp"]:
            return {}

        name = data["name"]
        port = data["port"]

        value = f"{port}/{ip_protocol}"
        if not self.service.get(name):
            self.service[name] = [value]
        return (name, ip_protocol)

    def _get_service_group_details(self, data):
        if not data["status"]["value"] == "active":
            return {}

        name = data["name"]
        service_group = []
        for service in data["service_objects"]:
            svc_name, ip_protocol = self._get_service_details(service)
            service_group.append(svc_name)

        if not self.service.get("name"):
            self.service[name] = service_group

        return (name, ip_protocol)

    def get_policy_data(self):

        for rule in self.policy_obj:
            p_source_addr = []
            p_destination_addr = []
            p_service = []
            for source_address_group in rule["source_address_group"]:
                p_source_addr.append(self._get_address_group_details(model_to_json(source_address_group)))
            for source_address in rule["source_address"]:
                p_source_addr.append(self._get_address_details(model_to_json(source_address)))

            for destination_address_group in rule["destination_address_group"]:
                p_destination_addr.append(self._get_address_group_details(model_to_json(destination_address_group)))
            for destination_address in rule["destination_address"]:
                p_destination_addr.append(self._get_address_details(model_to_json(destination_address)))

            for service in rule["service"]:
                p_service.append(self._get_service_details(model_to_json(service)))
            for service_group in rule["service_group"]:
                p_service.append(self._get_service_group_details(model_to_json(service_group)))

            rule_details = {
                "rule_name": rule["rule"].name,
                "source-address": clean_list(p_source_addr, True),
                "from-zone": rule["source_zone"].name,
                "destination-address": clean_list(p_destination_addr, True),
                "to-zone": rule["destination_zone"].name,
                "destination-port": [i[0] for i in p_service],
                "protocol": clean_list([i[1].lower() for i in p_service]),
                "action": ACTION_MAP[rule["action"]],
                "logging": LOGGING_MAP[str(rule["log"]).lower()],
                "comment": rule["request_id"],
            }
            self.policy.append(rule_details)

    def get_capirca_cfg(self):
        if not self.policy:
            self.get_policy_data()

        # TODO: Allow for mapping this model from user defined
        if not CAPIRCA_MAPPER.get(self.platform):
            raise ValidationError(
                f"The platform slug {self.platform} was not one of the supported options {list(CAPIRCA_MAPPER.keys())}."
            )

        pol = []
        for index, rule in enumerate(self.policy):

            if CAPIRCA_MAPPER[self.platform]["type"] == "zone":
                pol.append("header {")
                _header = f"  target:: {self.platform} from-zone {rule['from-zone']} to-zone {rule['to-zone']}"
                pol.append(_header)
                pol.append("}")
                pol.append("")
            elif index == 0:
                pol.append("header {")
                _header = f"  target:: {self.platform}"
                if CAPIRCA_MAPPER[self.platform]["type"] == "filter-name":
                    _header += f" {self.policy_name}"
                pol.append(_header)
                pol.append("}")
                pol.append("")

            del rule["from-zone"]
            del rule["to-zone"]

            pol.append(f"term {rule['rule_name']}" + " {")
            del rule["rule_name"]
            for key, value in rule.items():
                if not value:
                    continue
                if isinstance(value, list):
                    for item in value:
                        if not item:
                            continue
                        pol.append(f"  {key}:: {item}")
                else:
                    pol.append(f"  {key}:: {value}")
            pol.append("}")
            pol.append("")

        networkdata = []
        for name, addresses in self.address.items():
            addresses = clean_list(addresses, True)
            first_address = addresses.pop(0)
            networkdata.append(f"{name} = {first_address}")
            for address in addresses:
                networkdata.append(" " * (len(name) + 3) + address)

        servicedata = []
        for name, services in self.service.items():
            services = clean_list(services, True)
            first_service = services.pop(0)
            servicedata.append(f"{name} = {first_service}")
            for service in services:
                servicedata.append(" " * (len(name) + 3) + service)

        self.pol_file = "\n".join(pol)
        self.svc_file = "\n".join(servicedata)
        self.net_file = "\n".join(networkdata)

        defs = Naming(None)
        defs.ParseServiceList(servicedata)
        defs.ParseNetworkList(networkdata)
        pol = policy.ParsePolicy(self.pol_file, defs, optimize=True)

        self.cfg_file = str(import_string(CAPIRCA_MAPPER[self.platform]["lib"])(pol, 0))


class DevicePolicyToCapirca(PolicyToCapirca):
    def __init__(self, device_obj, *args, **kwargs):
        """Overload init to account for computed field."""
        self.policy_name = ""
        self.platform = CAPIRCA_OS_MAPPER.get(device_obj.platform.slug, device_obj.platform.slug)
        self.policy_objs = []
        self.address = {}
        self.service = {}
        self.policy = []
        policy_name = []
        self.pol_file = ""
        self.svc_file = ""
        self.net_file = ""
        self.cfg_file = ""

        for dynamic_group in device_obj.dynamic_groups.all():
            for policy_group in dynamic_group.policydynamicgroupm2m_set.all():
                self.policy_objs.append(policy_group.policy)
                policy_name.append(policy_group.policy.name)
        self.policy_name = "__".join(policy_name)

    def get_all_capirca_cfg(self):
        for pol in self.policy_objs:
            class_obj = PolicyToCapirca(pol, self.platform)
            class_obj.get_policy_data()
            self.address.update(class_obj.address)
            self.service.update(class_obj.service)
            self.policy.extend(class_obj.policy)

        self.get_capirca_cfg()
