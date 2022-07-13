import subprocess


archive = subprocess.check_output(["zip", "-", "./data", "-r"])
archive_name = "photos"

with open(f"{archive_name}.zip", "wb") as file:
    file.write(archive)
