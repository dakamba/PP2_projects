import shutil
import os

# Move a file into test_dir
if os.path.exists("sample.txt"):
    os.makedirs("test_dir", exist_ok=True)
    shutil.move("sample.txt", "test_dir/sample.txt")
    print("sample.txt moved to test_dir/")
else:
    print("sample.txt not found to move")