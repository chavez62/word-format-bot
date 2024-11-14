import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Style, init
import time
from typing import Optional, Dict, List
from dataclasses import dataclass
import json
from pathlib import Path
import logging

# Initialize colorama for Windows compatibility
init(autoreset=True)

@dataclass
class TaskConfig:
    name: str
    description: str
    instruction: str
    max_tokens: int = 500
    temperature: float = 0.7

class TextFormatterBot:
    def __init__(self):
        self.model_name = "gpt-4-1106-preview"
        self.tasks: Dict[str, TaskConfig] = {
            'formal': TaskConfig(
                name="formal",
                description="Professional and polished format",
                instruction="Please rewrite the following text in a professional, clear, and well-structured format, "
                           "fixing any typos or grammatical errors."
            ),
            'bullet': TaskConfig(
                name="bullet",
                description="Convert to organized bullet points",
                instruction="Please convert the following text into organized bullet points, "
                           "fixing any typos or grammatical errors."
            ),
            'summarize': TaskConfig(
                name="summarize",
                description="Create a clear summary",
                instruction="Please provide a clear, organized summary of the following text, "
                           "fixing any typos or grammatical errors.",
                max_tokens=300
            )
        }
        self.history_file = Path("formatting_history.json")
        self.setup_logging()
        self.client = None

    def setup_logging(self):
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('formatter_bot.log'),
                logging.StreamHandler()
            ]
        )

    def load_config(self) -> None:
        """Load environment variables and configure OpenAI client."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = openai.OpenAI(api_key=api_key)

    def save_to_history(self, input_text: str, task: str, output_text: str) -> None:
        """Save formatting results to history file."""
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            
            history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'task': task,
                'input_length': len(input_text),
                'output_length': len(output_text)
            })
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save history: {e}")

    def get_multiline_input(self) -> Optional[str]:
        """Get multi-line input from user with improved handling and validation."""
        print(Fore.CYAN + "\n=== TEXT INPUT MODE ===")
        print(Fore.YELLOW + "Commands:")
        print(Fore.WHITE + "- Type or paste your text")
        print(Fore.WHITE + "- '/done' to finish")
        print(Fore.WHITE + "- '/cancel' to cancel")
        print(Fore.WHITE + "- '/clear' to clear current input")
        print(Fore.WHITE + "- '/preview' to see current input\n")
        
        lines: List[str] = []
        while True:
            try:
                line = input(Fore.WHITE + "> ").strip()
                
                if line.lower() == '/done':
                    if not lines:
                        print(Fore.RED + "No text entered. Please enter some text or '/cancel'")
                        continue
                    break
                elif line.lower() == '/cancel':
                    return None
                elif line.lower() == '/clear':
                    lines.clear()
                    print(Fore.YELLOW + "Input cleared")
                    continue
                elif line.lower() == '/preview':
                    if lines:
                        print(Fore.CYAN + "\nCurrent input:")
                        print(Style.BRIGHT + '\n'.join(lines) + "\n")
                    else:
                        print(Fore.YELLOW + "No input yet")
                    continue
                
                lines.append(line)
                
            except KeyboardInterrupt:
                return None
            
        return '\n'.join(lines)

    def get_task_choice(self) -> Optional[str]:
        """Get the formatting task choice from user with improved UI."""
        while True:
            print(Fore.CYAN + "\n=== CHOOSE FORMATTING TASK ===")
            print(Fore.YELLOW + "Available options:")
            
            for i, (task_name, task_config) in enumerate(self.tasks.items(), 1):
                print(f"{Fore.WHITE}{i}. {task_name:<8} - {task_config.description}")
            
            choice = input(Fore.MAGENTA + "\nEnter your choice (number or name): ").strip().lower()
            
            if choice == 'cancel':
                return None
                
            # Handle numeric input
            try:
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(self.tasks):
                        return list(self.tasks.keys())[index]
            except ValueError:
                pass
                
            # Handle text input
            if choice in self.tasks:
                return choice
                
            print(Fore.RED + f"Invalid choice. Please select a number (1-{len(self.tasks)}) "
                           f"or one of: {', '.join(self.tasks.keys())}")
            time.sleep(1)

    def format_text(self, input_text: str, task: str) -> str:
        """Format text using OpenAI API with improved error handling and retry logic."""
        if not input_text.strip():
            raise ValueError("Input text cannot be empty")
        
        if not self.client:
            raise ValueError("OpenAI client not initialized")
        
        task_config = self.tasks[task]
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": task_config.instruction},
                        {"role": "user", "content": input_text}
                    ],
                    max_tokens=task_config.max_tokens,
                    temperature=task_config.temperature
                )
                
                formatted_text = response.choices[0].message.content
                self.save_to_history(input_text, task, formatted_text)
                return formatted_text
                
            except openai.APIError as e:
                logging.error(f"OpenAI API error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise Exception("Failed to format text after multiple attempts")
                    
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                raise

    def run(self) -> int:
        """Main loop with improved error handling and user experience."""
        try:
            self.load_config()
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(Fore.CYAN + "=== Text Formatter Bot ===")
            print(Fore.CYAN + "Format your text professionally with AI assistance\n")

            while True:
                try:
                    print(Fore.YELLOW + "Commands:")
                    print(Fore.WHITE + "- Press Enter to start")
                    print(Fore.WHITE + "- Type 'exit' to quit")
                    print(Fore.WHITE + "- Type 'stats' to view usage statistics\n")
                    
                    command = input(Fore.MAGENTA + "> ").strip().lower()
                    
                    if command == 'exit':
                        print(Fore.GREEN + "\nThank you for using Text Formatter Bot!")
                        break
                    elif command == 'stats':
                        self.display_statistics()
                        continue

                    # Get and validate input
                    user_input = self.get_multiline_input()
                    if not user_input:
                        continue

                    # Get task choice
                    task_type = self.get_task_choice()
                    if not task_type:
                        continue

                    # Process text with progress indicator
                    print(Fore.CYAN + "\nFormatting your text... ⏳")
                    formatted_output = self.format_text(user_input, task_type)
                    
                    # Display results
                    print(Fore.CYAN + "\n=== FORMATTING RESULT ===")
                    print(Fore.BLUE + f"\nTask: {task_type.upper()}")
                    print(Style.BRIGHT + formatted_output + "\n")
                    print(Fore.CYAN + "=" * 50 + "\n")

                except KeyboardInterrupt:
                    print(Fore.YELLOW + "\nOperation cancelled by user.")
                    continue
                except Exception as e:
                    logging.error(f"Error during text formatting: {str(e)}")
                    print(Fore.RED + f"Error: {str(e)}")
                    time.sleep(2)

        except Exception as e:
            logging.critical(f"Fatal error: {str(e)}")
            print(Fore.RED + f"Fatal error: {str(e)}")
            return 1
            
        return 0

    def display_statistics(self) -> None:
        """Display usage statistics from history."""
        if not self.history_file.exists():
            print(Fore.YELLOW + "\nNo usage history available yet.")
            return
            
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                
            if not history:
                print(Fore.YELLOW + "\nNo usage history available yet.")
                return
                
            print(Fore.CYAN + "\n=== USAGE STATISTICS ===")
            
            # Calculate basic stats
            total_uses = len(history)
            task_counts = {}
            total_input_length = 0
            total_output_length = 0
            
            for entry in history:
                task = entry['task']
                task_counts[task] = task_counts.get(task, 0) + 1
                total_input_length += entry['input_length']
                total_output_length += entry['output_length']
            
            # Display stats
            print(Fore.WHITE + f"\nTotal uses: {total_uses}")
            print(Fore.WHITE + "\nTask usage:")
            for task, count in task_counts.items():
                percentage = (count / total_uses) * 100
                print(f"- {task}: {count} ({percentage:.1f}%)")
                
            avg_input_length = total_input_length / total_uses
            avg_output_length = total_output_length / total_uses
            
            print(Fore.WHITE + f"\nAverage input length: {avg_input_length:.0f} characters")
            print(Fore.WHITE + f"Average output length: {avg_output_length:.0f} characters")
            
            print(Fore.CYAN + "\n" + "=" * 50 + "\n")
            
        except Exception as e:
            logging.error(f"Error displaying statistics: {e}")
            print(Fore.RED + "Error loading statistics")

if __name__ == "__main__":
    bot = TextFormatterBot()
    exit(bot.run())
