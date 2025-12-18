#!/usr/bin/env python3
"""
Test runner script for the High School Management System API
"""
import subprocess
import sys

def main():
    """Run pytest with verbose output"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]
    result = subprocess.run(cmd, cwd="/workspaces/skills-getting-started-with-github-copilot")
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
