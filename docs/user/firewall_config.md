# Firewall Config

The Firewall Config data model and workflow relies on one of three types of integrations.

1. Aerleon
1. Capirca
1. Custom (roll your own)

The configuration generation was initially based on Capirca. Since then there has been limited updates and support for the package. In support of modernizing and standardizing the Nautobot Firewall configuration management strategy, the decision was made to leverage a generic data model and support multiple configuration generation engines, defaulting to Aerleon.

You can find out more information on the [Areleon](aerleon.md) and [Capirca](capirca.md) integrations in their respective documentation.

In addition, you can build a custom configuration engine. In order to do so, you would be responsible for that implementation. You can provide within your settings, a dotted path [import_string](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.module_loading.import_string) to your own function. This is provided in the `custom_firewall_config` setting within your Plugin Configurations. The signature takes a `Device` object instance and must return a tuple of `(pol, svc, net, cfg)`, none of which are required to have data.

```python
self.pol, self.svc, self.net, self.cfg = import_string(PLUGIN_CFG["custom_firewall_config"])(self.device)
```

!!! info
    The setting `custom_capirca` is deprecated and will be completely removed in 3.0.

## Default Driver

By default, the firewall configuration generation uses the `default_driver` specified in your plugin configuration. This setting determines which backend engine (such as Aerleon, Capirca, or custom) will be used to generate firewall configurations unless explicitly overridden on a specific object. 

To set the default driver, update your plugin configuration as follows:

```python
PLUGINS_CONFIG = {
    "nautobot_firewall_models": {
        "default_driver": "aerleon",  # "capirca" or "custom_firewall_config"
    }
}
```

If `default_driver` is not specified, the system will default to using Aerleon. You can override this behavior by providing the desired driver name. This setting is used in the migration process, so please ensure it matches your expectations.
