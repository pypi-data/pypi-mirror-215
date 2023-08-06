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

import click
import yaml

from flook.module.logger import Logger
from flook.module.database import Database
from flook.module.output import Output
from flook.module.config import Config
from flook.module.file_system import FileSystem


class Recipes:
    """Recipes Class"""

    def __init__(self):
        self.output = Output()
        self.database = Database()
        self.config = Config()
        self.file_system = FileSystem()
        self.logger = Logger().get_logger(__name__)

    def init(self):
        """Init database and configs"""
        self._configs = self.config.load()
        self.database.connect(self._configs["database"]["path"])
        self.database.migrate()
        return self

    def add(self, name, configs):
        """Add a Recipe"""
        recipe = ""
        templates = []

        if self.database.get_recipe(name) is not None:
            raise click.ClickException(f"Recipe with name {name} exists")

        if self.file_system.file_exists("{}/recipe.yml".format(configs["path"])):
            recipe = self.file_system.read_file("{}/recipe.yml".format(configs["path"]))

        if self.file_system.file_exists("{}/recipe.yaml".format(configs["path"])):
            recipe = self.file_system.read_file(
                "{}/recipe.yaml".format(configs["path"])
            )

        data = yaml.load(recipe, Loader=yaml.Loader)

        if "templates" in data.keys():
            for k, v in data["templates"].items():
                if self.file_system.file_exists("{}/{}".format(configs["path"], v)):
                    templates.append(
                        {
                            k: self.file_system.read_file(
                                "{}/{}".format(configs["path"], v)
                            )
                        }
                    )

        self.database.insert_recipe(
            name, {"recipe": recipe, "templates": templates, "tags": configs["tags"]}
        )

        click.echo(f"Recipe with name {name} got created")

    def list(self, tag, output):
        """List Recipes"""
        data = []
        result = self.database.list_recipes()

        for item in result:
            if tag != "" and tag not in item["config"]["tags"]:
                continue

            data.append(
                {
                    "Name": item["name"],
                    "Tags": ", ".join(item["config"]["tags"])
                    if len(item["config"]["tags"]) > 0
                    else "-",
                    "Created at": item["createdAt"],
                }
            )

        if len(data) == 0:
            raise click.ClickException(f"No recipes found!")

        print(
            self.output.render(
                data, Output.JSON if output.lower() == "json" else Output.DEFAULT
            )
        )

    def get(self, name, output):
        """Get Recipe"""
        result = self.database.get_recipe(name)

        if result is None:
            raise click.ClickException(f"Recipe with name {name} not found")

        data = [
            {
                "Name": name,
                "Tags": ", ".join(result["tags"]) if len(result["tags"]) > 0 else "-",
                "Created at": result["createdAt"],
            }
        ]

        print(
            self.output.render(
                data, Output.JSON if output.lower() == "json" else Output.DEFAULT
            )
        )

    def delete(self, name):
        """Delete a Recipe"""
        self.database.delete_recipe(name)
        click.echo(f"Recipe with name {name} got deleted")
