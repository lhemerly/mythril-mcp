from mcp.server.fastmcp import FastMCP, Context
import subprocess
import asyncio
import os
import json
from typing import List, Dict, Optional, Union, Any

# Initialize the MCP server
mcp = FastMCP("MythrilMCP", dependencies=["mcp[cli]>=1.6.0"])

@mcp.tool()
async def analyze_solidity_file(file_path: str, output_format: str = "text", ctx: Context = None) -> str:
    """
    Analyze a Solidity smart contract file using Mythril.
    
    Args:
        file_path: Path to the Solidity file
        output_format: Output format (text, markdown, json, jsonv2)
    
    Returns:
        Analysis results as a string
    """
    if ctx:
        await ctx.report_progress(1, 3)
        await ctx.info(f"Analyzing Solidity file: {file_path}")
    
    cmd = ["myth", "analyze", file_path, "-o", output_format]
    
    if ctx:
        await ctx.report_progress(2, 3)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Error analyzing file: {e.stderr}"
    
    if ctx:
        await ctx.report_progress(3, 3)
    
    return output

@mcp.tool()
async def analyze_contract_address(
    address: str, 
    network: str = "mainnet", 
    output_format: str = "text",
    infura_id: Optional[str] = None,
    ctx: Context = None
) -> str:
    """
    Analyze an on-chain smart contract using Mythril.
    
    Args:
        address: Contract address to analyze
        network: Network name (mainnet, rinkeby, kovan, ropsten)
        output_format: Output format (text, markdown, json, jsonv2)
        infura_id: Infura ID for API access (optional)
    
    Returns:
        Analysis results as a string
    """
    if ctx:
        await ctx.report_progress(1, 3)
        await ctx.info(f"Analyzing contract at address: {address} on {network}")
    
    cmd = ["myth", "analyze", "-a", address, "-o", output_format]
    
    # Set up RPC connection
    if network != "ganache":
        if infura_id:
            cmd.extend(["--rpc", f"infura-{network}", "--infura-id", infura_id])
        else:
            # Try to use environment variable or config
            cmd.extend(["--rpc", f"infura-{network}"])
    else:
        cmd.extend(["--rpc", "ganache"])
    
    if ctx:
        await ctx.report_progress(2, 3)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Error analyzing contract: {e.stderr}"
    
    if ctx:
        await ctx.report_progress(3, 3)
    
    return output

@mcp.tool()
async def analyze_with_options(
    target: str,
    is_address: bool = False,
    contract_name: Optional[str] = None,
    execution_timeout: int = 60,
    max_depth: int = 22,
    solc_version: Optional[str] = None,
    output_format: str = "text",
    network: str = "mainnet",
    infura_id: Optional[str] = None,
    ctx: Context = None
) -> str:
    """
    Analyze a smart contract with advanced options using Mythril.
    
    Args:
        target: File path or contract address
        is_address: Whether the target is an address (True) or a file (False)
        contract_name: Specify contract name if file has multiple contracts
        execution_timeout: Execution timeout in seconds
        max_depth: Maximum recursion depth
        solc_version: Solidity compiler version
        output_format: Output format (text, markdown, json, jsonv2)
        network: Network name for on-chain analysis
        infura_id: Infura ID for API access
    
    Returns:
        Analysis results as a string
    """
    if ctx:
        await ctx.report_progress(1, 4)
        if is_address:
            await ctx.info(f"Analyzing contract at address: {target}")
        else:
            await ctx.info(f"Analyzing file: {target}")
    
    cmd = ["myth", "analyze"]
    
    if is_address:
        cmd.extend(["-a", target])
        # Set up RPC connection
        if network != "ganache":
            if infura_id:
                cmd.extend(["--rpc", f"infura-{network}", "--infura-id", infura_id])
            else:
                # Try to use environment variable or config
                cmd.extend(["--rpc", f"infura-{network}"])
        else:
            cmd.extend(["--rpc", "ganache"])
    else:
        cmd.append(target)
        if contract_name:
            cmd[-1] = f"{target}:{contract_name}"
    
    if ctx:
        await ctx.report_progress(2, 4)
    
    # Add additional options
    cmd.extend(["-o", output_format])
    cmd.extend(["--execution-timeout", str(execution_timeout)])
    cmd.extend(["--max-depth", str(max_depth)])
    
    if solc_version:
        cmd.extend(["--solv", solc_version])
    
    if ctx:
        await ctx.report_progress(3, 4)
        await ctx.info(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Error during analysis: {e.stderr}"
    
    if ctx:
        await ctx.report_progress(4, 4)
    
    return output

@mcp.resource("resource://mythril/usage")
def mythril_usage() -> str:
    """
    Return information about Mythril usage.
    """
    try:
        with open("LLM/mythril-usage.md", "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Mythril usage documentation not found."

@mcp.prompt()
def analyze_prompt(contract_file: str) -> str:
    return f"""
    I'm going to analyze the smart contract file {contract_file} for security vulnerabilities.
    I'll use Mythril, which is a security analysis tool for EVM bytecode.
    This will check for common issues like reentrancy, integer overflow/underflow, and other vulnerabilities.
    """

def main():
    print("Starting Mythril MCP server...")
    mcp.run()

if __name__ == "__main__":
    main()
