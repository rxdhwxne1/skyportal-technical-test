# SkyPortal Daily Digest Summarizer (Technical-test)

## Project Overview

The SkyPortal Daily Digest Summarizer is a tool designed to generate daily summaries of actions taken on astronomical objects saved to the "Redshift Completeness Factor" group. This project aims to provide astronomers with a concise and formal summary of the actions performed on these objects, including relevant comments and classifications. The summaries are generated using the Ollama language model and displayed through an interactive Streamlit interface.

## Project Context

Astronomers capture a plethora of transient phenomena, such as stars devouring their partners, objects captured by supermassive black holes, dying stars, or even collisions of dead stars. Among these, some high-energy phenomena can illuminate the sky for as short as a few hours, up to days. These rare and short-lived events are of immense value to various scientific fields, such as the origin of heavy elements found on Earth or the origin of Dark Energy.

To coordinate the efforts of ground and space-based facilities, the SkyPortal web application is used by US and EU scientific collaborations. This coordination is enabled by a web application named SkyPortal, which processes alerts from the ZTF (Zwicky Transient Facility) and other surveys in real-time.

## Objective

The objective of this project is to automate the generation of daily digest summaries for the "Redshift Completeness Factor" group. These summaries should include relevant information about the actions performed on each astronomical object, such as important comments and whether a spectrum was taken by an instrument. The summaries should be concise, formal, and suitable for an audience of experienced astronomers.

## Features

- Data Filtering: Filters objects saved on a specific date (16/05/2021) from a JSON file.
- Data Cleaning: Extracts relevant information from the filtered objects, including the most recent redshift value, classifications, and comments.
- Prompt Generation: Creates a prompt for the Ollama model to generate a summary.
- Summary Generation: Uses the Ollama model to generate a summary based on the prompt.
- Interactive Interface: Provides an interactive Streamlit interface to generate summaries of the cleaned data and display summaries for selected objects.

## Installation

Step 1. Clone the Repository:
```bash
git clone git@github.com:rxdhwxne1/skyportal-technical-test.git
cd skyportal-technical-test
```

Step 2. Create a virtual environment (mandatory):

```bash
python -m venv env
source env/bin/activate  # For macOS/Linux
.\env\Scripts\activate   # For Windows
```

Step 3. Install dependencies:

```bash
pip install -r requirements.txt
```

Step 4. Install and Configure Ollama: 

The project uses Ollama to manage the Llama 3.2 language model.
- Download and install Ollama from [ollama.com](https://ollama.com).
- Run the Llama 3.2 model locally:

```bash
ollama run llama3.2
```

Step 5. Run the Streamlit App:
```bash
streamlit run project.py
```

## Usage

1. Load Data: The application loads data from a JSON file (rcf_sample_sources.json).
2. Filter and Clean Data: The application filters objects saved on 16/05/2021 and cleans the data to extract relevant information.
3. Select Object: Use the Streamlit interface to select the index of the object you want to summarize.
4. Generate Summary: Click the "Validate" button to generate and display the summary for the selected object.
5. Display Summary: Choose one specific summary to display or display all summaries.

## Code Structure

- project.py: The main script that contains the data filtering, cleaning, prompt generation, summary generation, and Streamlit interface.
- rcf_sample_sources.json: The JSON file containing the sample data.
- requirements.txt: The file listing the project dependencies.

## Dependencies

- streamlit: For creating the interactive web interface.
- ollama: For generating summaries using the Ollama model.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
