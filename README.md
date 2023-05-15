# DB Chatbot

DB Chatbot is a conversational agent designed to provide information and answer queries related to databases.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Maintenance](#maintenance)
- [Features](#features)

## Installation

To install and set up the DB Chatbot project, follow these steps:

1. Clone the repository:

   ```shell
   $ git clone https://github.com/ArjunChang/db_chatbot.git
   ```
2. Navigate to project folder
    ```shell
    cd db_chatbot
    ```
3. Install required dependencies
    ```shell
    pip install -r requirements.txt
    ```
4. In server.py update the API Key to a valid api key provided by openai.

## Usage
To use the DB Chatbot, follow these steps:
1. Start the chatbot
    ```shell
    python chatbot.py
    ```
2. Ask the bot any questions you want to. Limit the questions to those based on the database.

## Maintenance
To update or change the schema:
1. Open the rules.txt file
2. Update the schema here.
>**NOTE:** Changing any other rules might lead to a breakage of the chatbot.

## Features
DB Chatbot offers the following features:

- Natural language processing to understand user queries and prompts.
- Database-related information retrieval and responses.
- Multi-turn conversations for interactive and dynamic user interactions.
