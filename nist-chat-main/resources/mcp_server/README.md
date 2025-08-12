# How to setup a local MCP Server

This guide shows how to:
- create a python environment using [uv](https://docs.astral.sh/uv/)
- create a MCP tool with [FastMCP](https://gofastmcp.com/getting-started/welcome)
- start a MCP server for Open WebUI with [mcpo](https://github.com/open-webui/mcpo)
- register and use tools in Open WebUI


**All commands need to be run from the folder `resources/mcp_server`**

## Setup a python environment

Download and install `uv`.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Python 3.10 for `uv`.
```shell
uv python install 3.10
```

Go into the `mcp_server` folder and create a virtual python environment, then activate it.
```shell
uv venv --python 3.10
source .venv/bin/activate
```

Install the required dependencies (`requirements.txt`) found in the `mcp_server` folder.
```shell
uv pip install -r requirements.txt
```

## Create your first MCP tool

Make sure the environment is properly setup by creating a simple MCP tool.
Open the file `hello.py` to see a simple MCP tool and client.
With your env activated, run the following command:

```shell
python hello.py
[TextContent(type='text', text='Hello, Rchat!', annotations=None)]
```

Source: [FastMCP - testing the server](https://gofastmcp.com/getting-started/quickstart#testing-the-server)

## Start a MCP server

The MCP servers available in the `mcp_server` folder can be used by most AI frameworks as/is via stdio.
However, Open WebUI (the frontend used by Rchat) is expecting the tools to be available via an OpenAPI-compatible HTTP server.
The following steps will show how to set up this server.

Source: [Open WebUI - MCP](https://docs.openwebui.com/openapi-servers/mcp/)


### Configure your MCP Server

The file `config.json` contains a list of MCP servers that will be made available for your local Open WevUI instance:
- `count.py`: python tool that counts the number of times a letter appears in a word
- `calculator.py`: python tool that provides basic mathematical and statistical operations

### Start the MCP server

From the `mcp_server` folder, with your python env activated, run the following command:
```shell
uvx mcpo --port 8081 --api-key "CHANGE_ME" --config ./config.json
```

**Notes:** 
- api-key should be a random string, this is **NOT your Rchat API KEY**,
- an api-key is provided in the `mcpo` documentation as an example and should be changed.

Source: [mcpo - quick usage](https://github.com/open-webui/mcpo?tab=readme-ov-file#-quick-usage)

### Check the available tools

Open your browser at the following address: http://localhost:8081/docs

Check that the two MCP servers appear and see the tools they provide by clicking on each link.

![mcpo_tools.png](images%2Fmcpo_tools.png){width=50%}

To try a tool, first authenticate using the same `api-key` that was used to start the server.

![mcpo_auth.png](images%2Fmcpo_auth.png){width=50%}

Use the swagger interface to try the tool, and see its output.

![mcpo_raspberry.png](images%2Fmcpo_raspberry.png){width=50%}


## Register the tools in your local Open WebUI

In a browser, go to your local Open WebUI instance, and add the tools in the admin dashboard.

![owui_admin_tools.png](images%2Fowui_admin_tools.png){width=50%}

Each MCP server from the `config.json` file needs to be added (2 in this case):

- Count
  - URL: http://localhost:8081/count
  - API KEY: the api-key set in the mcpo command
  - Name: Letter Count
- Calculator:
  - URL: http://localhost:8081/calculator
  - API KEY: the api-key set in the mcpo command
  - Name: Calculator

**Notes**:
- for docker deployments, use http://host.docker.internal:8081

## Chat with tools enabled

When starting a new chat, you should now see a list of available tools.
You can select, one or more tools that you think could help the LLM with its task.

![owui_tool_selection.png](images%2Fowui_tool_selection.png){width=50%}
 
Look at the terminal window to see if Open WebUI called a tool:

![mcpo_tool_call.png](images%2Fmcpo_tool_call.png){width=50%}

The result of the tool call is added to the context of the LLM that can then use it to answer your question:

![owui_response.png](images%2Fowui_response.png){width=50%}
