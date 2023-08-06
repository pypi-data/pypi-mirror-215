from bitssh import inquirer, questions, console
from inquirer.themes import GreenPassion
import os
answers = inquirer.prompt(questions=questions, theme=GreenPassion())
cmd = answers['host']
cmd = cmd[6::]
cmd = f"ssh {cmd}"
console.print(
    "Please Wait While Your System is Connecting to the Remote Server", style="green")
os.system(cmd)
