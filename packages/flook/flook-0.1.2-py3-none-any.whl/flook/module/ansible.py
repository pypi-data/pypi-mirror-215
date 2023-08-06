# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ansible_runner

from flook.module.logger import Logger
from flook.module.file_system import FileSystem


class Ansible:
    """Ansible Module"""

    def __init__(self):
        self.file_system = FileSystem()
        self.logger = Logger().get_logger(__name__)

    def run(self, data_dir, playbook, inventory):
        """
        Run Ansible Playbook
        """
        out = ansible_runner.run(
            private_data_dir=data_dir,
            playbook=playbook,
            inventory=inventory,
            quiet=True,
        )

        if out.status.lower() == "failed":
            return False

        elif out.status.lower() == "successful":
            return True

        return False

    def cleanup(self, path):
        """
        Cleanup Plan Directory
        """
        try:
            self.file_system.delete_directory(path)
        except Exception:
            pass
