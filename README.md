# Mythril MCP Server

This project implements a Model Context Protocol (MCP) server that exposes tools for using Mythril, a security analysis tool for Ethereum smart contracts.

## Description

Mythril MCP Server provides an interface to run Mythril security analysis tools via the Model Context Protocol (MCP). This makes it easy to integrate Mythril's smart contract security analysis capabilities with AI models and other applications that support MCP.

## Features

- Analyze Solidity smart contract files
- Analyze on-chain contracts by address
- Advanced analysis with customizable options
- Access to Mythril usage documentation as a resource

## Requirements

- Python 3.12+
- Mythril installed and accessible in PATH
- Solc compiler (for analyzing Solidity files)

## Installation

1. Clone this repository
2. Install dependencies with `pip install -e .` or `pip install mcp[cli]>=1.6.0`
3. Install Mythril with `pip install mythril`

## Usage

### Starting the Server

Run the server using the MCP CLI:

```bash
mcp dev server.py
```

Or directly:

```bash
python server.py
```

### Available Tools

1. **analyze_solidity_file** - Analyze a local Solidity file
2. **analyze_contract_address** - Analyze a contract deployed on-chain
3. **analyze_with_options** - Advanced analysis with custom options

### Available Resources

- **resource://mythril/usage** - Documentation about Mythril usage

## Example Client Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python", args=["server.py"])
async with stdio_client(params) as (r, w):
    async with ClientSession(r, w) as session:
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {tools}")
        
        # Analyze a Solidity file
        result = await session.call_tool(
            "analyze_solidity_file", 
            arguments={"file_path": "path/to/contract.sol", "output_format": "text"}
        )
        print(result)
```