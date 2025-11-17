# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The app is compatible with Nautobot 2.4.20 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

## Install Guide

!!! note
    Apps can be installed from the [Python Package Index](https://pypi.org/) or locally. See the [Nautobot documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/app-install/) for more details. The pip package name for this app is [`nautobot-firewall-models`](https://pypi.org/project/nautobot-firewall-models/).

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-firewall-models
```

To ensure Nautobot Firewall Models is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-firewall-models` package:

```shell
echo nautobot-firewall-models >> local_requirements.txt
```

Once installed, the app needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

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

Models provided by this plugin have a `status` attribute and the default `status` is set to use `Active`. This corresponds to the pre-built Nautobot `Active` Status object.

The app behavior can be controlled with the following list of settings:

Use the `default_status` plugin configuration setting to change the default value for the `status` attribute.

```python
PLUGINS_CONFIG = {
    "nautobot_firewall_models": {
        "default_status": "Active",
        "allowed_status": ["Active"], # default shown, `[]` allows all
        "default_driver": "aerleon",  # Options are 'aerleon', 'capirca', or 'custom_firewall_config'
        "capirca_remark_pass": True,
        "capirca_os_map": {           # Note: currently deprecated
            "cisco_ios": "cisco",
            "arista_eos": "arista",
        },
        "aerleon_remark_pass": True,
        # "custom_firewall_config": "my.custom.func", # provides ability to create a custom configuration engine
    }
}
```

The value assigned to `default_status` must match the name of an existing Nautobot Status object. That Status object must have all of the Firewall Models listed in the Content Type associations. See examples below on selecting the Content Type(s) when creating/editing a Status object and the pre-built `Active` Status with firewall content types added.

> Note: In Nautobot v1.x, the `default_status` must match the slug on an existing Nautobot Status object, not the name. Nautobot v2 moved away from using slugs entirely, instead using the name as an identifier.

![Custom Status](../images/custom-status.png "Custom Status")

![Existing Status](../images/existing-status.png "Existing Status")
