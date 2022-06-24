# Assigning Policies
There are three primary ways of assigning policies to devices:

* Directly via the `assigned_devices` attribute on the Policy object.
* Dynamically by assigning existing `DynamicGroup` object to the `assigned_dynamic_groups` on the Policy object.
    * At this time in Nautobot v1.3.X DynamicGroups can only be assigned to a Device objects or VirtualMachine objects.
* By creating a new `Relationship` specifying additional targets for Policy association. This can be, for example, used to associate Policy with an Interface object.
    * The use of a Relationship _may_ limit furture integrations with parsing or templating.

Although policies can be created without any rules it is recommended to create the required underlying objects first before moving to the Policy definitions. [Creation Order](./models.md#creation-order) provides an ordered list of steps for creating and assigning, objects, needed for Policy creation.



# Example
This example is using the same data that is loaded and used in unittesting of the plugin. To load the data for testing in a development environment `invoke testdata` will populate this information. If you are not using the local development environment you are still in luck. The invoke command is actually wrapping `nautobot-server create_test_firewall_data`. This management command is available to any environment that has this plugin installed and listed in `PLUGINS` in the `nautobot_config.py`.

## API
All firewall models are built with the use of both the REST API & GraphQL API available to the end user.

### GraphQL

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

### REST
When using the REST GET method to `/api/plugins/firewall/policy/<uuid>/` below is an example output.

#### Response
```json
{
  "id": "246a037f-9858-4848-90a5-7ca967a3583f",
  "tags": [],
  "display": "Policy 3",
  "policy_rules": [
    {
      "rule": "03182134-11a7-40a9-b433-169ab2df721b",
      "index": 10
    },
    {
      "rule": "f78c677d-feaa-41b2-90f8-a4e8c8a62791",
      "index": 20
    },
    {
      "rule": "b9aab2e9-5490-4dd7-b2b7-ca4c71247a10",
      "index": 30
    },
    {
      "rule": "3b92704a-9913-4f02-b499-f083d6a4912a",
      "index": 99
    },
    {
      "rule": "e10a4346-9d28-4b3f-b501-2ed8bd12a453",
      "index": 100
    }
  ],
  "assigned_devices": [],
  "assigned_dynamic_groups": [
    {
      "dynamic_group": "eaa19dba-bfe0-4072-a458-b47e1e1375e6",
      "weight": 1000
    }
  ],
  "created": "2022-06-09",
  "last_updated": "2022-06-09T01:35:14.230438Z",
  "_custom_field_data": {},
  "description": "",
  "name": "Policy 3",
  "status": "35206353-47f4-4e71-9e2c-807092b6c439",
  "tenant": "5fabe6c7-84a6-45af-95a0-384f9ebcbeb8"
}
```