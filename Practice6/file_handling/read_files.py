# Read and print file contents
try:
    with open("sample.txt", "r") as f:
        content = f.read()
    print("Contents of sample.txt:")
    print(content)
except FileNotFoundError:
    print("sample.txt not found. Please run write_files.py first.")