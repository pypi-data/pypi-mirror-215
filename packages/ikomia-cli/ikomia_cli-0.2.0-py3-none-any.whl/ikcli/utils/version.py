"""Parse and manipulate version."""
import re


class Version:
    """A version object to manage, validate or compare versions."""

    # TODO: from ikscale.utils.version. Integrate it to iktools

    def __init__(self, version: str):
        """
        Initialize a new version.

        Args:
            version: Version as str
        """
        p_version = self.__class__._parse(version)

        self.major = p_version["major"]
        self.minor = p_version["minor"]
        self.patch = p_version["patch"]
        self.release = p_version["release"]
        self.metadata = p_version["metadata"]

    def __hash__(self) -> int:
        """
        Hash Version object to use it as dict key.

        Returns:
            A hash of version object
        """
        return hash((self.major, self.minor, self.patch, self.release, self.metadata))

    def __repr__(self) -> str:
        """
        Return a human readable representation of version.

        Returns:
            A str to represent version
        """
        v = f"{self.major}.{self.minor}"
        if self.patch is not None:
            v += f".{self.patch}"
        if self.release is not None:
            v += f"-{self.release}"
        if self.metadata is not None:
            v += f"+{self.metadata}"
        return v

    @classmethod
    def _parse(cls, version: str) -> dict:
        """
        Parse version and return dict for each version member (ie major / minor / patch / release and metadata).

        Args:
            version: Version to parse

        Returns:
            A dict that contains an entry for each version member

        Raises:
            ValueError: If version is not semver compatible
        """
        m = re.match(
            r"^(?P<major>\d+)\.(?P<minor>\d+)(\.(?P<patch>\d+))?"
            r"(-(?P<release>[0-9a-zA-Z-\.]+))?(\+(?P<metadata>[0-9a-zA-Z-\.]+))?$",
            version,
        )
        if m is None:
            raise ValueError(f"'{version}' is not a valid version")
        groupdict = m.groupdict()
        return {
            "major": int(groupdict["major"]),
            "minor": int(groupdict["minor"]),
            "patch": None if groupdict["patch"] is None else int(groupdict["patch"]),
            "release": groupdict["release"],
            "metadata": groupdict["metadata"],
        }

    def _cmp(self, other) -> int:
        """
        Compare two versions.

        Args:
            other: An other version

        Returns:
            A int as result. 0 is equals, <0 if other is greater, >0 if other is less.

        Raises:
            TypeError: If other is not a version object
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can't compare version and {other.__class__}")

        # Compare major
        if self.major > other.major:
            return 1
        if self.major < other.major:
            return -1

        # Compare minor
        if self.minor > other.minor:
            return 1
        if self.minor < other.minor:
            return -1

        # Special case : patch to None is same than 0
        sp = 0 if self.patch is None else self.patch
        op = 0 if other.patch is None else other.patch

        if sp > op:
            return 1
        if sp < op:
            return -1

        # Compare release. If they are None, versions are equals
        if self.release is None and other.release is None:
            return 0

        # If one has no release but the other has, it's greater
        if self.release is None:
            return 1
        if other.release is None:
            return -1

        # Both have release.
        # Use a simple alpha order to know which one is greater
        # It's not fully semver compatible,
        # but really simpler and functional most of the time.
        if self.release > other.release:
            return 1
        return -1

    def __eq__(self, other) -> bool:
        """
        Return True if versions are equals.

        Args:
            other: An other version

        Returns:
            True if equals
        """
        return self._cmp(other) == 0

    def __lt__(self, other):
        """
        Test if this version is less than an other.

        Args:
            other: An other version

        Returns:
            True if less than other
        """
        return self._cmp(other) == -1

    def __le__(self, other):
        """
        Test if this version is less or equals than an other.

        Args:
            other: An other version

        Returns:
            True if less or equals than other
        """
        return self._cmp(other) <= 0

    def __gt__(self, other):
        """
        Test if this version is greater than another.

        Args:
            other: An other version

        Returns:
            True if greater
        """
        return self._cmp(other) == 1

    def __ge__(self, other):
        """
        Test if this version is greater or equals than another.

        Args:
            other: An other version

        Returns:
            True if greater or equals
        """
        return self._cmp(other) >= 0
