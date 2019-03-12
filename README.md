# Azure DevOps Manager

Azdevman is a CLI tool that assists in managing resources within an Azure DevOps organization.

## Install

```bash
virtualenv -p python3 venv && pip install -e . && source ./venv/bin/activate
```

## Configure

For general use, the ```azdevman config create-context``` command is the fastest way to setup ```azdevman```.  When prompted, enter the Azure DevOps Organization, Personal Access Token (with appropriate permissions) and the Azure DevOps Project you would like to start working with.

```bash
$ azdevman config create-context
Azure Devops Organization: MyOrg
Personal Access Token: <personal access token>
Project: MyProject
```

This will store your configuration within ```~/.azdevman/config.json```.

Additionally, you can create multiple contexts by utilizing the ```--profile``` option in order to work between different Azure DevOps Organizations and Projects.

To view the current configuration, use the ```azdevman config get-context``` command.

## Usage

Azdevman is capable of managing a handful of resources within an Azure DevOps Organization and Project.  The current focus is to work with repositories, builds, build definitions, releases and release definitions.  This functionality will expand as more is added.

```string
Usage: azdevman [OPTIONS] COMMAND [ARGS]...

  Azure DevOps Manager

  Azdevman is a CLI tool that assists in managing resources within an Azure DevOps organization.

Options:
  -h, --help  Show this message and exit.
  --version   Show the version and exit.

Commands:
  compare  Compare similar Azure DevOps resources
  config   Configure azdevman local options
  create   Create Azure DevOps resources
  delete   Delete Azure DevOps resources
  get      Get Azure DevOps resources
  update   Update Azure DevOps resources
```

## Disclaimer

> Azdevman is currently in early stages of development and may have incomplete or broken functionality.  This cli tool was written to fill requirements I personally had while working with Azure DevOps.  If you are uncomfortable with what this tool may do, please test on a non critical DevOps Organization or Project.  Use at your own risk!
>
> THIS IS NOT A MIGRATION TOOL.
>
> For an official cli tool, please reference [Azure Devops CLI Extension](https://github.com/Microsoft/azure-devops-cli-extension).

## License

[MIT](LICENSE) © Keith Craley
