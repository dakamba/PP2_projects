import shutil
import os

# Copy the file
if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "sample_backup.txt")
    print("sample.txt copied to sample_backup.txt")
else:
    print("sample.txt not found!")

# Delete the backup safely
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("sample_backup.txt deleted")