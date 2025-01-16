from tabulate import tabulate

def table_with_arrows():
    print("Enter a number between 1-5 to choose the position of the arrow above the smiley.\n")

    # Predefined table structure (without the "Ausstehend" column)
    table_data = [
        ["Selbsteinschätzung", "", "", "", "", "", ""],
        ["Qualität des Eintrags", "", "", "", "", ""],  # Row for arrows (5 columns for arrow placement)
        ["", ":laughing:", ":smiley:", ":neutral_face:", ":worried:", ":tired_face:"],  # Smiley row
        ["Effektivität in der Berichtsperiode", "", "", "", "", ""],  # Row for arrows (5 columns for arrow placement)
    ]

    # User interaction for each category
    for row_index, category in enumerate(["Qualität des Eintrags", "Effektivität in der Berichtsperiode"]):
        print(f"\nCategory: {category}")
        
        while True:
            smiley_column = input(f"Select a number (1-5) for '{category}': ")

            # Check if input is a valid number and within the range 1-5
            if smiley_column.isdigit() and 1 <= int(smiley_column) <= 5:
                smiley_column_index = int(smiley_column)  # Convert to integer
                
                # Clear previous arrows and set the new one
                for col in range(1, 6):  # Columns 1-5 (5 columns for arrows)
                    table_data[row_index * 2 + 1][col] = ""  # Clear any existing arrow (row * 2 + 1 for correct row)

                # Set the arrow based on the row (up or down)
                if row_index == 0:  # First category
                    table_data[row_index * 2 + 1][smiley_column_index] = ":arrow_double_down:"
                else:  # Second category
                    table_data[row_index * 1 + 2][smiley_column_index] = ":arrow_double_up:"  
                break  # Exit the loop after valid input
            else:
                print("Invalid selection. Please enter a number between 1 and 5.")

    # Generate and print the Markdown table
    markdown_table = tabulate(table_data, headers="firstrow", tablefmt="github")
    print("\nGenerated Markdown Table:")
    print(markdown_table)

    return markdown_table

# Example usage
if __name__ == "__main__":
    markdown_output = table_with_arrows()
