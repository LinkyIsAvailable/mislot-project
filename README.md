# mislot-project

*The project is based in french. If you want to use it on your language, you'll have to edit it by yourself.*
*Same for prompts used in the main code.*

# Mission Locale Search Assistant

This project is an intelligent search assistant designed specifically for Missions Locales in France. It uses the Mistral AI API for query analysis and the Tavily API for relevant information retrieval.

## Features

- Intelligent analysis of user queries in French
- Search for information in specific fields:
  - Housing
  - Employment
  - Education
  - Healthcare
  - Mobility
- Automatic extraction of relevant keywords
- Structured presentation of results with links and descriptions

## Prerequisites

- Python 3.11
- API keys :
  - Mistral AI API
  - Tavily API

## Installation

1. Install the required dependencies:
```bash
pip install requests tavily-python
```

2. Configure your API keys in the main file

## Usage

1. Run the main script:
```bash
python mislot-offres.py
```

2. Enter your search when prompted
3. The program will analyze your query and return relevant results.
4. To quit the program, press 'cancel'.

## How it works

1. The user enters a query in French
2. System uses Mistral AI to extract relevant keywords
3. These keywords are used to search via the Tavily API
4. The results are formatted and presented to the user with :
   - Article/page titles
   - Description
   - Links to sources


## Limitations

- Searches are limited to the specific fields of Missions Locales
- Results are only in French and concern France (you can edit in the code)
- Maximum 5 results per search

## Contribution

Please feel free to contribute to this project by submitting pull requests or reporting problems in the Issues section.
