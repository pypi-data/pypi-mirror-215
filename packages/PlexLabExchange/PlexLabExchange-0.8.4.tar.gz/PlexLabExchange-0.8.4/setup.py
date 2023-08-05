from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform
import subprocess
import shutil
import tempfile


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Call parent 
        print("Running post installation script...")
        install.run(self)
        print("Running post installation script after parent install")
        # Determine platform 
        go_bin_url = ""
        system_platform = platform.system()
        print(system_platform)
        machine = platform.machine()
        print(machine)
        if system_platform == "Windows":
            if machine == "AMD64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_windows_amd64.tar.gz"
            elif machine == "i386":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_windows_386.tar.gz"
            elif machine == "ARM64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_windows_arm64.tar.gz"
        elif system_platform == "Linux":
            if machine == "x86_64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_linux_amd64.tar.gz"
            elif machine == "i386":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_linux_386.tar.gz"
            elif machine == "aarch64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_linux_arm64.tar.gz"
        elif system_platform == "Darwin":
            if machine == "x86_64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_darwin_amd64.tar.gz"
            elif machine == "arm64":
                go_bin_url = "https://github.com/labdao/plex/releases/download/v0.8.0/plex_0.8.0_darwin_arm64.tar.gz"
        # Download Go binary to scripts path
        if go_bin_url:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    self.download_and_extract(go_bin_url, temp_dir)

                    # move the binary to the package directory
                    src = os.path.join(temp_dir, 'plex')
                    dst_dir = os.path.join(self.install_lib, 'PlexLabExchange')

                    # Create target Directory if don't exist
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    dst = os.path.join(dst_dir, 'plex')
                    shutil.move(src, dst)
                    # set the binary as executable
                    os.chmod(dst, 0o755)
            except Exception as e:
                print(f"Failed to download and extract the Go binary: {e}")
        else:
            raise RuntimeError(f"The current platform/machine of {system_platform}/{machine} is not supported.")

    def download_and_extract(self, go_bin_url, temp_dir):
        # Note: This assumes that curl and tar are installed on the system
        subprocess.run(f"curl -sSL {go_bin_url} | tar xvz -C {temp_dir}", shell=True, check=True)


setup(
    name="PlexLabExchange",
    version="0.8.4",
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
    author="LabDAO",
    author_email="media@labdao.xyz",
    description="A Python interface to the Plex Go CLI.",
    url="https://github.com/labdao/plex",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="plex golang cli wrapper",
    license="MIT",
    python_requires='>=3.8',
)
