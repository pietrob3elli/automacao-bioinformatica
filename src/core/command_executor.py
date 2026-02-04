"""
Command executor module for running shell commands.

This module provides a safe and robust way to execute shell commands
for bioinformatics tools like FastQC, SPAdes, and other analysis tools.
"""

import logging
import subprocess
import shlex
from typing import Dict, List, Optional, Tuple
from pathlib import Path


logger = logging.getLogger(__name__)


class CommandExecutor:
    """
    Execute shell commands with proper error handling and logging.
    
    This class provides methods to run external bioinformatics tools
    safely using the subprocess module.
    """
    
    def __init__(self, working_dir: Optional[Path] = None):
        """
        Initialize the CommandExecutor.
        
        Args:
            working_dir: Optional working directory for command execution.
                        If None, uses current directory.
        """
        self.working_dir = working_dir or Path.cwd()
        logger.info(f"CommandExecutor initialized with working directory: {self.working_dir}")
    
    def run_command(
        self,
        command: str,
        timeout: Optional[int] = None,
        check: bool = True,
        capture_output: bool = True
    ) -> Tuple[int, str, str]:
        """
        Execute a shell command and return its output.
        
        Args:
            command: The command to execute as a string.
            timeout: Optional timeout in seconds.
            check: If True, raises an exception on non-zero exit code.
            capture_output: If True, captures stdout and stderr.
        
        Returns:
            A tuple of (return_code, stdout, stderr).
        
        Raises:
            subprocess.CalledProcessError: If check=True and command fails.
            subprocess.TimeoutExpired: If command exceeds timeout.
        
        Example:
            >>> executor = CommandExecutor()
            >>> code, out, err = executor.run_command("echo 'Hello'")
            >>> print(out.strip())
            Hello
        """
        logger.info(f"Executing command: {command}")
        
        try:
            # Parse command safely
            cmd_list = shlex.split(command)
            
            # Execute command
            result = subprocess.run(
                cmd_list,
                cwd=self.working_dir,
                timeout=timeout,
                check=check,
                capture_output=capture_output,
                text=True
            )
            
            logger.info(f"Command completed with return code: {result.returncode}")
            
            return (
                result.returncode,
                result.stdout if capture_output else "",
                result.stderr if capture_output else ""
            )
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with return code {e.returncode}: {e.stderr}")
            raise
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out after {timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"Unexpected error executing command: {str(e)}")
            raise
    
    def run_command_async(
        self,
        command: str,
        stdout_file: Optional[Path] = None,
        stderr_file: Optional[Path] = None
    ) -> subprocess.Popen:
        """
        Execute a command asynchronously.
        
        Args:
            command: The command to execute.
            stdout_file: Optional file to redirect stdout.
            stderr_file: Optional file to redirect stderr.
        
        Returns:
            A Popen object representing the running process.
        
        Note:
            When using file redirection, files are opened and will be
            automatically closed when the process terminates and its
            stdout/stderr attributes are garbage collected.
        
        Example:
            >>> executor = CommandExecutor()
            >>> process = executor.run_command_async("long_running_task")
            >>> # Do other work...
            >>> exit_code = process.wait()
        """
        logger.info(f"Starting async command: {command}")
        
        cmd_list = shlex.split(command)
        
        # Set up file handles - will be closed when process is garbage collected
        stdout_handle = subprocess.PIPE
        stderr_handle = subprocess.PIPE
        
        if stdout_file:
            stdout_handle = open(stdout_file, 'w')
        if stderr_file:
            stderr_handle = open(stderr_file, 'w')
        
        try:
            process = subprocess.Popen(
                cmd_list,
                cwd=self.working_dir,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True
            )
            
            logger.info(f"Process started with PID: {process.pid}")
            return process
            
        except Exception as e:
            # Clean up file handles if process creation fails
            if stdout_file and stdout_handle != subprocess.PIPE:
                stdout_handle.close()
            if stderr_file and stderr_handle != subprocess.PIPE:
                stderr_handle.close()
            logger.error(f"Failed to start async command: {str(e)}")
            raise
    
    def check_tool_available(self, tool_name: str) -> bool:
        """
        Check if a bioinformatics tool is available in the system PATH.
        
        Args:
            tool_name: Name of the tool to check (e.g., 'fastqc', 'spades.py').
        
        Returns:
            True if the tool is available, False otherwise.
        
        Example:
            >>> executor = CommandExecutor()
            >>> if executor.check_tool_available('fastqc'):
            ...     print("FastQC is installed")
        """
        try:
            result = subprocess.run(
                ["which", tool_name],
                capture_output=True,
                text=True,
                check=False
            )
            available = result.returncode == 0
            
            if available:
                logger.info(f"Tool '{tool_name}' is available at: {result.stdout.strip()}")
            else:
                logger.warning(f"Tool '{tool_name}' is not available in PATH")
            
            return available
        except Exception as e:
            logger.error(f"Error checking tool availability: {str(e)}")
            return False
    
    def get_tool_version(self, tool_name: str, version_flag: str = "--version") -> Optional[str]:
        """
        Get the version of a bioinformatics tool.
        
        Args:
            tool_name: Name of the tool.
            version_flag: Flag to get version (default: --version).
        
        Returns:
            Version string if available, None otherwise.
        
        Example:
            >>> executor = CommandExecutor()
            >>> version = executor.get_tool_version('fastqc')
            >>> print(f"FastQC version: {version}")
        """
        try:
            command = f"{tool_name} {version_flag}"
            code, stdout, stderr = self.run_command(command, check=False)
            
            version_output = stdout + stderr
            logger.info(f"Tool '{tool_name}' version info: {version_output.strip()}")
            
            return version_output.strip()
        except Exception as e:
            logger.error(f"Error getting tool version: {str(e)}")
            return None
