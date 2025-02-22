# Python Virtual Environment Setup

This guide provides instructions on setting up a Python virtual environment and installing the necessary dependencies for working with mapping, QR code generation, and network analysis.

## Prerequisites

Ensure you have Python installed (preferably Python 3.8 or later). You can check your Python version by running:

```bash
python --version
```

If Python is not installed, download and install it from [Python's official website](https://www.python.org/downloads/).

## Setting up the Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to your project directory:

   ```bash
   cd /path/to/your/project
   ```

3. Create a virtual environment named `venv`:

   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```

5. Upgrade `pip` to ensure you have the latest package manager:
   
   ```bash
   pip install --upgrade pip
   ```

## Installing Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install folium networkx osmnx qrcode gmaps googlemaps pillow pyperclip
```

## Verifying the Installation

To ensure that all packages are installed correctly, run the following Python command:

```python
import csv
import folium
import networkx as nx
import osmnx as ox
import qrcode
import gmaps
import googlemaps

print("All packages imported successfully!")
```

If you don't see any errors, the setup is complete!

## Deactivating the Virtual Environment

Once you're done working in the virtual environment, deactivate it with:

```bash
deactivate
```

## Additional Notes

- If you want to store the installed packages in a `requirements.txt` file for future installations, run:
  
  ```bash
  pip freeze > requirements.txt
  ```
  
- To install dependencies from `requirements.txt` in a new environment:
  
  ```bash
  pip install -r requirements.txt
  ```

This ensures that anyone working on the project has the same dependencies installed.

---

Now you are ready to start using Python for mapping, QR code generation, and network analysis!

