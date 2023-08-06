"""Tools to create a valid workflow zip archive from workflow.json file."""
import json
import logging
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import BinaryIO

from yarl import URL

logger = logging.getLogger(__name__)


class Archive:
    """Manager archive to send to ikomia service to deploy a workflow."""

    def __init__(self, filename: Path):
        """
        Initialize a new Archive.

        Args:
            filename: workflow filename to process
        """
        with open(filename, "rt", encoding="utf-8") as fh:
            self.workflow = json.load(fh)
        self.temporary_directory = None

    def prepare(self) -> BinaryIO:
        """
        Prepare zip archive to send to service.

        Returns:
            A zip file name
        """
        # Sanity check
        assert self.temporary_directory is None

        # Create temporary directory
        self.temporary_directory = tempfile.TemporaryDirectory(prefix="ikcli-workflow-")  # pylint: disable=R1732

        # Create temporary working directory
        directory = Path(self.temporary_directory.name)
        working_directory = directory / "workdir"
        working_directory.mkdir()

        # Create workflow file
        with open(working_directory / "workflow.json", "wt", encoding="utf-8") as fh:
            json.dump(self.workflow, fh)

        # Add plugins
        self._add_plugins(working_directory)

        # Zip working directory
        zip_filename = directory / "archive.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(working_directory):
                for filename in files:
                    filepath = Path(root, filename)
                    zipf.write(filepath, filepath.relative_to(working_directory))

        # Return zip file name
        return zip_filename

    def __enter__(self):
        """
        When used with ContextManager, prepare zip to send to service.

        Returns:
            A zip file handler
        """
        return self.prepare()

    def cleanup(self):
        """Clean temporary working files and directories."""
        # Sanity check
        assert self.temporary_directory is not None

        # Clean temporary directory
        self.temporary_directory.cleanup()
        self.temporary_directory = None

    def __exit__(self, *exc):
        """
        Cleanup when exit to ContextManager.

        Args:
            *exc: Information related to stack trace
        """
        self.cleanup()

    def _add_plugins(self, directory: Path):
        """
        Parse task list and embed plugins if needed.

        Args:
            directory: Directory to copy plugins

        Raises:
            ValueError: when plugin URL is not supported
        """
        logger.debug("Check to embedded plugins")

        # For each task, check if we have to embed plugin
        for task in self.workflow["tasks"]:
            data = task["task_data"]

            # Extract URL
            if "url" not in data:
                logger.debug("Task %s plugin is internal", data["name"])
            else:
                url = URL(task["task_data"]["url"])
                logger.debug("Task %s plugin is located at %s", data["name"], url)

                if url.scheme == "file":
                    # If URL is file scheme, copy
                    dst = directory / data["name"]
                    logger.debug("Copy plugin from '%s' to '%s'", url.path, dst)
                    shutil.copytree(url.path, dst, ignore=shutil.ignore_patterns(".git"))
                    # Update url
                    data["url"] = "file://" + data["name"]
                else:
                    raise ValueError(f"Plugin url scheme '{url}' is not supported yet")
