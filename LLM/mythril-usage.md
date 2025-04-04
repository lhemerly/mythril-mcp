Security Analysis
Run myth analyze with one of the input options described below will run the analysis modules in the /analysis/modules directory.

Analyzing Solidity Code
In order to work with Solidity source code files, the solc command line compiler needs to be installed and in PATH. You can then provide the source file(s) as positional arguments.

$ myth analyze ether_send.sol
==== Unprotected Ether Withdrawal ====
SWC ID: 105
Severity: High
Contract: Crowdfunding
Function name: withdrawfunds()
PC address: 730
Estimated Gas Usage: 1132 - 1743
Anyone can withdraw ETH from the contract account.
Arbitrary senders other than the contract creator can withdraw ETH from the contract account without previously having sent an equivalent amount of ETH to it. This is likely to be a vulnerability.
--------------------
In file: tests/testdata/input_contracts/ether_send.sol:21

msg.sender.transfer(address(this).balance)

--------------------
If an input file contains multiple contract definitions, Mythril analyzes the last bytecode output produced by solc. You can override this by specifying the contract name explicitly:

myth analyze OmiseGo.sol:OMGToken
Specifying Solc Versions
You can specify a version of the solidity compiler to be used with --solv <version number>. Please be aware that this uses py-solc and will only work on Linux and macOS. It will check the version of solc in your path, and if this is not what is specified, it will download binaries on Linux or try to compile from source on macOS.

Output Formats
By default, analysis results are printed to the terminal in text format. You can change the output format with the -o argument:

myth analyze underflow.sol -o jsonv2
Available formats are text, markdown, json, and jsonv2. For integration with other tools, jsonv2 is generally preferred over json because it is consistent with other MythX tools.

Analyzing On-Chain Contracts
When analyzing contracts on the blockchain, Mythril will by default attempt to query INFURA. You can use the built-in INFURA support or manually configure the RPC settings with the --rpc argument.

--rpc ganache	Connect to local Ganache
--rpc infura-[netname] --infura-id <ID>	Connect to mainnet, rinkeby, kovan, or ropsten.
--rpc host:port	Connect to custom rpc
--rpctls <True/False>	RPC connection over TLS (default: False)
To specify a contract address, use -a <address>

Analyze mainnet contract via INFURA:

myth analyze -a 0x5c436ff914c458983414019195e0f4ecbef9e6dd --infura-id <ID>
You can also use the environment variable INFURA_ID instead of the cmd line argument or set it in ~/.mythril/config.ini.

myth -v4 analyze -a 0xEbFD99838cb0c132016B9E117563CB41f2B02264 --infura-id <ID>
Speed vs. Coverage
The execution timeout can be specified with the --execution-timeout <seconds> argument. When the timeout is reached, mythril will stop analysis and print out all currently found issues.

The maximum recursion depth for the symbolic execution engine can be controlled with the --max-depth argument. The default value is 22. Lowering this value will decrease the number of explored states and analysis time, while increasing this number will increase the number of explored states and increase analysis time. For some contracts, it helps to fine tune this number to get the best analysis results. -