# 🧠 LLM-Powered CSV Editor

A Streamlit application that uses Azure OpenAI to intelligently edit CSV files through natural language commands.

## Features

- Upload CSV files and view them in a clean interface
- Use natural language to modify your data (e.g., "Add a column with all 1s", "Change value in row 2 column B to 100")
- Preview generated Python code before execution
- Download modified CSV files
- Powered by Azure OpenAI for intelligent code generation

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd smart-csv-editor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Azure OpenAI credentials:
   ```env
   AZURE_DEPLOYMENT_NAME=your-deployment-name
   AZURE_API_KEY=your-api-key-here
   AZURE_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_API_VERSION=2023-05-15
   AZURE_MODEL_NAME=gpt-35-turbo
   ```

### 4. Run the application
```bash
streamlit run app.py
```

## Usage

1. **Upload a CSV file** using the file uploader
2. **Enter a natural language command** describing what you want to do with the data
3. **Click "Run Command"** to generate and execute the Python code
4. **Review the results** and download the modified CSV if needed

## Example Commands

- "Add a new column called 'total' that sums columns A and B"
- "Filter rows where column 'age' is greater than 25"
- "Replace all null values in column 'name' with 'Unknown'"
- "Sort the data by column 'date' in descending order"
- "Remove duplicate rows"

## Requirements

- Python 3.8+
- Azure OpenAI account with GPT-3.5-turbo or GPT-4 deployment
- Streamlit
- pandas
- langchain

## Security Note

Never commit your `.env` file to version control. It contains sensitive API keys that should be kept private.

## License

MIT License
