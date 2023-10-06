# Nautobot Firewall Models

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/icon-nautobot-firewall-models.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-plugin-firewall-models/actions"><img src="https://github.com/nautobot/nautobot-plugin-firewall-models/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/firewall-models/en/latest"><img src="https://readthedocs.org/projects/nautobot-plugin-firewall-models/badge/"></a>
  <a href="https://pypi.org/project/nautobot-firewall-models/"><img src="https://img.shields.io/pypi/v/nautobot-firewall-models"></a>
  <a href="https://pypi.org/project/nautobot-firewall-models/"><img src="https://img.shields.io/pypi/dm/nautobot-firewall-models"></a>
  <br>
  An <a href="https://www.networktocode.com/nautobot/apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

A plugin for [Nautobot](https://github.com/nautobot/nautobot) that is meant to model layer 4 firewall policies and/or extended access control lists.

### Screenshots

More screenshots can be found in the [Using the App](https://docs.nautobot.com/projects/firewall-models/en/latest/user/app_use_cases/) page in the documentation. Here's a quick overview of some of the plugin's added functionality:

![Navigation Menu](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/navmenu.png "Navigation Menu")

![Policy View](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/policy.png "Policy View")


## Try it out!

This App is installed in the Nautobot Community Sandbox found over at [demo.nautobot.com](https://demo.nautobot.com/)!

> For a full list of all the available always-on sandbox environments, head over to the main page on [networktocode.com](https://www.networktocode.com/nautobot/sandbox-environments/).

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/firewall-models/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/firewall-models/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/firewall-models/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/firewall-models/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/firewall-models/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/nautobot/nautobot-plugin-firewall-models/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/firewall-models/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/firewall-models/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
