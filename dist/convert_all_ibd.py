import subprocess
from pathlib import Path
import zipfile

# === FIXED PATH TO main.py FROM ibd2sql ===
IBD2SQL_PATH = Path("PATH/TO/LIBRARY/main.py") # Replace with correct path
RECURSIVE = False  # Set to True if you want to include subfolders

# === FOLDER WHERE THIS SCRIPT IS LOCATED ===
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = SCRIPT_DIR / "combined_output.sql"
ZIP_FILE = SCRIPT_DIR / "combined_output.zip"

def find_ibd_files(folder: Path, recursive: bool = False):
    files = folder.rglob("*.ibd") if recursive else folder.glob("*.ibd")
    return sorted(files, key=lambda f: f.name.lower())  # sort alphabetically (case-insensitive)

def convert_ibd_files():
    with open(OUTPUT_FILE, "w") as outfile:
        for ibd_file in find_ibd_files(SCRIPT_DIR, RECURSIVE):
            print(f"Processing: {ibd_file.name}")
            result = subprocess.run(
                ["python3", str(IBD2SQL_PATH), str(ibd_file), "--sql", "--ddl"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                outfile.write(result.stdout)
                outfile.write("\n")
            else:
                print(f"❌ Error processing {ibd_file.name}:\n{result.stderr}")

    print(f"✅ SQL export complete: {OUTPUT_FILE}")
    compress_sql_output()

def compress_sql_output():
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(OUTPUT_FILE, OUTPUT_FILE.name)
    print(f"✅ Compressed into: {ZIP_FILE}")

if __name__ == "__main__":
    convert_ibd_files()
