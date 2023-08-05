from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)

        system_platform = platform.system()
        machine = platform.machine()
        go_bin_url = ""
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

        if go_bin_url:
            try:
                self.download_and_extract(go_bin_url)
            except Exception as e:
                raise RuntimeError(f"Failed to download and extract the Go binary: {e}")
        else:
            raise RuntimeError(f"The current platform/machine of {system_platform}/{machine} is not supported.")

    def download_and_extract(self, go_bin_url):
        # Note: This assumes that curl and tar are installed on the system
        subprocess.run(f"curl -sSL {go_bin_url} | tar xvz", shell=True, check=True)


setup(
    name="PlexLabExchange",
    version="0.8.3",
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
