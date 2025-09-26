# Aerleon Integration

The firewall model plugin provides the ability to integrate with Aerleon for configuration generation. The authors have applied a very light opinion onto the translation from the firewall models to generate valid policy (`.pol`), network (`.net`), and service (`.svc`) files that are consumed by Aerleon.

FW Model                    | Aerleon
--------------------------- | -------
Name (as applicable)        | Header - Filter Name
Zone (as applicable)        | Header - to-zone/from-zone
Source Address / Group      | Term - source-address
Destination Address / Group | Term - destination-address
Destination Service / Group | Term - destination-port, protocol
Action                      | Term - action
Logging                     | Term - logging
Address - IP                | *.net
Address - Prefix            | *.net
Address Group               | *.net
Service - tcp/udp           | *.svc
Service Group               | *.svc

!!! note
    If this terminology is not familiar, please review the documentation at [Aerleon](https://github.com/aerleon/aerleon).

## Special Considerations

* Aerleon does not allow special characters in a majority of the named objects, as such named objects are modified to the ouput used when processed via a modified (to allow for capital letters) [Django slugify](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify), this includes:
    * Policy name, policy rule name, address, address group, zone, service, service group
    * e.g. Policy called "Allow to Internet" will be called "Allow-to-Internet"
    * Note: This **will not change** barring a major update from Aerleon
* FQDN and IP Range are not supported by Aerleon and will fail if attempting to use those features
* The zone is only used where Aerleon supports it, at the time of this writing is only Palo Alto and Juniper SRX
    * Zone based firewalls have headers on every rule
    * Both Juniper SRX and Palo Alto support using the named zone "all" to represent all zones, but in all cases a zone must be set
* The "Filter Name" is a concatenation of the Policies applied to a given firewall
    * Not all firewalls get a filter name, such as zone or direction based firewalls, which require a `chd_` custom field (more details below)
* An object (policy, policy rule, src-addr, dst-addr, etc.) is put into and out of use based on whether or not the status is `active` or as defined in your plugin configuration
    * Anything other than active or defined in plugin setting `allowed_status` is ignored
* Removing the last active object in an source-address, destination-address, or service will fail the process to avoid your policy failing open
* The Platform `network_driver` must match the Aerleon generator name
    * You can optionally provide a mapping in the settings `aerleon_os_map` to map from the current platform name, to the Aerleon generator name
* The action of "remark" on a rule is not conidered, you can set the setting `aerleon_remark_pass=False` if you want it to fail by default rather than silently skipping

In addition to the above, you can add to any header or term by creating specific custom fields on the `PolicyRule` data model. They must start with:

* `chd_` - Aerleon Header Data - will be applied to the `header` for any given rule (`chd_` name comes from previous versions of this app using Capirca, kept for compatibility).
* `ctd_` - Aerleon Term Data - will be applied to the `term` for any given rule (same comment than before).

The process is to create a custom field, such as `ctd_pan-application`, this will be applied to the PolicyRule as you describe. This can become problematic if you share the model for multiple firewall OSs. This can be conditionally applied via a custom field to the `Platform` model. This custom field **must** be named `aerleon_allow` and be of type JSON and be a single list. For each OS defined by the platform, you can allow that custom field to populate. This allows you to use the same model, and not let the custom fields for one OS conflict with another OS.

```python
aerleon_allow = ['ctd_pan-application', 'ctd_expiration']
```

> Note: This is pseudo-code and is technically the custom_field called `aerleon_allow` that has the data `["ctd_pan-application", "ctd_expiration"]` in this example.

As previously mentioned, there is only a small opinion that is applied from the translation between the model and Aerleon. That being said, Aerleon has an opinion on how rules and objects are deployed, and within this project there is no consideration for how that may not align with anyone's intention on how Aerleon should work. All such considerations should be referred to the Aerleon project. There is no intention to modify the output that Aerleon creates **in any situation** within this plugin.

That being said, in an effort to provide flexibility, you can override the translation process. However, you would be responsible for that implementation. You can provide within your setting, a dotted path [import_string](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.module_loading.import_string) to your own function. This is provided in the `custom_aerleon` setting within your Plugin Configurations. The signature takes a `Device` object instance and must return a tuple of `(pol, svc, net, cfg)`, none of which are required to have data.

```python
self.pol, self.svc, self.net, self.cfg = import_string(PLUGIN_CFG["custom_aerleon"])(self.device)
```

## Summary

To summarize, what this integration provides and does not provide.

### Provides

* Integrations with Aerleon
* The ability to manage per platform Headers and Terms
* A Job that generated the configurations at the time you want
* The ability to override the opinionated Aerleon solution

### Does not Provide

* An opinionated configuration management solution that matches anything other than Aerleon-provided configurations
* The ability to push configurations directly and natively from Nautobot
* The immediate updating from data in a `Policy` or `PolicyRule` that gets reflected in the configuration, instead when the job is ran
* Any post processing of configuration or pre-validation of data (such as checking if object name starts with an integer)
