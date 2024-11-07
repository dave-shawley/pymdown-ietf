import collections
import csv
import functools
import importlib.resources
import re
import typing
import xml.etree.ElementTree as ET
from collections import abc

import markdown
from markdown import inlinepatterns

HTTPHeader = typing.NewType('HTTPHeader', str)
StatusCode = typing.NewType('StatusCode', int)
RFCLink = typing.NewType('RFCLink', str)


class _ConfigMapping(typing.TypedDict):
    process: bool | None
    overrides: abc.Mapping[str, str]


class _Configuration(typing.TypedDict):
    link_template: str
    rfc: _ConfigMapping
    http_headers: _ConfigMapping


class _IETFMapper:
    def __init__(self) -> None:
        self.link_template = 'https://www.rfc-editor.org/rfc/rfc{rfc}'
        self.header_links: dict[HTTPHeader, RFCLink] = {}

    def process_configuration(
        self, config: _Configuration, md: markdown.Markdown
    ) -> None:
        link = self.link_template = config['link_template']
        self.header_links.update(
            {
                HTTPHeader(header.lower()): RFCLink(link.format(rfc=rfc))
                for rfc, headers in self.header_map.items()
                for header in headers
            }
        )

        process = config['rfc'].get('process', True)
        if process is not None:
            md.inlinePatterns.register(
                IetfProcessor(
                    (
                        r'(?P<skip_text>RFC-?(?P<rfc_num>\d+))'
                        r'(?:-(?P<anchor>[^]]*))?'
                    ),
                    md,
                    self._create_rfc_link if process else self._skip,
                ),
                'ietf-rfc',
                50,
            )

        process = config['http_headers'].get('process', True)
        if process is not None:
            overrides = config['http_headers'].get('overrides', {})
            self.header_links.update(
                {
                    HTTPHeader(n.lower()): RFCLink(v)
                    for n, v in overrides.items()
                }
            )
            md.inlinePatterns.register(
                IetfProcessor(
                    r'HTTP-(?P<skip_text>(?P<header>[A-Za-z][-A-Za-z0-9]+))',
                    md,
                    self._create_header_link if process else self._skip,
                ),
                'http-header',
                50,
            )

    @staticmethod
    def _skip(m: re.Match[str]) -> ET.Element:
        elm = ET.Element('span')
        elm.text = m.groupdict().get('skip_text', m.group(0))
        return elm

    def _create_header_link(self, m: re.Match[str]) -> ET.Element:
        header_name = m.group('header').lower()
        try:
            link = self.header_links[HTTPHeader(header_name)]
        except KeyError:
            elm = ET.Element('span')
        else:
            if '#' not in link:
                link = RFCLink(link + f'#name-{header_name.lower()}')
            elm = ET.Element('a', {'href': link})
        elm.text = header_name.title()
        return elm

    def _create_rfc_link(self, m: re.Match[str]) -> ET.Element:
        rfc_no = int(m.group('rfc_num'))
        elm = ET.Element(
            'a', {'href': self.generate_rfc_link(rfc_no, m.group('anchor'))}
        )
        elm.text = f'RFC-{rfc_no}'
        return elm

    def generate_rfc_link(self, rfc_no: int, anchor: str | None = None) -> str:
        """Return href for RFC-{rfc_no} with optional anchor."""
        link = self.link_template.format(rfc=rfc_no)
        if anchor:
            link = link.removesuffix('#') + f'#{anchor}'
        return link

    @functools.cached_property
    def header_map(self) -> abc.Mapping[int, abc.Set[str]]:
        data = collections.defaultdict(set)
        data_dir = importlib.resources.files(f'{__package__}.data')
        for path in data_dir.iterdir():
            if path.name == 'field-names.csv':
                with path.open('r', encoding='utf-8') as f:
                    rows = csv.DictReader(f)
                    expr = re.compile(r'\[RFC[- ]?(?P<rfc_no>\d+)')
                    for row in rows:
                        if row['Status'] == 'permanent' and (
                            m := expr.match(row['Reference'])
                        ):
                            data[int(m['rfc_no'])].add(
                                row['Field Name'].lower()
                            )
                break
        return data


class IetfLinksExtension(markdown.Extension):
    """Add inlineProcessors for RFC & HTTP header references."""

    config: abc.Mapping[str, list[object]] = {
        'http_headers': [{'process': True}, 'Enable HTTP header links'],
        'rfc': [{'process': True}, 'Enable links to RFCs'],
        'link_template': [
            'https://www.rfc-editor.org/rfc/rfc{rfc}',
            'Template for RFC links',
        ],
    }

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.mapper = _IETFMapper()

    def extendMarkdown(self, md: markdown.Markdown) -> None:  # noqa: N802
        """Add new inline processors to `md`."""
        self.mapper.process_configuration(
            {  # type: ignore[arg-type]
                name: self.getConfig(name)
                for name in ('http_headers', 'link_template', 'rfc')
            },
            md,
        )


class IetfProcessor(inlinepatterns.InlineProcessor):
    """Implements reference rewriting based on config."""

    def __init__(
        self,
        pattern: str,
        md: markdown.Markdown,
        render: typing.Callable[[re.Match[str]], ET.Element],
    ) -> None:
        super().__init__(pattern, md)
        self.render_link = render

    def handleMatch(  # type: ignore[override]  # noqa: D102, N802
        self,
        m: re.Match[str],
        data: str,
    ) -> tuple[ET.Element | str | None, int | None, int | None]:
        if within_hyperlink(m, data):
            return self.render_link(m), m.start() - 1, m.end() + 1
        return None, None, None


def within_hyperlink(m: re.Match[str], data: str) -> bool:
    """Return `true` if the match is contained in square brackets."""
    try:
        before_chr, next_chr = data[m.start() - 1], data[m.end()]
    except IndexError:
        return False
    return (before_chr, next_chr) == ('[', ']')
