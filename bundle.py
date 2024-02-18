# Simple script to bundle a bunch of repositories.
import sys
import os
import subprocess

if __name__ == "__main__":
    # Validate user inputs
    
    args = sys.argv
    
    if len(args) != 2:
        print("Please only provide a repositories.csv file; each line containing a name followed by the clone url.")
        exit(1)
            
    file_path = args[1]
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("The provided repositories.csv file either does not exist or is not a file.")
        exit(1)
    
    # Ensure required directories exist.
    root_directory = os.getcwd()
    bundle_directory = root_directory + "/bundles"
    os.makedirs(root_directory + "/repositories", exist_ok = True)
    os.makedirs(bundle_directory, exist_ok = True)
    
    # Read repositories from provided file.
    
    repositories: list[(str, str)] = []
    
    with open(file_path, "r+") as file:
        lines = file.readlines()
        
        for line_number, line in enumerate(lines):
            line = line.rstrip("\r\n")
            
            if line.count(",") == 1:
                repositories.append(line.split(","))
            else:
                print(f"Skipping invalid repository definition on line {line_number + 1}.")
    
    # Change to repositories directory
    
    os.chdir("./repositories")
                
    for name, url in repositories:
        # region Skip if bundle exists already
        if os.path.exists(bundle_directory + f"/{name}.bundle"):
            print(f"Skipping {name}, bundle already exists.")
            continue
        # endregion
        
        # region Clone repository into repositories folder
        if not os.path.exists(name):
            completion = subprocess.run(["git", "clone", "--mirror", url, name])
            
            if completion.returncode != 0:
                print(f"Skipping {name}, got a non-zero return code when cloning the repository.")
                continue
            
            print(f"Got exit code {completion.returncode} after cloning {name}")
        else:
            print(f"Skipping the cloning of {name} because it already exists.")
        # endregion
        
        # region Create the bundle file
        os.chdir(f"./{name}")
        
        completion = subprocess.run(["git", "bundle", "create", f"{name}.bundle", "--all"])
            
        if completion.returncode != 0:
            print(f"Skipping {name}, got a non-zero return code when creating the bundle.")
            continue
        
        os.chdir("..") # Back into the repositories folder
        # endregion
        
        # region Move bundle file to bundles folder
        os.rename(f"./{name}/{name}.bundle", f"../bundles/{name}.bundle")
        # endregion
        
    os.chdir("..") # Back to root