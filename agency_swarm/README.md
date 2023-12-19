# Agency Swarm Documentation

## Introduction

This directory contains the core modules and components of the Agency Swarm system. Its purpose is to provide a robust framework for creating and managing a swarm of agent-based workflows.

## Directory Structure and Purpose

- `__init__.py`: The initializer script for the module.
- `__pycache__`: A directory containing compiled Python files for faster loading.
- `agency`: Contains core logic for agency operations.
- `agents`: Houses the definitions for different agent roles in the system.
- `cli.py`: The command-line interface for interacting with the system.
- `messages`: Manages inter-agent communication.
- `threads`: Handles multithreading tasks.
- `tools`: Consists of utility functions and helpers.
- `user`: Manages user-related components.
- `util`: General utility scripts.

## File and Directory Roles

Each file and directory has a specific role within the Agency Swarm system. The `agents` directory, for example, contains the definitions for different agent roles and their responsibilities. Understanding each component's role is crucial for navigating and utilizing the system effectively.

### Core Files and Directories:

- `agency`: Implements the operational logic of the system.
- `agents`: Defines roles and capabilities of the agents within the system.

### `agency/__init__.py`

Initializes the `agency` module and its components.

### `agency/agency.py`

Contains the `Agency` class which is the main entry point for creating and managing the agency's structure, including agents, threads, and communication tools. The class provides several methods:

- `__init__`: Sets up the agency, initializes components, and prepares for user interactions.
- `get_completion`: Retrieves completion for messages from the main thread, optionally yielding intermediate messages.
- `run_demo`: Runs a demonstration of the agency's capabilities in a command-line interface.
- `_parse_agency_chart`: Initializes and organizes agents based on an agency chart.
- `_add_agent`: Adds an agent to the agency's list with unique identification.
- `get_agent_by_name`: Looks up an agent by its name within the agency.
- `get_agents_by_names`: Retrieves a list of agents by their names.
- `get_agent_ids`: Obtains ids of all agents in the agency.
- `get_agent_names`: Gets names of all agents in the agency.
### `agents/__init__.py`

Initializes the `agents` module and its components.

### `agents/agent.py`

Contains the `Agent` class which represents individual agents with specialized functions within the agency. The class provides methods for initialization, OpenAI assistant handling, file handling, and settings management:

- `__init__`: Initializes an agent with attributes and tools.
- `init_oai`: Initializes the OpenAI assistant for the agent.
- `add_tool`: Adds a tool to the agent's repertoire.
- `add_instructions`: Adds shared instructions to the agent.
- `set_params`: Sets or updates parameters for the agent.
- `delete_assistant`: Deletes the assistant and its settings from OpenAI server.
- `get_class_folder_path`: Retrieves the absolute path of the class's directory.
- `get_oai_tools`: Converts the list of tools to OpenAI format.
### `messages/__init__.py`

Initializes the `messages` module for handling message output and formatting within the agency.

### `messages/message_output.py`

Contains the `MessageOutput` class which is used to format and print messages to the console with specific styles and emojis, creating a clear visual representation of the message flow. The class includes the following methods:

- `__init__`: Initializes a message with a specified type, sender, receiver, and content.
- `cprint`: Prints the message to console with formatting based on the message type.
- `get_formatted_header`: Formats the header of the message to include relevant emojis and names.
- `get_formatted_content`: Combines the formatted header and message content.
- `get_sender_emoji`: Generates an emoji representation for the message sender based on a hash of the sender name.


### `threads/__init__.py`

Sets up the `threads` module, which handles parallel processing and asynchronous connections within the agency framework.

### `threads/thread.py`

Contains the `Thread` class for managing individual threads of communication between an agent and user or between agents. This class is essential for handling dialogue and processing tool outputs. Key methods include:

- `__init__`: Initializes a thread with a designated agent and recipient agent.
- `get_completion`: Processes messages and tool calls within the thread, returning responses and outputs.
- `_execute_tool`: Executes a tool call and processes the output within the thread.




### `tools/__init__.py`

Initializes the `tools` module, including the base classes for extending functionality through various specialized tools.

### `tools/base_tool.py`

Defines the abstract `BaseTool` class that all tools used by agents derive from. The class incorporates an OpenAI schema and an abstract method `run` which must be implemented by any subclass to perform specific actions or calculations:

- `__init__`: Instantiates a tool, setting up any required configurations.
- `run`: Abstract method intended to be implemented by subclasses to define the tool's operational logic.


- `_read_instructions`: Loads shared instructions for agents from a file.
### `tools/tool_factory.py`

Implements the `ToolFactory` class, providing static methods for creating tool classes dynamically based on different schemas or sets of functions. It can convert langchain tools or standard tool definitions from OpenAI schema into operational tools within the agency. It supports the following factory methods:

- `from_langchain_tools`: Converts a list of langchain tools into BaseTool instances.
- `from_langchain_tool`: Converts a single langchain tool into a BaseTool instance.
- `from_openai_schema`: Creates BaseTool instances from an OpenAI function schema with a specified callback.


- `_create_send_message_tools`: Sets up messaging tools for each agent to communicate within the structure.
- `_create_send_message_tool`: Generates a messaging tool for an agent, allowing communication with specified recipients.
- `get_recipient_names`: Retrieves names of recipients the agent can communicate with.
- `_init_agents`: Initializes agents with shared instructions and models.
### `user/__init__.py`

Initializes the `user` module for managing user-related components and interactions with the agency system.

### `user/user.py`

Defines the `User` class which represents the end-user interacting with the agency system. This class is primarily a placeholder for future extensions where more personalized user attributes and functionalities may be added:

- `__init__`: Constructs a user instance optionally with a specified name.


### `util/__init__.py`

Provides initialization for the `util` module which contains various utility scripts and helper functions for the agency.

### `util/create_agent_template.py`

Features a script to generate a directory structure template for a new agent within the agency. It creates necessary files like the agent script, instructions, tools, and file storage directory:

- `create_agent_template`: Generates a directory with the agent class, init file, instructions, tools, and files folder.

### `util/logging.py`

Provides a customized logging utility for the agency, including log file handling and console output formatting with color schemes for different log levels:

- `getLogger`: Retrieves the logger instance for a specific module or the default agency logger.
- `ConsoleFormatter`: A custom formatter class to add color to log level names in console output.

### `util/oai.py`

Contains utility functions to manage OpenAI client instances, ensuring the proper configuration and access for operational tasks within the agency:

- `get_openai_client`: Retrieves or initializes the OpenAI client object.
- `set_openai_key`: Sets the API key for the OpenAI client.

### `util/schema.py`

Offers functions to handle JSON schema references, enabling the conversion between dereferenced schemas and schemas with extracted definitions into distinct `$defs` sections:

- `dereference_schema`: Dereferences `$ref` within a JSON schema, resolving into full definitions.
- `reference_schema`: Processes a JSON schema, extracting nested definitions into a `$defs` section.



- `_init_threads`: Sets up threads for agent communication.
- `get_class_folder_path`: Finds the path of the class file directory.


### Utilities and Helpers:

- `cli.py`: Entry point for command-line operations.
- `tools`: A collection of useful tools to enhance the functionality.

### Communication and Multithreading:

- `messages`: Handles the message-passing between agents.
- `threads`: Provides threading mechanisms to enable concurrent operations.

## Usage Examples

To be populated with concrete examples illustrating the use of key components.

## API Documentation

To be populated with API signatures and descriptions of public methods from the `.py` files within the directory.

## Testing Documentation

The documentation will undergo several tests for readability, navigation, accuracy, and completeness to ensure that it efficiently serves its intended purpose.

