import os
import sys
import re
import logging
import shutil
import subprocess
from typing import List


class PackageInfo:
    def __init__(self, line):
        self.name = None
        self.version = None
        splitted_info: List[str] = []
        if "=" in line:
            splitted_info = re.split(r"==", line)  # split name and version in code
        else:
            splitted_info = re.split(r"\s+", line)  # split name and version int pip list files
        self.name = splitted_info[0]
        if len(splitted_info) > 1:
            self.version = splitted_info[1]


class PipControl:
    def __init__(
        self,
        file: str = "",
        packages: List[str] = None,
        run_file: str = None,
        venv_folder: str = "venv",
        venv: bool = False,
        delete: bool = False,
    ) -> None:
        self.cmd = sys.executable
        self.file = file
        self.venv = venv
        self.delete = delete
        self.venv_folder = venv_folder
        self.abs_path = os.path.abspath(file)
        self.abs_dir = os.path.dirname(self.abs_path)
        self.abs_dir_dir = os.path.dirname(self.abs_dir)
        self.pip_path = os.path.join(self.abs_dir, "pip_list.txt")
        self.requirement_path = os.path.join(self.abs_dir, "requirements.txt")
        self.venv_path = os.path.join(self.abs_dir, self.venv_folder)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python3")
        elif sys.platform == "darwin":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python3")
        elif sys.platform == "win32":
            self.cmd_venv = os.path.join(self.venv_path, "bin", "python")

        self.package_infos_installed: List[PackageInfo] = []
        self.package_infos_input: List[PackageInfo] = []
        self.categarized = False
        self.install_packages: List[PackageInfo] = []
        self.update_packages: List[PackageInfo] = []
        self.installed_packages: List[PackageInfo] = []

        logging.basicConfig(level=logging.INFO)

        if packages:
            self.install(packages)
        if run_file:
            self.run(run_file)

    def __enter__(self):
        if self.venv:
            self.setup_venv()
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            logging.error(f"{type} | {value} | {traceback}")
            return False
        else:
            logging.getLogger().handlers = []
            if self.delete:
                self.delete_venv()
            return True

    def console_no_output(self, command: List[str]):
        try:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logging.error(e)

    def setup_venv(self):
        logging.info(f"setup virtual environment ./{self.venv_folder}")
        self.console_no_output([self.cmd, "-m", "venv", self.venv_path])
        self.cmd = self.cmd_venv
        self.console_no_output([self.cmd, "-m", "pip", "install", "--upgrade", "pip"])

    def delete_venv(self):
        logging.info(f"delete virtual environment ./{self.venv_folder}")
        if os.path.exists(self.venv_path):
            shutil.rmtree(self.venv_path)

    def run(self, file_name: str = ""):
        """Run python in virtual environment"""
        if file_name == os.path.basename(file_name):
            file_path = os.path.join(self.abs_dir, os.path.basename(file_name))
        elif file_name == os.path.abspath(file_name):
            file_path = file_name
        else:
            logging.error("wrong file name or path")
        os.system(f"{self.cmd} {file_path}")

    def get_package_infos_installed(self):
        command = [self.cmd, "-m", "pip", "list"]
        with open(self.pip_path.replace(" ", "\ "), "w") as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.DEVNULL, check=True)
        with open(f"{self.pip_path}", "r", encoding="utf-8-sig") as f:
            self.package_lines = f.readlines()
        for line in self.package_lines:
            self.package_infos_installed.append(PackageInfo(line))
        os.remove(f"{self.pip_path}")

    def get_package_infos_code(self, packages: List[str]):
        for package in packages:
            self.package_infos_input.append(PackageInfo(package))

    @staticmethod
    def normalize_string(string: str):
        string = string.lower()
        string = re.sub(r"[-_]", "", string)
        return string

    def compare_strings(self, string1, string2):
        normalized_str1 = self.normalize_string(string1)
        normalized_str2 = self.normalize_string(string2)
        return normalized_str1 == normalized_str2

    def show_categorized_packages(self):
        if self.install_packages:
            logging.info(f"intall {[p.name for p in self.install_packages]}")
        if self.update_packages:
            logging.info(f"update {[p.name for p in self.update_packages]}")
        if self.installed_packages:
            logging.info(f"installed {[p.name for p in self.installed_packages]}")

    def initialize_list(self):
        self.install_packages.clear()
        self.update_packages.clear()
        self.installed_packages.clear()
        self.package_lines.clear()
        self.package_infos_input.clear()
        self.package_infos_installed.clear()

    def categorizing_logic(self, packages: List[str]):
        logging.debug("categorizing logic")
        if not self.categarized:
            self.get_package_infos_installed()
            self.get_package_infos_code(packages)
            for package_input in self.package_infos_input:
                check_intalled = False
                for package_installed in self.package_infos_installed:
                    if self.compare_strings(package_installed.name, package_input.name):
                        check_intalled = True
                        break
                if check_intalled:
                    if package_input.version:
                        if package_input.version in package_installed.version:
                            self.installed_packages.append(package_input)
                        else:
                            self.install_packages.append(package_input)
                            self.update_packages.append(package_input)
                    else:
                        self.installed_packages.append(package_input)
                else:
                    self.install_packages.append(package_input)
            self.categarized = True
        self.show_categorized_packages()

    def categorize_packages(self, packages: List[str]):
        logging.debug("categorize packages to install, update, installed list")
        self.categorizing_logic(packages)

    def recategorize_package(self, packages: List[str]):
        logging.debug("recategorize packages to check")
        self.initialize_list()
        self.categarized = False
        self.categorizing_logic(packages)

    def install(self, packages: List[str]):
        self.categorize_packages(packages)
        for package_info in self.install_packages:
            if package_info.version is None:
                package = package_info.name
            else:
                package = f"{package_info.name}=={package_info.version}"
            logging.debug(f"install package [{package}]")
            self.console_no_output([self.cmd, "-m", "pip", "install", package])
        self.recategorize_package(packages)

    def update(self, packages: List[str]):
        self.categorize_packages(packages)
        for package_info in self.update_packages:
            if package_info.version is None:
                package = package_info.name
            else:
                package = f"{package_info.name}=={package_info.version}"
            logging.debug(f"update package [{package}]")
            self.console_no_output([self.cmd, "-m", "pip", "install", "--upgrade", package])
        self.recategorize_package(packages)

    def uninstall(self, packages: List[str]):
        self.categorize_packages(packages)
        for package_info in self.installed_packages:
            if package_info.version is None:
                package = package_info.name
            else:
                package = f"{package_info.name}=={package_info.version}"
            logging.debug(f"uninstall package [{package}]")
            self.console_no_output([self.cmd, "-m", "pip", "uninstall", "-y", package])
        self.recategorize_package(packages)

    def requirement_install(self):
        command = [self.cmd, "-m", "pip", "install", "-r", self.requirement_path]
        logging.info("install requirement.txt")
        self.console_no_output(command)

    def requirement_unistall(self):
        command = [self.cmd, "-m", "pip", "uninstall", "-y", "-r", self.requirement_path]
        logging.info("uninstall requirement.txt")
        self.console_no_output(command)

    def requirement_freeze(self):
        logging.info("freeze requirement.txt")
        command = [self.cmd, "-m", "pip", "freeze"]
        with open(self.requirement_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, check=True)


if __name__ == "__main__":
    # list of packages
    packages = ["python-crontab", "requests", "psutil", "selenium==4.8"]

    # fuctions
    # pipcontrol = PipControl(__file__)
    # pipcontrol.install(packages)
    # pipcontrol.update(packages)
    # pipcontrol.uninstall(packages)
    # pipcontrol.requirement_freeze()
    # pipcontrol.requirement_install()
    # pipcontrol.requirement_unistall()

    # Run in global python evironment 1
    with PipControl(__file__) as pip1:
        pip1.install(packages)

    # # Run in global python evironment 2
    # with PipControl(__file__, packages, "test.py test2"):
    #     pass  # install packages and run file in __init__

    # Run in venv1
    # ! Run in virtual environment python
    pipv_1 = PipControl(__file__, venv_folder="venv1")
    pipv_1.setup_venv()
    pipv_1.install(packages)
    pipv_1.run("test.py venv_test1")
    pipv_1.delete_venv()

    # Run in venv2
    with PipControl(__file__, venv_folder="venv2", venv=True) as pipv_2:
        pipv_2.install(packages)
        pipv_2.run("test.py venv_test2")

    # Run in venv3
    with PipControl(__file__, packages, "test.py venv_test3", "venv3", True):
        pass
