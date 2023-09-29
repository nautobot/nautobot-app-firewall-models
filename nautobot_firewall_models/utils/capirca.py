"""Management command to bootstrap dummy data for firewall model plugin."""
# pylint: disable=too-many-instance-attributes,too-many-locals
import logging
import re
import unicodedata
from capirca.lib.naming import Naming
from capirca.lib import policy

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string

from nautobot.dcim.models import Platform

from nautobot_firewall_models.constants import (
    ALLOW_STATUS,
    CAPIRCA_OS_MAPPER,
    ACTION_MAP,
    LOGGING_MAP,
    CAPIRCA_MAPPER,
    PLUGIN_CFG,
)
from nautobot_firewall_models.utils import model_to_json

LOGGER = logging.getLogger(__name__)


def _slugify(value):
    """
    Taken from Django's implementation of slugify, to allow for capital letters.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def _list_slugify(values):
    """Function to go through list of names and slugify them."""
    return sorted([_slugify(i) for i in values])


def _clean_list(_list, remove_empty=False):
    """Remove duplicates and conditionally empty, such as None, in a list."""
    if remove_empty:
        _list = [i for i in _list if i]
    _list = list(set(_list))
    return sorted(_list)


def _get_instance_from_dict(obj):
    """Get DB object from serialized json."""
    if isinstance(obj, dict) and obj.get("id") and obj.get("object_type"):
        app, model = obj["object_type"].split(".")
        obj = ContentType.objects.get(app_label=app, model=model).get_object_for_this_type(id=obj["id"])
    return obj


def _check_status(status):
    """Check if status is active or as provided via plugin settings. If nothing, it is always good."""
    if not isinstance(status, str):
        status = _get_instance_from_dict(status).status.name
    if len(ALLOW_STATUS) == 0 or status not in ALLOW_STATUS:
        return True
    return False


def generate_capirca_config(servicedata, networkdata, pol, platform):
    """Given platform with pol, net, svc files have Capirca generate config."""
    defs = Naming(None)
    LOGGER.debug("Parsing Service List")
    defs.ParseServiceList(servicedata)
    LOGGER.debug("Parsing Network List")
    defs.ParseNetworkList(networkdata)
    LOGGER.debug("Parsing Policy")
    pol = policy.ParsePolicy(pol, defs, optimize=True)
    LOGGER.debug("Parsing Policy Completed")

    LOGGER.debug("Running Capirca Against: %s", str(CAPIRCA_MAPPER[platform]["lib"]))
    return str(import_string(CAPIRCA_MAPPER[platform]["lib"])(pol, 0))


class PolicyToCapirca:
    """Class object to convert Policy orm object to Capirca object."""

    def __init__(self, platform, policy_obj=None, **kwargs):
        """Overload init to account for computed field."""
        self.policy_name = str(policy_obj)
        self.platform_obj = Platform.objects.get(network_driver=platform)
        self.platform = CAPIRCA_OS_MAPPER.get(platform, platform)
        self.policy_details = None
        if policy_obj:
            self.policy_details = policy_obj.policy_details
        self.address = {}
        self.address_group = {}
        self.service = {}
        self.service_protocol = {}
        self.service_group_protocol = {}
        self.service_group = {}
        self.policy = []
        self.cap_policy = []
        self.pol_file = ""
        self.svc_file = ""
        self.net_file = ""
        self.cfg_file = ""
        # TODO: Evaluate if this is the best way to manage
        # Currently this hints as to when to use additional terms or headers
        _allow_list = self.platform_obj.custom_field_data.get("capirca_allow")
        self.cf_allow_list_enabled = bool("capirca_allow" in self.platform_obj.custom_field_data)
        self.cf_allow_list = _allow_list if _allow_list else []

        LOGGER.debug("Processing Policy: `%s`", str(self.policy_name))
        LOGGER.debug("Original Platform Name: `%s`", str(platform))
        LOGGER.debug("Capirca Platform Name: `%s`", str(self.platform))
        LOGGER.debug("cf_allow_list_enabled: `%s`", str(self.cf_allow_list_enabled))
        LOGGER.debug("cf_allow_list: `%s`", str(self.cf_allow_list))

    @staticmethod
    def _check_for_empty(_type, start1, start2, end1, end2):
        """Check is somehow all the rules were empty, such as status was changed on all."""
        start = len(start1) + len(start2)
        end = len(end1) + len(end2)
        if start > 0 and end == 0:
            data = ", ".join([str(value) for value in start1]) + ", ".join([str(value) for value in start2])
            raise ValidationError(
                f"{_type} with values of `{data}` had all instances removed."
                "The likely cause of this is either the status was not active or "
                "Capirca does not support the value you provided, and was removed from consideration"
            )

    def _format_data(self, data, _type):
        def format_address(data, name):
            """Format address objects, looking for the address type."""
            keys = ["ip_range", "fqdn", "prefix", "ip_address"]
            for key in keys:
                if data.get(key):
                    value = data[key]["display"]
                    if not self.address.get(name):
                        self.address[name] = {key: value}
                    break
            else:
                raise ValidationError(f"Address object: `{name}` does not have a valid `{str(keys)}` object applied.")

        def format_address_group(data, name):
            """Format address group objects, also adding the address objects as new ones are found."""
            address_group = []
            for address in data["address_objects"]:
                address = model_to_json(_get_instance_from_dict(address))
                if _check_status(address["status"]["name"]):
                    LOGGER.debug("Skipped due to status: `%s`", str(address["name"]))
                    continue
                format_address(address, address["name"])
                address_group.append(address["name"])
            if not self.address_group.get(name):
                self.address_group[name] = sorted(address_group)

        def format_service(data, name):
            """Format service objects."""
            ip_protocol = data["ip_protocol"]
            port = data.get("port")
            if not self.service.get(name):
                self.service[name] = {ip_protocol: port}
                self.service_protocol[name] = [ip_protocol]

        def format_service_group(data, name):
            """Format service group objects, also adding the address objects as new ones are found."""
            service_group = []
            service_group_protocols = []
            for service in data["service_objects"]:
                service = model_to_json(_get_instance_from_dict(service))
                if _check_status(service["status"]["name"]):
                    LOGGER.debug("Skipped due to status: `%s`", str(service["name"]))
                    continue
                format_service(service, service["name"])
                service_group.append(service["name"])
                service_group_protocols.append(service["ip_protocol"])

            # TODO: Do we need to verify if names object is the same and sanely error out? This goes for all types
            if not self.service_group.get("name"):
                self.service_group[name] = sorted(service_group)
                self.service_group_protocol[name] = service_group_protocols

        data = model_to_json(data)
        if _check_status(data["status"]["name"]):
            LOGGER.debug("Skipped due to status: `%s`", str(data))
            return None
        name = data["name"]
        type_mapper = {
            "address": format_address,
            "address-group": format_address_group,
            "service": format_service,
            "service-group": format_service_group,
        }

        type_mapper[_type](data, name)

        return name

    def validate_policy_data(self):  # pylint: disable=too-many-branches,too-many-statements
        """Helper method to get data in format required.

        This provides the general checking that should go against any firewall generation process, specifically
          * toggling obects based on status
          * checking if status toggle
          * normalizing format
          * de-duplicating data
          * Ordering list via sorted function
        """
        if not self.policy_details:
            raise ValidationError(
                "Must have set the self.policy_details attribute, which is an Policy.policy_details() object instance."
            )
        for rule in self.policy_details:
            if _check_status(rule["rule"].status.name):
                LOGGER.debug("Skipped due to status: `%s`", str(rule["rule"]))
                continue
            if rule["action"] == "remark" and PLUGIN_CFG["capirca_remark_pass"] is True:
                continue
            rule_src_addr = []
            rule_src_addr_group = []
            rule_src_svc = []
            rule_src_svc_group = []
            rule_dst_addr = []
            rule_dst_addr_group = []
            rule_dst_svc = []
            rule_dst_svc_group = []
            rule_protocol = []

            # Source
            for source_address in rule["source_addresses"]:
                rule_src_addr.append(self._format_data(source_address, "address"))
            for source_address_group in rule["source_address_groups"]:
                rule_src_addr_group.append(self._format_data(source_address_group, "address-group"))

            for service in rule["source_services"]:
                name = self._format_data(service, "service")
                rule_src_svc.append(name)
                # If service is empty, will get key error
                if name:
                    rule_protocol.append(self.service_protocol[name][0])

            for service_group in rule["source_service_groups"]:
                name = self._format_data(service_group, "service-group")
                rule_src_svc_group.append(name)
                # If service group is empty, will get key error
                if name:
                    rule_protocol.extend(self.service_group_protocol[name])

            # Destination
            for destination_address in rule["destination_addresses"]:
                rule_dst_addr.append(self._format_data(destination_address, "address"))
            for destination_address_group in rule["destination_address_groups"]:
                rule_dst_addr_group.append(self._format_data(destination_address_group, "address-group"))

            for service in rule["destination_services"]:
                name = self._format_data(service, "service")
                rule_dst_svc.append(name)
                # If service is empty, will get key error
                if name:
                    rule_protocol.append(self.service_protocol[name][0])

            for service_group in rule["destination_service_groups"]:
                name = self._format_data(service_group, "service-group")
                rule_dst_svc_group.append(name)
                # If service group is empty, will get key error
                if name:
                    rule_protocol.extend(self.service_group_protocol[name])

            rule_src_addr = _clean_list(rule_src_addr, True)
            rule_src_addr_group = _clean_list(rule_src_addr_group, True)
            rule_src_svc = _clean_list(rule_src_svc, True)
            rule_src_svc_group = _clean_list(rule_src_svc_group, True)

            rule_dst_addr = _clean_list(rule_dst_addr, True)
            rule_dst_addr_group = _clean_list(rule_dst_addr_group, True)
            rule_dst_svc = _clean_list(rule_dst_svc, True)
            rule_dst_svc_group = _clean_list(rule_dst_svc_group, True)
            rule_protocol = _clean_list(rule_protocol, True)

            # Check if a group consists of only object that are not active, if no make inactive as well.
            for name in rule_src_addr_group:
                for address in self.address_group[name]:
                    if self.address.get(address):
                        break
                else:
                    del self.address_group[name]
                    rule_src_addr_group.remove(name)

            for name in rule_src_svc_group:
                for service in self.service_group[name]:
                    if self.service.get(service):
                        break
                else:
                    del self.service_group[name]
                    rule_src_svc_group.remove(name)

            for name in rule_dst_addr_group:
                for address in self.address_group[name]:
                    if self.address.get(address):
                        break
                else:
                    del self.address_group[name]
                    rule_dst_addr_group.remove(name)

            for name in rule_dst_svc_group:
                for service in self.service_group[name]:
                    if self.service.get(service):
                        break
                else:
                    del self.service_group[name]
                    rule_dst_svc_group.remove(name)

            # This checks if an item existed on the source, but all source, destinations, or services
            # were remove, which would most likely happen when madde inactive
            self._check_for_empty(
                "source_addresses",
                rule["source_addresses"],
                rule["source_address_groups"],
                rule_src_addr,
                rule_src_addr_group,
            )
            self._check_for_empty(
                "source_services",
                rule["source_services"],
                rule["source_service_groups"],
                rule_src_svc,
                rule_src_svc_group,
            )

            self._check_for_empty(
                "destination_address",
                rule["destination_addresses"],
                rule["destination_address_groups"],
                rule_dst_addr,
                rule_dst_addr_group,
            )
            self._check_for_empty(
                "destination_services",
                rule["destination_services"],
                rule["destination_service_groups"],
                rule_dst_svc,
                rule_dst_svc_group,
            )

            rule_details = {
                "rule-name": rule["rule"].name,
                "source-address": rule_src_addr,
                "source-group-address": rule_src_addr_group,
                "source-service": rule_src_svc,
                "source-group-service": rule_src_svc_group,
                "from-zone": rule["source_zone"].name,
                "destination-address": rule_dst_addr,
                "destination-group-address": rule_dst_addr_group,
                "to-zone": rule["destination_zone"].name,
                "destination-service": rule_dst_svc,
                "destination-group-service": rule_dst_svc_group,
                "protocol": rule_protocol,
                "action": rule["action"],
                "logging": rule["log"],
                "request-id": rule["request_id"],
                "custom_field_data": rule["rule"].custom_field_data,
            }
            LOGGER.debug("Rule Details within iteration: `%s`", str(rule_details))

            self.policy.append(rule_details)
        if not self.policy:
            raise ValidationError(
                f"There was no valid policy rules found in {self.policy_name }, either the policy"
                " is empty or the status of all rules was not active."
            )

    def validate_capirca_data(self):  # pylint: disable=too-many-statements,too-many-branches
        """Helper method to get data in format required for Capirca.

        This provides the Capirca checking that should, specifically
          * Combine address|address group, service|service group objects
          * Lowercase the protocol
          * Nomalize port format
          * Check for non-usable IP address formats, fqdn/ip_range
          * Verifty action is one of the expected
          * Convert `ctd_` & `chd_` custom fields for inclusion as terms and headers
          * Normalize header info, such as zones or filter names
          * Case Sensitve slugify names
          * Convert request-id to a comment
          * Ordering list via sorted function
          * No destination port if not tcp/udp
          * Fail if mixing tcp/udp with with ports and protocols
        """
        if not self.policy:
            self.validate_policy_data()

        if not CAPIRCA_MAPPER.get(self.platform):
            raise ValidationError(
                f"The platform network driver {self.platform} was not one of the supported options {list(CAPIRCA_MAPPER.keys())}."
            )

        networkdata = {}
        for name, addresses in self.address.items():
            name = _slugify(name)
            if addresses.get("ip_range"):
                raise ValidationError(
                    f"The ip_range object `{addresses['ip_range']}` was attempted which is not supported by Capirca."
                )
            if addresses.get("fqdn"):
                raise ValidationError(
                    f"The fqdn object `{addresses['fqdn']}` was attempted which is not supported by Capirca."
                )
            if addresses.get("ip_address"):
                networkdata[name] = [addresses["ip_address"]]
            elif addresses.get("prefix"):
                networkdata[name] = [addresses["prefix"]]
            else:
                raise ValidationError(
                    f"Met a condition on {name} that should not happen, where address {addresses} was not an expected type of ip_address or prefix"
                )
        for name, addresses in self.address_group.items():
            name = _slugify(name)
            networkdata[name] = _clean_list(addresses, True)

        servicedata = {}
        servicedata_ports = {}
        for name, services in self.service.items():
            name = _slugify(name)
            port = list(services.values())[0]
            ip_protocol = list(services.keys())[0].lower()
            # May not have a port, if not, do not add
            if port:
                servicedata[name] = [f"{port}/{ip_protocol}"]
                servicedata_ports[name] = f"{port}/{ip_protocol}"
        for name, services in self.service_group.items():
            name = _slugify(name)
            services = _clean_list(services, True)
            # A service in Capirca is TCP/UDP, What if all child services
            # had not TCP/UDP Ports. Since servicedata is only populated if
            # in fact there is a port, procede if any of the child objects
            # have a port, otherwise pass
            if any(service in servicedata for service in services):
                servicedata[name] = services

        cap_policy = []
        for pol in self.policy:
            rule_name = _slugify(pol["rule-name"])
            if pol["action"] not in ACTION_MAP:
                raise ValidationError(
                    f"Rule: {rule_name}, the action `{pol['action']}` is not one of the support actions {str(ACTION_MAP.keys())} on rule."
                )
            protocols = _list_slugify([i.lower() for i in pol["protocol"]])

            _source_port = _list_slugify(pol["source-service"] + pol["source-group-service"])
            source_port_values = {}
            source_port = []
            for item in _source_port:
                if servicedata_ports.get(item):
                    source_port_values[item] = servicedata_ports[item]
                if servicedata.get(item):
                    source_port.append(item)

            _destination_port = _list_slugify(pol["destination-service"] + pol["destination-group-service"])
            destination_port_values = {}
            destination_port = []
            for item in _destination_port:
                if servicedata_ports.get(item):
                    destination_port_values[item] = servicedata_ports[item]
                if servicedata.get(item):
                    destination_port.append(item)

            rule_details = {"rule-name": rule_name, "headers": []}
            rule_details["terms"] = {
                "source-address": _list_slugify(pol["source-address"] + pol["source-group-address"]),
                "source-port": source_port,
                "destination-address": _list_slugify(pol["destination-address"] + pol["destination-group-address"]),
                "destination-port": destination_port,
                "protocol": protocols,
                "action": ACTION_MAP[pol["action"]],
                "logging": LOGGING_MAP[str(pol["logging"]).lower()],
                "comment": '"' + pol["request-id"] + '"',
            }
            if destination_port_values and not set(protocols).issubset(set(("tcp", "udp"))):
                raise ValidationError(
                    f"Rule: {rule_name}, {destination_port_values} destination port specified on rule that has non tcp or udp on it: {protocols}"
                )

            rule_details["headers"].append(self.platform)
            if CAPIRCA_MAPPER[self.platform]["type"] == "zone":
                from_zone = _slugify(pol["from-zone"])
                to_zone = _slugify(pol["to-zone"])
                rule_details["headers"].extend(["from-zone", from_zone, "to-zone", to_zone])
                LOGGER.debug("Zone Logic hit, from-zone: `%s` to-zone: `%s`", from_zone, to_zone)
            if CAPIRCA_MAPPER[self.platform]["type"] == "filter-name":
                rule_details["headers"].append(rule_details["rule-name"])
                LOGGER.debug("Filter Name Logic hit for: `%s`", str(rule_details["rule-name"]))

            for field, value in pol["custom_field_data"].items():
                is_ctd = field.startswith("ctd_")
                is_chd = field.startswith("chd_")
                is_allowed_disabled = self.cf_allow_list_enabled is False
                is_allowed = self.cf_allow_list_enabled and field in self.cf_allow_list
                field = field[4:]

                if is_ctd and (is_allowed_disabled or is_allowed):
                    rule_details["terms"][field] = value
                    LOGGER.debug("Updated ctd_ field `%s` to value: `%s`", str(field), str(value))
                if is_chd and (is_allowed_disabled or is_allowed):
                    rule_details["headers"].append(value)
                    LOGGER.debug("Updated chd_ field `%s` to value: `%s`", str(field), str(value))
            cap_policy.append(rule_details)

        return cap_policy, networkdata, servicedata

    @staticmethod
    def _get_capirca_files(cap_policy, networkdata, servicedata):  # pylint: disable=too-many-branches
        """Convert the data structures taken in by method to Capirca configs."""
        pol = []
        for index, rule in enumerate(cap_policy):
            LOGGER.debug("Index `%s` for rule `%s`", str(index), str(rule))

            pol.append("header {")
            pol.append("  target:: " + " ".join(rule["headers"]))
            pol.append("}")
            pol.append("")
            pol.append(f"term {rule['rule-name']}" + " {")

            for key, value in sorted(rule["terms"].items()):
                if not value:
                    continue
                if not isinstance(value, list):
                    value = [value]
                for item in sorted(value):
                    pol.append(f"  {key}:: {item}")
                    LOGGER.debug("Adding term key: `%s` value: `%s`", str(key), str(item))
            pol.append("}")
            pol.append("")

        networkcfg = []
        for name, addresses in sorted(networkdata.items()):
            for index, address in enumerate(sorted(addresses)):
                if index == 0:
                    networkcfg.append(f"{name} = {address}")
                else:
                    networkcfg.append(" " * (len(name) + 3) + address)

        servicecfg = []
        for name, services in sorted(servicedata.items()):
            for index, service in enumerate(sorted(services)):
                if index == 0:
                    servicecfg.append(f"{name} = {service}")
                else:
                    servicecfg.append(" " * (len(name) + 3) + service)
        return pol, networkcfg, servicecfg

    def get_capirca_cfg(self):
        """Generate Capirca formatted data structure, convert that into Capirca text config, run Capirca."""
        cap_policy, networkdata, servicedata = self.validate_capirca_data()
        pol, networkcfg, servicecfg = self._get_capirca_files(cap_policy, networkdata, servicedata)

        self.pol_file = "\n".join(pol)
        self.net_file = "\n".join(networkcfg)
        self.svc_file = "\n".join(servicecfg)

        self.cfg_file = generate_capirca_config(servicecfg, networkcfg, self.pol_file, self.platform)


class DevicePolicyToCapirca(PolicyToCapirca):
    """Class object to convert Policy orm object to Capirca object for a whole device."""

    def __init__(self, device_obj, **kwargs):  # pylint: disable=super-init-not-called
        """Overload init."""
        super().__init__(device_obj.platform.network_driver, **kwargs)
        self.policy_objs = []
        policy_name = []
        LOGGER.debug("Capirca Platform Name: `%s`", str(self.platform))
        LOGGER.debug("Original Platform Name: `%s`", str(device_obj.platform.network_driver))
        LOGGER.debug("cf_allow_list_enabled: `%s`", str(self.cf_allow_list_enabled))
        LOGGER.debug("cf_allow_list: `%s`", str(self.cf_allow_list))

        # TODO: Determine if this can be done with weight and more efficient
        for dynamic_group in device_obj.dynamic_groups.all():
            for policy_group in dynamic_group.policydynamicgroupm2m_set.all():
                self.policy_objs.append(policy_group.policy)
                policy_name.append(policy_group.policy.name)
        for policy_group in device_obj.policydevicem2m_set.all():
            if policy_group.policy.name not in policy_name:
                self.policy_objs.append(policy_group.policy)
                policy_name.append(policy_group.policy.name)

        self.policy_name = "__".join(policy_name)

    def get_all_capirca_cfg(self):
        """Aggregate off of the Capirca Configurations for a device."""
        for pol in self.policy_objs:
            if _check_status(pol.status.name):
                LOGGER.debug("Policy Skipped due to status: `%s`", str(pol))
                continue
            self.policy_details = pol.policy_details
            self.validate_policy_data()

        self.get_capirca_cfg()
