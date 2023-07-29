import os
# It allows you to interact with the operating system, such as reading or writing files, managing directories.
import subprocess
# Which allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import sys
# Which provides access to some variables used or maintained by the interpreter.
import webbrowser
# It allows you to open URLs in the user's default web browser.
import argparse
#  Which makes it easy to write user-friendly command-line interfaces.
import shutil
# It provides functions for copying files, deleting files and directories, and more.
import platform
# Which gives access to various information about the host operating system, such as the operating system name, version, and architecture.

def check_dependencies():   #This line defines a function named check_dependencies without any arguments.
    # *****Check if Docker is installed*****
    try:    #The code inside the try block is executed, and if an exception occurs, it will be caught by the corresponding except block.
        subprocess.run(['docker', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # 1) ['docker', '--version'] : It tries to execute the Docker command to check if Docker is installed on the system.
        # 2) "check=True" : This argument in the subprocess.run() call instructs the function to raise a CalledProcessError exception if the return code of the command is non-zero. 
        # In this case, it means that Docker is not installed, and the except block will be executed.

    except subprocess.CalledProcessError:  # Exception is raised (i.e., Docker is not installed), the code inside this block will be executed.
        print("Docker is not installed. Please install Docker before running this script.")
        sys.exit(1)  # An exit code of 1 usually indicates an error, which means the script cannot proceed without Docker.

    # Check if Docker Compose is installed
    try:
        subprocess.run(['docker-compose', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Docker Compose is not installed. Please install Docker Compose before running this script.")
        sys.exit(1)

def create_wordpress_site(site_name):
    # Create a directory for the WordPress site

    # his line creates a directory with the name specified by site_name for the new WordPress site. The os.makedirs() function ensures that the directory is created. 
    # The exist_ok=True argument prevents raising an error if the directory already exists.
    os.makedirs(site_name, exist_ok=True)

    # Create docker-compose.yml file for the WordPress site
    with open(f"{site_name}/docker-compose.yml", "w") as compose_file:
        compose_file.write(f'''version: '3'
services:
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: root
      MYSQL_PASSWORD: example
      MYSQL_RANDOM_ROOT_PASSWORD: "yes"
    volumes:
      - db_data:/var/lib/mysql
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    restart: always
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: example
    volumes:
      - ./wp-content:/var/www/html/wp-content
  nginx:
    image: nginx:latest
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./wp-content:/var/www/html/wp-content
volumes:
  db_data:
''')

    # Create nginx.conf file for Nginx configuration
    with open(f"{site_name}/nginx.conf", "w") as nginx_conf:
        nginx_conf.write(f'''server {{
    listen 80;
    server_name {site_name};
    root /var/www/html;
    index index.php;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    location ~ \.php$ {{
        include fastcgi_params;
        fastcgi_pass wordpress:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }}
}}
''')

    # Add entry to /etc/hosts

    # 1) This line checks the host operating system using the platform.system() function. 
    # If the operating system is Windows, it will execute the following block of code. Otherwise, it will execute the else block.
    if platform.system() == "Windows":
        add_host_entry_windows(site_name)
        # This line calls the function add_host_entry_windows() and passes the site_name as an argument. 
    else:
        add_host_entry_unix(site_name)

    print(f"WordPress site '{site_name}' with a LEMP stack created successfully!")
    # This line uses an f-string to print a message indicating that the WordPress site with the specified site_name has been created successfully, and it is running on a LEMP stack (Linux, Nginx, MySQL, and PHP).
    
    print(f"Please wait for a moment while the site is being set up...")
    # This line prints a message informing the user to wait while the site is being set up. This may involve configurations and installations necessary for the WordPress site to function correctly.
    
    print("Opening the site in your default browser...")
    # This line prints a message indicating that the script is about to open the newly created WordPress site in the user's default web browser.
    
    webbrowser.open(f"http://{site_name}")
    # This line uses the webbrowser module to open the newly created WordPress site in the user's default web browser. It constructs the URL using the site_name variable, assuming that the site is accessible via http. 
    # The webbrowser.open() function will open the URL in the default web browser of the user's system.
    
# Function to add entry to the hosts file on Windows

# This line defines the function named add_host_entry_windows which takes site_name as an argument. The function is designed to add an entry to the Windows hosts file.
def add_host_entry_windows(site_name):
    import ctypes
    # This line imports the ctypes module, which allows calling functions from shared libraries written in C and provides access to some low-level Windows functionalities.

    # *****Check if the script is running with administrator privileges*****

    # This line checks whether the script is running with administrator privileges on Windows. It calls the IsUserAnAdmin() function from the shell32 library in the ctypes.windll namespace. 
    # If the script is not running with admin privileges, it prints an error message and exits the script with an exit code of 1.
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Error: The script needs to be run with administrator privileges to modify the hosts entry.")
        sys.exit(1)

    try:

        # This line imports the winreg module, which provides access to the Windows Registry. The Windows Registry is a hierarchical database that stores configuration settings and options for Windows and applications running on the system.
        import winreg

        # ***Open the Windows Registry key for the hosts entry***
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters")
        # This line opens the Windows Registry key for the TCP/IP parameters (hosts entry) using the winreg.OpenKey() function. 
        # It accesses the HKEY_LOCAL_MACHINE hive, which contains system-wide configuration data.

        # ***Read the existing value of the "DataBasePath" entry***
        data_path, _ = winreg.QueryValueEx(key, "DataBasePath")
        # This line reads the value of the "DataBasePath" entry from the previously opened registry key using the winreg.QueryValueEx() function. The value is stored in the data_path variable. 
        # The underscore _ is used to capture the second value returned by the function.

        # ***Construct the full path to the hosts file***
        hosts_path = os.path.join(data_path, "hosts")
        # This line constructs the full path to the hosts file by joining the data_path (retrieved from the registry) with the filename "hosts".

        # Add the entry to the hosts file
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f'127.0.0.1 {site_name}\n')
            # This line writes the entry for the specified site_name to the hosts file. 
            # It adds an entry mapping 127.0.0.1 (localhost) to the site_name, allowing the site to be accessed locally.

        print("Hosts entry added successfully.")
        # If the entry was added successfully, this line prints a success message.

    except Exception as e:
        # f an exception occurs within the try block (e.g., permission issues while accessing the registry or file), this line catches the exception and stores it in the variable e.

        print(f"Error: {e}")
        # If an exception occurred, this line prints an error message along with the specific exception details.


# ***Function to add entry to /etc/hosts on Unix-based systems***

# The function is designed to add an entry to the hosts file on Unix-based systems.
def add_host_entry_unix(site_name):

    # This line assigns the file path of the hosts file to the variable hosts_path. In Unix-based systems, the hosts file is usually located at /etc/hosts. 
    # The function will append an entry to this file.
    hosts_path = '/etc/hosts'

    # This line opens the hosts file in "append" mode using a context manager. 
    # The with statement ensures that the file is properly closed after the operation is done.
    with open(hosts_path, 'a') as hosts_file:

        # This line writes the entry for the specified site_name to the hosts file. 
        # It adds an entry mapping 127.0.0.1 (localhost) to the site_name, allowing the site to be accessed locally. 
        hosts_file.write(f'127.0.0.1 {site_name}\n')

# The function is responsible for enabling and running a WordPress site using Docker.
def enable_wordpress_site(site_name):

    # *****Start the Docker containers for the site*****

    # ['docker-compose', 'up', '-d']: This is the list of arguments for the Docker Compose command. 
    # docker-compose up -d is used to start the containers in detached mode (-d flag means detached mode, which runs the containers in the background).
    subprocess.run(['docker-compose', 'up', '-d'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # After starting the Docker containers, this line prints a message to the console, 
    # indicating that the specified WordPress site (site_name) is now enabled and running.
    print(f"WordPress site '{site_name}' is now enabled and running!")

# The function is responsible for disabling and stopping a WordPress site running in Docker containers.
def disable_wordpress_site(site_name):

    # *****Stop and remove the Docker containers for the site*****

    # ['docker-compose', 'down']: This is the list of arguments for the Docker Compose command. 
    # docker-compose down is used to stop and remove the containers defined in the docker-compose.yml file.
    subprocess.run(['docker-compose', 'down'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # After stopping and removing the Docker containers, this line prints a message to the console, 
    # indicating that the specified WordPress site (site_name) is now disabled and stopped.
    print(f"WordPress site '{site_name}' is now disabled and stopped!")


# The function is responsible for deleting a WordPress site running in Docker containers.
def delete_wordpress_site(site_name):

    # *****Stop and remove the Docker containers for the site*****

    # This line stops and removes the Docker containers associated with the specified WordPress site using Docker Compose.
    subprocess.run(['docker-compose', 'down'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # ******Delete the site directory and its contents*****

    try:
        #This line attempts to delete the entire site directory (including all its contents) using the shutil.rmtree() function. 
        # The shutil module provides functions for file operations, and rmtree() is used here to remove a directory recursively.
        shutil.rmtree(site_name)
        print(f"WordPress site '{site_name}' is deleted successfully!")
    except FileNotFoundError:
        print(f"WordPress site '{site_name}' does not exist.")
        
# This is a common Python idiom to check if the script is being run as the main program. 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage WordPress sites with Docker.")
    parser.add_argument("site_name", help="Name of the WordPress site")
    parser.add_argument("action", choices=["create", "enable", "disable", "delete"], help="Action to perform: create, enable, disable, or delete")

    args = parser.parse_args()
 
    # This condition checks if the supplied action is equal to "create." If it is, it executes the following indented block of code.
    if args.action == "create":
        check_dependencies()
        create_wordpress_site(args.site_name)
        print(f"Please wait for a moment while the site is being set up...")
        print("Opening the site in your default browser...")
        webbrowser.open(f"http://{args.site_name}")
    elif args.action == "enable":
        enable_wordpress_site(args.site_name)
    elif args.action == "disable":
        disable_wordpress_site(args.site_name)
    elif args.action == "delete":
        delete_wordpress_site(args.site_name)
    else:
        print("Invalid action. Please use 'create', 'enable', 'disable', or 'delete' as the action.")
