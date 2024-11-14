# Text Formatter Bot 🤖

A command-line tool that uses OpenAI's GPT models to intelligently format and transform text. Perfect for cleaning up notes, formatting documents, and creating summaries.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🎨 Multiple formatting options (formal, bullet points, summaries)
- 📊 Usage statistics tracking
- 🎯 Intelligent text processing using GPT-4
- 💾 Command history and session logging
- 🎭 Rich command-line interface with color coding
- ⚡ Robust error handling and retry logic

## 🚀 Quick Start

### Prerequisites

```bash
python -m pip install --upgrade pip
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/text-formatter-bot.git
cd text-formatter-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Usage

Run the bot:
```bash
python formatter_bot.py
```

## 🎮 Commands

While using the bot:

### Main Menu
- Press `Enter` to start formatting
- Type `exit` to quit
- Type `stats` to view usage statistics

### Text Input Mode
- Type or paste your text
- `/done` to finish input
- `/cancel` to cancel operation
- `/clear` to clear current input
- `/preview` to see current input

## 🛠 Available Formatting Tasks

1. **Formal Format**
   - Transforms text into a professional, well-structured format
   - Fixes grammar and typos
   - Perfect for business communications

2. **Bullet Points**
   - Converts text into organized bullet points
   - Maintains key information
   - Ideal for lists and summaries

3. **Summarize**
   - Creates a clear, concise summary of the text
   - Maintains core message
   - Great for long documents

## 📊 Statistics

The bot keeps track of:
- Total number of uses
- Task usage distribution
- Average input/output lengths
- Historical formatting data

Access statistics by typing `stats` at the main menu.

## 🔧 Configuration

Task configurations can be modified in the `TaskConfig` class:

```python
@dataclass
class TaskConfig:
    name: str
    description: str
    instruction: str
    max_tokens: int = 500
    temperature: float = 0.7
```

## 📝 Logging

The bot maintains two types of logs:
1. Application logs (`formatter_bot.log`)
2. Usage history (`formatting_history.json`)

## 🔒 Security

- API keys are loaded from environment variables
- Input validation for all user commands
- Secure error handling without exposing sensitive information

## ⚡ Performance

- Implements retry logic for API calls
- Efficient input handling for large text blocks
- Optimized memory usage for long sessions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Dependencies

- `openai`: OpenAI API interface
- `python-dotenv`: Environment variable management
- `colorama`: Terminal color support
- `logging`: Application logging
- `pathlib`: File path handling

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Contributors and testers
- The Python community

## ⚠️ Requirements

- Python 3.7 or higher
- OpenAI API key
- Internet connection

---

Made with ❤️ by [Louis Chavez]

Remember to ⭐ this repository if you found it helpful!
