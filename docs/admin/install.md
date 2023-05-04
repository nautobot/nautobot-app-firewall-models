# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The plugin is compatible with Nautobot 1.4.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

## Install Guide

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this plugin is [`nautobot-firewall-models`](https://pypi.org/project/nautobot-firewall-models/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-firewall-models
```

To ensure Nautobot Plugin Firewall Model is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-firewall-models` package:

```shell
echo nautobot-firewall-models >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_firewall_models"` to the `PLUGINS` list.
- Append the `"nautobot_firewall_models"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_firewall_models"]

# PLUGINS_CONFIG = {
#   "nautobot_firewall_models": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

Models provided by this plugin have a `status` attribute and the default `status` is set to use `active`. This corresponds to the pre-built Nautobot `Active` Status object.

Use the `default_status` plugin configuration setting to change the default value for the `status` attribute.

```python
PLUGINS_CONFIG = {
    "nautobot_firewall_models": {
        "default_status": "active"
        "allowed_status": ["active"], # default shown, `[]` allows all
        "capirca_remark_pass": True,
        "capirca_os_map": {
            "cisco_ios": "cisco",
            "arista_eos": "arista",
        },
        # "custom_capirca": "my.custom.func", # provides ability to overide capirca logic
    }
}
```

The value assigned to `default_status` must match the slug of an existing Nautobot Status object. That Status object must have all of the Firewall Models listed in the Content Type associations. See examples below on selecting the Content Type(s) when creating/editing a Status object and the pre-built `Active` Status with firewall content types added.

![Custom Status](../images/custom-status.png "Custom Status")

![Existing Status](../images/existing-status.png "Existing Status")
