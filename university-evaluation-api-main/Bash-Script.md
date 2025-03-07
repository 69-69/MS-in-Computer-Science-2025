# SETUP & RUN PYTHON PROJECT via BASH-SCRIPT IN A VIRTUAL ENV.: 
>(This script create & activate virtual env., install project’s dependencies from requirements.txt & start the flask webServer )

- Create requirement.txt file & include all project dependencies into the file.
- Create a start.sh file in your root directory and paste the below content in it
- Run CMD: ./start.sh
— Content Of The start.sh File —: 

>#!/bin/bash

```shell
# Create a virtual environment
echo 'Creating virtual environment'
python3 -m venv .venv

# Activate the virtual environment
echo 'Activating Virtual Environment...'
source .venv/bin/activate

# Variables for MySQL Setup
MYSQL_ROOT_PASSWORD = ‘root_password’ # Specifiy root password
#MySQL User Details
MYSQL_USER = ‘root’ # The new username for MySQL
MYSQL_USER_PASSWORD = ‘Winner@69’ # The new password for the new MySQL user
MYSQL_DB = ‘app_db’ # The name for the database to create

# Install Mysql if not installed
if ! command -v mysql &> /dev/null
then
	echo ‘MySQL is not found. Installing MySQL…’
	sudo apt update
	sudo apt install -y mysql-server
	sudo mysql_secure_installation
fi

# Start MySQL Service (in case it’s not running)
sudo systemctl start mysql

# Log in to MySQL as root and Create the user, password and database
echo ‘Setting up MySQL User and Database…’ 
sudo mysql -u root -p”$MYSQL_ROOT_PASSWORD“ <<EOF
CREATE DATABASE IF NOT EXISTS $MYSQL_DB;
CREATE USER IF NOT EXISTS ‘$MYSQL_USER’@‘localhost’ IDENTIFIED BY ‘$MYSQL_ROOT_PASSWORD’;
GRANT ALL PRIVILEGES ON’$MYSQL_DB’ TO ‘$MYSQL_USER’@‘localhost’;
FLUSH PRIVILEGES;
EOF

echo ‘MySQL User: “$MYSQL_USER” created with Password: “$MYSQL_ROOT_PASSWORD” and granted Privileges on “MYSQL_DB”…’

# Install dependencies
echo ‘Installing Requirements / Dependencies…’
pip install -r requirements.txt

echo ‘MySQL and Dependencies installed successfully…’ 

# Start the Flask app
echo ‘Starting App or Server…’
python app.py
```


### Bundle or Package MySQL Installer with .EXE file or app.py file in Python:

>**Windows OS: Download MySQL Installer:**
Go to MySQL Installer Download
Download the installer, thus .EXE file (eg: mysql-iunbstaller-community-8.0.XX.X.exe file)
Place the installer in your python project root or sub directory

>**Windows OS: Packaging / Bundling the Python App as .EXE using PyInstaller:**

```shell
pyinstaller --onefile --add-data "path_to_mysql_installer/mysql-installer-community-*.exe;." __init__.py
```

>**Mac OS: Packaging / Bundling the Python App as .dmg using PyInstaller:**
```shell
pyinstaller --onefile __init__.py
```



