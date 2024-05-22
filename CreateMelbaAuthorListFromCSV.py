import pandas as pd


def generate_latex_authors_multiple_cols(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Start the LaTeX author block
    latex_authors = "\\author{\n"

    # Define how many affiliation columns you expect at most
    max_affiliations = 3  # Adjust this number based on your CSV format

    # Loop through each row in the DataFrame
    for index, row in data.iterrows():
        # Prepare the author's basic information
        first_name = row['First Name']
        middle_names = row['Middle Name(s)']
        last_name = row['Last Name']
        email = row['Email']

        # Construct the LaTeX line for this author

        latex_authors += f"\t\\firstname {first_name} {middle_names} \\surname {last_name} \\email {email} \\\\\n"
        for i in range(1, max_affiliations + 1):
            affiliation_key = f"Affiliation{i}"
            if affiliation_key in row and pd.notna(row[affiliation_key]):
                affiliation = row[affiliation_key].strip()
                if affiliation:
                    latex_authors += f"\t\\addr {affiliation}"
                    if i < max_affiliations and pd.notna(row.get(f"Affiliation{i + 1}", "")):
                        latex_authors += " \\\\\n"
                    else:
                        latex_authors += "\n"

        # If not the last author, add the LaTeX command for the next author
        if index < len(data) - 1:
            latex_authors += "\t\\AND\n"

    # Close the author block
    latex_authors += "}"

    return latex_authors


# Example usage
file_path = r"C:\Users\dlabe\Downloads\Meningioma authors csv.csv"
latex_code = generate_latex_authors_multiple_cols(file_path)
print(latex_code)