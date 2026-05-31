# Python 3.12 Installation Guide with UV

This guide explains how to install Python 3.12 using UV (a fast Python package installer and resolver) on your operating system.

## What is UV?

UV is a fast, Rust-based Python package installer that's compatible with pip. It's significantly faster than pip and provides better dependency resolution.

## Installation Instructions

### macOS

1. **Install UV using Homebrew:**
   ```bash
   brew install uv
   ```

2. **Install Python 3.12:**
   ```bash
   # Install latest 3.12 patch version
   uv python install 3.12
   
   # Or install a specific version (e.g., 3.12.13)
   uv python install 3.12.13
   ```

3. **Verify installation:**
   ```bash
   python3.12 --version
   ```
   
   **Note:** Not all Python versions are available through UV. If you encounter issues, try installing a specific patch version like `3.12.13`.

### Windows

1. **Install UV using Windows Package Manager or pip:**
   ```bash
   # Using Windows Package Manager (if installed)
   winget install astral.uv
   
   # Or using pip
   pip install uv
   ```

2. **Install Python 3.12:**
   ```bash
   # Install latest 3.12 patch version
   uv python install 3.12
   
   # Or install a specific version (e.g., 3.12.13)
   uv python install 3.12.13
   ```

3. **Verify installation:**
   ```bash
   python3.12 --version
   ```
   
   **Note:** Not all Python versions are available through UV. If you encounter issues, try installing a specific patch version like `3.12.13`.

### Linux (Ubuntu/Debian)

1. **Install UV:**
   ```bash
   # Using curl
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or using apt (if available)
   apt-get install uv
   ```

2. **Install Python 3.12:**
   ```bash
   # Install latest 3.12 patch version
   uv python install 3.12
   
   # Or install a specific version (e.g., 3.12.13)
   uv python install 3.12.13
   ```

3. **Verify installation:**
   ```bash
   python3.12 --version
   ```
   
   **Note:** Not all Python versions are available through UV. If you encounter issues, try installing a specific patch version like `3.12.13`.

### Linux (Fedora/RHEL)

1. **Install UV:**
   ```bash
   sudo dnf install uv
   ```

2. **Install Python 3.12:**
   ```bash
   # Install latest 3.12 patch version
   uv python install 3.12
   
   # Or install a specific version (e.g., 3.12.13)
   uv python install 3.12.13
   ```

3. **Verify installation:**
   ```bash
   python3.12 --version
   ```
   
   **Note:** Not all Python versions are available through UV. If you encounter issues, try installing a specific patch version like `3.12.13`.

## Using UV in this Project

Once Python 3.12 is installed with UV, you can:

1. **Create a virtual environment:**
   ```bash
   # Default (creates .venv directory)
   uv venv --python 3.12
   
   # Custom name (e.g., my_env, env, venv_fastapi)
   uv venv --python 3.12 my_env
   ```

2. **Activate the virtual environment:**
   ```bash
   # Default (.venv)
   # macOS/Linux
   source .venv/bin/activate
   
   # Windows
   .venv\Scripts\activate
   
   # Custom name (e.g., my_env)
   # macOS/Linux
   source my_env/bin/activate
   
   # Windows
   my_env\Scripts\activate
   ```

3. **Install project dependencies:**
   
   **Note:** Make sure you're in the project root directory before running this command.
   
   ```bash
   uv pip install -r requirements.txt
   ```

## Troubleshooting

- **UV not found after installation?** Make sure your PATH includes the UV installation directory and restart your terminal.
- **Wrong Python version?** Run `uv python install 3.12 --force` to reinstall, or try a specific patch version like `3.12.13`.
- **Version not available?** Not all Python versions are available through UV. Try specifying a specific patch version (e.g., `3.12.13`, `3.12.0`) or check UV's available versions with `uv python list`.
- **Permission denied on Linux?** You may need to use `sudo` for system-wide installation.

## Available Python Versions

To see all available Python versions for installation:
```bash
uv python list
```

## Next Steps

Once you have Python 3.12 installed with UV, follow the project setup instructions in the README.md file.
