# External Interactions

## Nautobot REST API endpoints

These examples are based on the same data used in unittesting of the plugin. To load the data for testing in a development environment use the `invoke testdata` command.

If you are not using the local development environment you are still in luck. The invoke command is actually wrapping `nautobot-server create_test_firewall_data`. This management command is available to any environment that has this plugin installed and listed in `PLUGINS` in the `nautobot_config.py`.

All firewall models are built with the use of both the REST API and GraphQL API available to the end user.

### GraphQL

Example GraphQL query showing how to get instances for each of the models provided by this plugin:

####  Query

```no-highlight
{
  policies {
    name
    assigned_devices {
      name
    }
    assigned_dynamic_groups {
      name
    }
    policy_rules {
      name
      request_id
      action
      log
      source_user {
        username
      }
      source_user_group {
        name
        user_objects {
          username
        }
      }
      source_zone {
        name
      }
      source_address {
        ip_address {
          address
        }
        ip_range {
          start_address
          end_address
        }
      }
      source_address_group {
        address_objects {
          ip_address {
            address
          }
          ip_range {
            start_address
            end_address
          }
        }
      }
      destination_zone {
        name
      }
      destination_address {
        ip_address {
          address
        }
        ip_range {
          start_address
          end_address
        }
      }
      destination_address_group {
        address_objects {
          ip_address {
            address
          }
          ip_range {
            start_address
            end_address
          }
        }
      }
    }
  }
}
```

#### Response

```json
{
  "data": {
    "policies": [
      {
        "name": "Policy 1",
        "assigned_devices": [
          {
            "name": "DFW-WAN00"
          },
          {
            "name": "HOU-WAN00"
          }
        ],
        "assigned_dynamic_groups": [],
        "policy_rules": [
          {
            "name": "Policy Rule 1",
            "request_id": "req1",
            "action": "DENY",
            "log": true,
            "source_user": [
              {
                "username": "user1"
              }
            ],
            "source_user_group": [
              {
                "name": "usr group1",
                "user_objects": [
                  {
                    "username": "user1"
                  }
                ]
              }
            ],
            "source_zone": null,
            "source_address": [
              {
                "ip_address": null,
                "ip_range": {
                  "start_address": "192.168.0.11",
                  "end_address": "192.168.0.20"
                }
              }
            ],
            "source_address_group": [
              {
                "address_objects": [
                  {
                    "ip_address": null,
                    "ip_range": {
                      "start_address": "192.168.0.11",
                      "end_address": "192.168.0.20"
                    }
                  },
                  {
                    "ip_address": {
                      "address": "10.0.0.1/32"
                    },
                    "ip_range": null
                  }
                ]
              }
            ],
            "destination_zone": null,
            "destination_address": [
              {
                "ip_address": null,
                "ip_range": null
              }
            ],
            "destination_address_group": [
              {
                "address_objects": [
                  {
                    "ip_address": null,
                    "ip_range": {
                      "start_address": "192.168.0.11",
                      "end_address": "192.168.0.20"
                    }
                  },
                  {
                    "ip_address": null,
                    "ip_range": null
                  },
                  {
                    "ip_address": null,
                    "ip_range": null
                  },
                  {
                    "ip_address": {
                      "address": "10.0.0.1/32"
                    },
                    "ip_range": null
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```
