# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Generic metadata parsing structures and routines """

import logging
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional

logger = logging.getLogger("metadata")


@dataclass
class Person:
    name: str = field(default="", compare=False)
    email: str = ""

    def to_xml(self, attrib: Optional[dict] = None) -> ET.Element:
        """
        :param attrib: attributes for the ``<maintainer>`` tag
        :return: :file:`metadata.xml` respresentation of a person
        """
        result = ET.Element("maintainer", attrib=attrib or {})
        if self.name:
            name_elem = ET.SubElement(result, "name")
            name_elem.text = self.name
        if self.email:
            email_elem = ET.SubElement(result, "email")
            email_elem.text = self.email

        return result


@dataclass
class RemoteID:
    attr: str
    value: str

    def to_xml(self) -> ET.Element:
        """
        :return: :file:`metadata.xml` respresentation of a remote id
        """
        remote_elem = ET.Element("remote-id", type=self.attr)
        remote_elem.text = self.value
        return remote_elem


@dataclass
class Upstream:
    maintainers: list[Person] = field(default_factory=list)
    changelog: Optional[str] = None
    doc: Optional[str] = None
    bugs_to: Optional[str] = None
    remote_ids: list[RemoteID] = field(default_factory=list)


class MetadataXML:
    """ Parse and write :file:`metadata.xml` files. """

    def __init__(self, xmlfile: Path):
        """
        :param xmlfile: path to the :file:`metadata.xml` file
        """
        self.xmlfile: Path = xmlfile
        self.xml: ET.ElementTree = ET.parse(self.xmlfile)

        self._maintainers: list[Person] = []
        self._upstream = Upstream()
        self._parse_metadata_xml()

    @property
    def maintainers(self) -> list[Person]:
        """ List of package maintainers """
        return self._maintainers.copy()

    @property
    def upstream(self) -> Upstream:
        """ Upstream information """
        return replace(self._upstream)

    def dump(self) -> None:
        """ Write :file:`metadata.xml` file """
        logger.info("Writing metadata.xml")
        ET.indent(self.xml, space="\t", level=0)
        with open(self.xmlfile, "w") as file:
            file.write(textwrap.dedent("""\
                <?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE pkgmetadata SYSTEM "https://www.gentoo.org/dtd/metadata.dtd">
            """))
            self.xml.write(file, encoding="unicode")
            file.write("\n")

    def dumps(self) -> str:
        """ Convert the object to text """
        ET.indent(self.xml, space="\t", level=0)
        return ET.tostring(self.xml.getroot(), encoding="unicode")

    def add_upstream_maintainer(self, person: Person) -> None:
        """ Add a person to the list of upstream maintainers """
        if person in self._upstream.maintainers:
            return

        logger.info("Adding upstream maintainer: %s", person)
        self._upstream.maintainers.append(person)
        upstream = self._make_upstream_element()
        upstream.append(person.to_xml())

    def add_upstream_remote_id(self, remote_id: RemoteID) -> None:
        """ Add an item to the list of remote ids """
        if remote_id in self._upstream.remote_ids:
            return

        logger.info("Adding remote id: %s", remote_id)
        self._upstream.remote_ids.append(remote_id)
        upstream = self._make_upstream_element()
        upstream.append(remote_id.to_xml())

    def set_upstream_bugs_to(self, url: str) -> None:
        """ Set upstream bugs-to URL """
        if self._upstream.bugs_to:
            return

        logger.info("Setting upstream bug tracker to %s", url)
        self._upstream.bugs_to = url

        upstream = self._make_upstream_element()
        bugs_to = ET.SubElement(upstream, "bugs-to")
        bugs_to.text = url

    def set_upstream_changelog(self, url: str) -> None:
        """ Set upstream changelog URL """
        if self._upstream.changelog:
            return

        logger.info("Setting upstream changelog to %s", url)
        self._upstream.changelog = url

        upstream = self._make_upstream_element()
        changelog = ET.SubElement(upstream, "changelog")
        changelog.text = url

    def set_upstream_doc(self, url: str) -> None:
        """ Set upstream documentation URL """
        if self._upstream.doc:
            return

        logger.info("Setting upstream documentation to %s", url)
        self._upstream.doc = url

        upstream = self._make_upstream_element()
        doc = ET.SubElement(upstream, "doc")
        doc.text = url

    def _make_upstream_element(self) -> ET.Element:
        if (upstream := self.xml.find("upstream")) is None:
            pkgmetadata = self.xml.getroot()
            upstream = ET.SubElement(pkgmetadata, "upstream")
        return upstream

    def _parse_metadata_xml(self) -> None:
        """ Parse the :file:`metadata.xml` file """
        assert self.xml.getroot().tag == "pkgmetadata"

        for maint in self.xml.findall("maintainer"):
            self._parse_package_maintainer(maint)

        if (upstream := self.xml.find("upstream")) is not None:
            self._parse_upstream(upstream)

    def _parse_person(self, xml: ET.Element, *, name_optional: bool = False,
                      email_optional: bool = False) -> Optional[Person]:
        """
        :param xml: ``<maintainer>`` XML tag
        """
        assert xml.tag == "maintainer"

        if (email_tag := xml.find("email")) is not None:
            email = "".join(email_tag.itertext())
        elif email_optional:
            email = None
        else:
            return None

        if (name_tag := xml.find("name")) is not None:
            name = "".join(name_tag.itertext())
        elif name_optional:
            name = None
        else:
            return None

        return Person(name or "", email or "")

    def _parse_package_maintainer(self, xml: ET.Element) -> None:
        """
        :param xml: top-level ``<maintainer>`` XML tag
        """
        if (person := self._parse_person(xml, name_optional=True)) is not None:
            self._maintainers.append(person)

    def _parse_upstream(self, xml: ET.Element) -> None:
        """
        :param xml: ``<upstream>`` XML tag
        """
        assert xml.tag == "upstream"

        for maint in xml.findall("maintainer"):
            if (person := self._parse_person(maint, email_optional=True)) is not None:
                self._upstream.maintainers.append(person)

        for remote in xml.findall("remote-id"):
            attr = remote.get("type", "unknown")
            value = "".join(remote.itertext())
            self._upstream.remote_ids.append(RemoteID(attr, value))

        if (changelog := xml.find("changelog")) is not None:
            self._upstream.changelog = "".join(changelog.itertext())

        if (doc := xml.find("doc")) is not None:
            self._upstream.doc = "".join(doc.itertext())

        if (bugs_to := xml.find("bugs-to")) is not None:
            self._upstream.bugs_to = "".join(bugs_to.itertext())
