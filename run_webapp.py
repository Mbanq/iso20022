#!/usr/bin/env python3
"""
Run script for the ISO20022 Message Generator Web Application.
This script makes it easy to start the web application from the root directory.
"""

import os
import sys
import subprocess
import importlib.util
import pkg_resources

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['flask', 'werkzeug', 'xmltodict']
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
    
    if missing_packages:
        print("The following dependencies are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nYou can install them using:")
        print("  pip install -e .[webapp]")
        print("  or")
        print("  pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Run the web application."""
    webapp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp')
    app_path = os.path.join(webapp_dir, 'app.py')
    
    # Make sure the app.py file exists
    if not os.path.exists(app_path):
        print(f"Error: Web application not found at {app_path}")
        sys.exit(1)
    
    # Check if dependencies are installed
    if not check_dependencies():
        response = input("\nDo you want to install the missing dependencies now? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.[webapp]'])
                print("Dependencies installed successfully!")
            except subprocess.CalledProcessError:
                print("Failed to install dependencies. Please install them manually.")
                sys.exit(1)
        else:
            print("Please install the missing dependencies and try again.")
            sys.exit(1)
    
    # Run the web application
    print("Starting ISO20022 Message Generator Web Application...")
    print("Access the application at http://localhost:8888")
    subprocess.run([sys.executable, app_path], cwd=webapp_dir)

if __name__ == "__main__":
    main()
