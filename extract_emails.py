import os
import pandas as pd

FOLDER_PATH = "businesses"  # Update this if needed

def extract_valid_emails():
    all_emails = set()  # Use a set to avoid duplicates

    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".csv"):
            file_path = os.path.join(FOLDER_PATH, file)
            df = pd.read_csv(file_path)

            if "Email" in df.columns:
                valid_emails = df[df["Email"] != "N/A"]["Email"].dropna().unique()
                all_emails.update(valid_emails)

    if not all_emails:
        print("No valid emails found.")
        return

    timestamp = pd.Timestamp.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"extracted_emails_{timestamp}.csv"
    pd.DataFrame(list(all_emails)).to_csv(output_filename, index=False, header=False)
    print(f"Extracted emails saved to {output_filename}")

if __name__ == "__main__":
    extract_valid_emails()
