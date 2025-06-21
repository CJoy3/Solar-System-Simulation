# Setup Instructions
To get this project up and running on your local machine, follow these steps:

1. Clone the Repository
First, clone the project from GitHub to your local machine:

git clone https://github.com/YourUsername/Solar_Simulation.git
cd Solar_Simulation
(Replace YourUsername with your actual GitHub username.)

2. Create and Activate a Python Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies. This isolates the required Python packages for this project from your global Python installation.

# Create and activate the virtual environment (named '.venv' by convention)
python -m venv .venv

On Windows (Command Prompt / PowerShell):
.venv\Scripts\activate

On Linux / macOS / MSYS2 Bash:
source .venv/bin/activate
You should see (.venv) at the beginning of your terminal prompt, indicating the virtual environment is active.

# Final setup stage

3. Install Dependencies
With the virtual environment active, install all necessary project dependencies using pip:
pip install -r requirements.txt

5. Run the Application
Once all dependencies are installed, you can run the main application. Ensure your terminal's current directory is the project root (Solar_Simulation/).
Run main.py to open the menu screen for the simulation