```python
# setup.py

import subprocess
import os
import sys
import time
import platform

class Setup():
    def check_os_type(self):
        """Check OS type: Windows, Mac, or Linux"""
        if os.name == 'posix':  # Unix-like (Linux, Mac)
            os_name = platform.system()
            if os_name == 'Darwin':  # macOS
                print("This is a macOS system.")
                return 'isMac'
            else:  # Linux
                print("This is a Unix-like system (e.g., Linux).")
                return 'isLinux'
        elif os.name == 'nt':  # Windows
            print("This is a Windows system.")
            return 'isWin'
        else:
            print("Unknown OS")
            return 'isUnknown'
    
    def check_homebrew_installed(self):
        """Check if Homebrew is installed on macOS"""
        try:
            subprocess.check_call(["brew", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def install_homebrew(self):
        """Install Homebrew if it's not installed on macOS"""
        print("Homebrew is not installed. Installing Homebrew...")
        try:
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True, check=True
            )
            print("Homebrew installation completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Homebrew: {e}")
            sys.exit(1)
    
    def check_mysql_installed(self):
        """Check if MySQL is installed by looking for the mysql executable"""
        try:
            subprocess.check_call("mysql --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def install_mysql_for_mac_os(self, root_password):
        """Install MySQL on macOS using Homebrew and set the root password"""
        if not self.check_homebrew_installed():
            self.install_homebrew()
    
        print("Installing MySQL on macOS...")
        try:
            # Install MySQL using Homebrew
            subprocess.run(["brew", "install", "mysql"], check=True)
            print("MySQL installation completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing MySQL: {e}")
            sys.exit(1)
    
        # Start MySQL service
        print("Starting MySQL service...")
        try:
            subprocess.run(["brew", "services", "start", "mysql"], check=True)
            print("MySQL service started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting MySQL service: {e}")
            sys.exit(1)
    
        # Set the root password for MySQL
        print("Setting the root password for MySQL...")
        try:
            # The following command sets the root password
            subprocess.run(
                f"mysqladmin -u root password '{root_password}'", shell=True, check=True
            )
            print(f"Root password set to: {root_password}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting root password: {e}")
            sys.exit(1)
    
    def get_mysql_installer_path(self):
        """Get the path to the MySQL installer for Windows"""
        if hasattr(sys, '_MEIPASS'):
            # If running from PyInstaller .exe, extract from the bundled temp folder
            return os.path.join(sys._MEIPASS, "mysql-installer-community-*.exe")
        else:
            # If running from source, assume it's in the current directory
            return "mysql-installer-community-*.exe"
    
    def install_mysql_for_windows_os(self, root_password):
        """Install MySQL on Windows silently using MySQL installer"""
        installer_path = self.get_mysql_installer_path()
        
        if os.path.exists(installer_path):
            print("MySQL not found. Installing MySQL...")
            try:
                subprocess.run([
                    installer_path,
                    "/quiet",  # Silent install
                    "/norestart",  # Don't restart the system
                    "/install",  # Install MySQL
                    f"/rootPassword={root_password}"  # Set root password
                ], check=True)
                print("MySQL installation completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error installing MySQL: {e}")
                sys.exit(1)  # Exit the script if installation fails
        else:
            print("MySQL installer not found!")
            sys.exit(1)  # Exit the script if the installer is not found
    
    def setup_mysql_database_and_user(self, username, password, database, root_password):
        """Set up a new MySQL user, password, and database after installation"""
        print(f"Setting up MySQL user '{username}', password, and creating database '{database}'...")
    
        # Wait until MySQL is ready to accept commands
        time.sleep(10)  # Give MySQL some time to start (you can replace this with a proper check)
    
        try:
            # Command to execute MySQL commands: Create database and user, then grant permissions
            mysql_command = f"""
            mysql -u root -p{root_password} -e "CREATE DATABASE IF NOT EXISTS {database};"
            mysql -u root -p{root_password} -e "CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}';"
            mysql -u root -p{root_password} -e "GRANT ALL PRIVILEGES ON {database}.* TO '{username}'@'localhost';"
            mysql -u root -p{root_password} -e "FLUSH PRIVILEGES;"
            """
            subprocess.run(mysql_command, shell=True, check=True)
            print(f"Successful: User '{username}' created and granted privileges on database '{database}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting up MySQL user and database: {e}")
            sys.exit(1)
    
    def wait_for_mysql_installation(self):
        """Wait for MySQL to be fully installed and running"""
        print("Waiting for MySQL to start...")
        max_retries = 15
        retries = 0
    
        while retries < max_retries:
            if self.check_mysql_installed():
                print("MySQL is installed and running.")
                return True
            else:
                retries += 1
                print(f"Retrying ({retries}/{max_retries})... MySQL not yet available.")
                time.sleep(2)  # Wait for 2 seconds before retrying
    
        # If MySQL is not available after max retries, exit
        print("MySQL installation failed or MySQL service is not running.")
        sys.exit(1)
```

```python
# __init__.py

import subprocess
import sys

from . import Setup

class Main():
    def app(self):
        """Main function to check and install MySQL, then run the application"""
        root_password = "your_root_password"  # Specify the root password
        username = "your_username"  # The new username for MySQL
        password = "your_password"  # The password for the new MySQL user
        database = "your_database"  # The name of the database to create
    
        # Step 1: Install MySQL if not installed
        if not Setup.check_mysql_installed():
            os_type = Setup.check_os_type()
    
            if os_type == 'isMac':
                Setup.install_mysql_for_mac_os(root_password)
                Setup.wait_for_mysql_installation()
                Setup.setup_mysql_database_and_user(username, password, database, root_password)
            elif os_type == 'isWin':
                Setup.install_mysql_for_windows_os(root_password)
                Setup.wait_for_mysql_installation()
                Setup.setup_mysql_database_and_user(username, password, database, root_password)
            else:
                print("Unsupported operating system.")
                sys.exit(1)
    
        # Step 2: Set up user, password, and database if MySQL is already installed
        Setup.setup_mysql_database_and_user(username, password, database, root_password)
    
        # Proceed with your application logic
        print("Starting MyApp...")
        # Example: Run the actual application or start the packaged .exe
        subprocess.run(["path_to_your_app.exe"])  # Replace with the actual path to your executable
```

```python
# app.app.py

from flask import Flask
from . import Main

app = Flask(__name__)

Main.app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
```


# Automatically Run the 'Batch or .bat (Windows OS) or shell or .sh (Mac OS)' Script/File in Python
```python
import subprocess
import sys
import os

def run_script(script_path):
    """Run a script based on its type (Windows or macOS/Linux)"""
    if sys.platform.startswith('win'):  # Check if running on Windows
        # Run .bat file (Windows)
        if os.path.exists(script_path):
            try:
                print(f"Running script {script_path} on Windows...")
                subprocess.run([script_path], check=True, shell=True)
                print(f"Script {script_path} executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing {script_path}: {e}")
        else:
            print(f"{script_path} not found.")
    elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):  # macOS/Linux
        # Run .sh file (macOS/Linux)
        if os.path.exists(script_path):
            try:
                print(f"Running script {script_path} on macOS/Linux...")
                # Make the script executable first
                subprocess.run(['chmod', '+x', script_path], check=True)
                subprocess.run([script_path], check=True, shell=True)
                print(f"Script {script_path} executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing {script_path}: {e}")
        else:
            print(f"{script_path} not found.")
    else:
        print("Unsupported operating system.")

def main():
    # Example path to the script
    script_path = "install_and_run.sh"  # Change this to your script's path
    if sys.platform.startswith('win'):
        script_path = "install_and_run.bat"  # On Windows, use .bat script
    
    run_script(script_path)

if __name__ == "__main__":
    main()
```