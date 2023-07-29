# Task

Create a command-line script, preferably in Bash, PHP, Node, or Python to perform the following tasks:

   1) Check if docker and docker-compose is installed on the system. If not present, install the missing packages.
   2) The script should be able to create a WordPress site using the latest WordPress Version. Please provide a way for the user to provide the site name as a command-line argument.
   3) It must be a LEMP stack running inside containers (Docker) and a docker-compose file is a must.
   4) Create a /etc/hosts entry for example.com pointing to localhost. Here we are assuming the user has provided example.com as the site name.
   5) Prompt the user to open example.com in a browser if all goes well and the site is up and healthy.
   6) Add another subcommand to enable/disable the site (stopping/starting the containers)
   7) Add one more subcommand to delete the site (deleting containers and local files)

# Docker WordPress Manager

The Docker WordPress Manager is a powerful and versatile command-line tool designed to simplify the management of WordPress sites by leveraging the capabilities of Docker and the LEMP stack. With this script, developers and system administrators can effortlessly create, deploy, and manage multiple WordPress instances within isolated Docker containers. 

Overall, the Docker WordPress Manager empowers developers and administrators to efficiently manage WordPress sites in Docker containers, providing a robust, secure, and scalable environment for WordPress development and production environments.

## Prerequisites

Before using this script, ensure that you have the following prerequisites installed on your system:

1. **Python**: Ensure you have Python installed on your system. The Docker WordPress Manager is written in Python, so you'll need a working Python environment.
   - Most modern systems come with Python pre-installed. However, if you need to install it, visit the official Python website and follow the installation instructions for your operating system.

2. **Operating System**: The Docker WordPress Manager script is designed to work on various operating systems, including macOS, Windows, and Linux.
   - Ensure that your operating system is supported by Docker and Docker Compose. Refer to the official Docker documentation for specific requirements for your OS.

4. **Docker**: Docker is required to run containers. Follow the official documentation to install Docker for your operating system:
   - Docker Desktop for macOS and Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Docker for Linux: Follow the instructions for your specific Linux distribution.

5. **Docker Compose**: Docker Compose is required to manage multi-container applications. Follow the official documentation to install Docker Compose:
   - Docker Compose installation guide: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. To install this repository on your local machine, clone it or download it.

2. Browse to the directory where the wordpress_manager.py script is saved and open a terminal or command prompt.

3. Permissions must be granted to the script in order to execute it. The script may need to be made executable by running the following command:
   ```bash
   chmod +x wordpress_manager.py
   ```
   
4. The script is now ready for use in managing WordPress sites.

## Usage

### Step 1: Make sure dependencies are checked

Check if Docker and Docker Compose are installed on your system before creating a WordPress site. The following command should be run:
```bash
python wordpress_manager.py check
```

### Step 2: Install WordPress on a New Site
Use the following command to create a WordPress site with a LEMP stack:
```bash
python wordpress_manager.py create <site_name>
```
You can replace <site_name> with your desired site name (e.g., mywordpresssite). As a result, a new directory will be created with the given site name and the LEMP stack will be installed inside Docker containers.

### Step 3: Set up a WordPress site
You can enable/start a previously created WordPress site by using the following command:
```bash
python wordpress_manager.py enable <site_name>
```

You should replace <site_name> with the name of the site you want to enable.

### Step 4: Turn off a WordPress site
In order to disable or stop a running WordPress site, use the following command:

```bash
python wordpress_manager.py disable <site_name>
```

You need to replace <site_name> with the name of the site you want to disable.


### Step 5: The process of deleting a WordPress site
Use the following command to delete an existing WordPress site (including containers and local files):
```bash
python wordpress_manager.py delete <site_name>
```
You will have to replace <site_name> with the name of the site you want to delete.

## Resolving problems
During the running of the script, you may encounter the following issues:
- Follow the prerequisite installation steps and make sure that Docker and Docker Compose have been installed on your system.
- It is important to ensure that the wordpress_manager.py script has the appropriate permissions to run.
- Run the script with administrator privileges when necessary (for example, when adding entries to the hosts file) if you are using Windows.

## Lastly
The Python script provides a command-line interface for managing WordPress sites using Docker and the LEMP stack. By handling Docker-related tasks and configurations, the script makes it easy to create, enable, disable, and delete WordPress sites.


