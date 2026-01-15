"""
Quick start script for local development
Run this to set up and start the application locally
"""

import os
import subprocess
import sys
import platform


def run_command(cmd, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("STRESS DETECTION - LOCAL DEVELOPMENT SETUP")
    print("=" * 60)
    
    # Check Python version
    print("\n✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        return False
    print(f"✓ Python {sys.version.split()[0]}")
    
    # Check Node version
    print("\n✓ Checking Node.js version...")
    if not run_command("node --version"):
        print("✗ Node.js not found. Please install Node.js 14+")
        return False
    
    # Create virtual environment
    print("\n✓ Creating Python virtual environment...")
    if platform.system() == "Windows":
        venv_activate = "venv\\Scripts\\activate"
        run_command("python -m venv venv")
        run_command("venv\\Scripts\\pip install --upgrade pip")
    else:
        venv_activate = "source venv/bin/activate"
        run_command("python3 -m venv venv")
        run_command("source venv/bin/activate && pip install --upgrade pip")
    
    # Install Python dependencies
    print("\n✓ Installing Python dependencies...")
    if platform.system() == "Windows":
        run_command("venv\\Scripts\\pip install -r requirements.txt")
    else:
        run_command("source venv/bin/activate && pip install -r requirements.txt")
    
    # Install Node dependencies
    print("\n✓ Installing Node.js dependencies...")
    run_command("npm install --legacy-peer-deps", cwd="client")
    
    # Create .env file
    print("\n✓ Creating .env files...")
    if not os.path.exists("server/.env"):
        run_command("copy server\\.env.example server\\.env" if platform.system() == "Windows" 
                   else "cp server/.env.example server/.env")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Start the Flask backend (Terminal 1):")
    print("   cd server && python app.py")
    
    print("\n3. Start the React frontend (Terminal 2):")
    print("   cd client && npm start")
    
    print("\n4. Open browser:")
    print("   Backend:  http://localhost:5000")
    print("   Frontend: http://localhost:3000")
    
    print("\n5. Test the API:")
    print("   curl http://localhost:5000/health")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
