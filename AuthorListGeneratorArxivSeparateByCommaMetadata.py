import pandas as pd


def generate_latex_codes(file_path):
    # Load the CSV data
    data = pd.read_csv(file_path)
    data = data.sort_values('Overall Order')

    # Extract unique affiliations and assign them IDs
    unique_affiliations = {}
    affil_counter = 1
    affil_columns = ['Affiliation 1 name', 'Affiliation 2 name', 'Affiliation 3 name', 'Affiliation 4 name']

    for idx, row in data.iterrows():
        for affil_col in affil_columns:
            affil = row[affil_col]
            if pd.notna(affil) and affil not in unique_affiliations:
                unique_affiliations[affil] = affil_counter
                affil_counter += 1

    # Generate LaTeX for authors
    author_lines = []
    for idx, row in data.iterrows():
        affil_ids = [str(unique_affiliations[row[affil_col]]) for affil_col in affil_columns if
                     pd.notna(row[affil_col])]
        if pd.isna(row['Middle Name(s)']) or (str(row['Middle Name(s)']).strip()) == '':
            full_name = f"{row['First Name']} {row['Last Name']}".strip()
        else:
            full_name = f"{row['First Name']} {row['Middle Name(s)']} {row['Last Name']}".strip()
        author_line = full_name
        #author_line = f"\\author[{','.join(affil_ids)}]{{{full_name}}}"
        author_lines.append(author_line)

    # Generate LaTeX for affiliations
    #affiliation_lines = [f"\\affil[{idx}]{{{affil}}}" for affil, idx in unique_affiliations.items()]
    affiliation_lines = [f"\\and {affil}" for affil, idx in unique_affiliations.items()]

    return ','.join(author_lines)


# Assuming the file path is correctly set to the path of your CSV file
file_path = r"C:\Users\dlabe\Downloads\Meningioma authors csv.csv"
latex_code = generate_latex_codes(file_path)

print(latex_code)
