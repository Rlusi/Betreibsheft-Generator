import time
from datetime import datetime, timedelta
from pathlib import Path
import os
from colorama import init, Fore
from tabulate import tabulate

# Initialize colorama for colored console output
init(autoreset=True)

class LogbookEntry:
    def __init__(self):
        self.current_time = datetime.now()
        self.script_dir = Path(__file__).parent
        self.logs_dir = self.script_dir / "BetriebsheftEinträge"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate date ranges
        self.current_weekday = self.current_time.weekday()
        self.week_start = self.current_time - timedelta(days=self.current_weekday)
        self.week_end = self.week_start + timedelta(days=4)
        
        # Format dates for different uses
        self.formatted_date = self.current_time.strftime("%d-%m-%Y")
        self.formatted_time = self.current_time.strftime("%H-%M")
        self.week_start_formatted = self.week_start.strftime("%Y.%m.%d")
        self.week_end_formatted = self.week_end.strftime("%Y.%m.%d")
        
        # Template paths
        self.template_path = self.script_dir / "template.md"
        self.human_template_path = self.script_dir / "HumanTemplate.md"

    def read_template(self, template_path):
        """Read and return content from a template file."""
        try:
            with open(template_path, "r", encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(Fore.RED + f"Template file not found: {template_path}")
            exit(1)

    def get_multiline_input(self, prompt):
        """Collect multiline input from user."""
        print(f"\nEnter text for {prompt} (Type 'done' or 'end' to finish):")
        lines = []
        while True:
            line = input("- ").strip()
            if line.lower() in {"done", "end"}:
                break
            if line:
                lines.append(line)
        return '\n- '.join(lines) if lines else ""

    def create_table(self, columns, prompts=None):
        """Create a markdown table with specified columns and optional input prompts."""
        if prompts is None:
            prompts = [""] * len(columns)
        
        print("\nType 'done' or 'end' to finish entering data.")
        table_data = [columns]  # Header row
        
        while True:
            row_data = []
            for col, prompt in zip(columns, prompts):
                value = input(f"{col} {prompt}: ").strip()
                if value.lower() in {"done", "end"}:
                    return tabulate(table_data, headers="firstrow", tablefmt="github")
                row_data.append(value)
            table_data.append(row_data)

    def create_assessment_table(self):
        """Create the self-assessment table with arrows and smileys."""
        table_structure = [
            ["Selbsteinschätzung", "", "", "", "", "", ""],
            ["Qualität des Eintrags", "", "", "", "", ""],
            ["", ":laughing:", ":smiley:", ":neutral_face:", ":worried:", ":tired_face:"],
            ["Effektivität in der Berichtsperiode", "", "", "", "", ""]
        ]

        categories = ["Qualität des Eintrags", "Effektivität in der Berichtsperiode"]
        for idx, category in enumerate(categories):
            while True:
                try:
                    position = int(input(f"\nSelect position (1-5) for {category}: "))
                    if 1 <= position <= 5:
                        arrow = ":arrow_double_down:" if idx == 0 else ":arrow_double_up:"
                        row_idx = 1 if idx == 0 else 3
                        table_structure[row_idx][position] = arrow
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        return tabulate(table_structure, headers="firstrow", tablefmt="github")

    def generate_logbook(self):
        """Main function to generate the logbook entry."""
        print(f"Creating logbook entry for week: {self.week_start_formatted} - {self.week_end_formatted}")
        
        log_title = input("\nEnter the title of the entry: ")
        manual_entry = input("Do you want to enter the log content manually? (y/n): ").lower().strip() == 'y'

        template_content = self.read_template(self.template_path)
        
        # Replace common placeholders
        replacements = {
            "dd.mm.yyyy - dd.mm.yyyy": f"{self.week_start_formatted} - {self.week_end_formatted}",
            "Title": log_title,
            "YYYY-MM-DD": self.formatted_date,
            "HH:MM": self.formatted_time
        }

        for old, new in replacements.items():
            template_content = template_content.replace(old, new)

        if manual_entry:
            # Collect user input for each section
            goals_table = self.create_table(
                ["Ziel / Auftrag", "Zieltermin", "Ziel erreicht am"],
                ["", "(DD.MM.YYYY)", "(DD.MM.YYYY)"]
            )
            achievements = self.get_multiline_input("Was mir gut gelungen ist")
            difficulties = self.get_multiline_input("Was mir Schwierigkeiten bereitet hat")
            learnings = self.get_multiline_input("Was ich für die Zukunft mitnehme")
            self_assessment = self.create_assessment_table()
            assessment_notes = input("\nErläutern Sie Ihre Einschätzung kurz: ")
            feedback = self.create_assessment_table()

            # Replace placeholders with content
            content_replacements = {
                "T0": goals_table,
                "M0": f"> {achievements}",
                "M1": f"> {difficulties}",
                "M2": f"> {learnings}",
                "T1": self_assessment,
                "M3": f"> {assessment_notes}",
                "T2": feedback
            }
        else:
            # Use human template content for placeholders
            human_template = self.read_template(self.human_template_path)
            content_replacements = {
                "T0": "",
                "M0": "",
                "M1": "",
                "M2": "",
                "T1": "",
                "M3": "",
                "T2": ""
            }
            template_content = human_template

        # Apply all replacements
        for placeholder, content in content_replacements.items():
            template_content = template_content.replace(placeholder, content)

        # Save the generated content
        output_path = self.logs_dir / f"{self.week_start_formatted}.md"
        try:
            with open(output_path, "w", encoding='utf-8') as file:
                file.write(template_content)
            print(Fore.GREEN + f"\nLogbook entry created successfully: {output_path}")
        except Exception as e:
            print(Fore.RED + f"\nError saving logbook entry: {e}")

if __name__ == "__main__":
    logbook = LogbookEntry()
    logbook.generate_logbook()