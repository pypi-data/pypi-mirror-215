# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Generic generator routines """

from abc import ABC, abstractmethod
from pathlib import Path

from gentle.metadata import MetadataXML


class AbstractGenerator(ABC):
    """ Generic class for metadata generators. """
    _subclasses = []

    @classmethod
    def get_generator_subclasses(cls):
        return cls._subclasses.copy()

    @abstractmethod
    def __init__(self, srcdir: Path):
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        AbstractGenerator._subclasses.append(cls)

    @abstractmethod
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        ...

    @property
    @abstractmethod
    def active(self) -> bool:
        ...
