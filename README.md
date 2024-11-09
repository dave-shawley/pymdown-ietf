# Referencing IETF sources

> links to RFCs with a simple syntax -- `[RFC-9110]` and `[RFC-2045-section-5.1]` \
> links to HTTP headers regardless of current RFC that defines it -- `[HTTP-Accept]`

I wrote this simple extension when I was converting my [ietfparse] project from sphinx
to mkdocs. It's documentation suite contains **a lot** of references to RFCs and HTTP
headers. Sphinx supports referencing RFCs using [`:rfc:`] natively. The
[sphinxcontrib-httpdomain] package adds support for HTTP headers and status codes
using `:http:`. I wanted to bring this to mkdocs so that I didn't need to
continuously add local references to RFCs.

[ietfparse]: https://pypi.org/project/ietfparse
[`:rfc:`]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-rfc
[sphinxcontrib-httpdomain]: https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/

## Usage

This is the simple part. This extension recognizes two _reference style_ link patterns
and converts them to hyperlinks.

| Markdown Text            | Generated HTML                                                            |
|--------------------------|---------------------------------------------------------------------------|
| `[RFC-9110]`             | `<a href="https://www.rfc-editor.org/rfc/rfc9110">RFC-9110</a>`           |
| `[RFC-9110-name-accept]` | `<a href="https://www.rfc-editor.org/rfc/rfc9110#name-accept">Accept</a>` |
| `[HTTP-Accept]`          | `<a href="https://www.rfc-editor.org/rfc/rfc9110#name-accept">Accept</a>` |

I haven't created a syntax that lets you control the link text yet. I may in the future but
this met my immediate need.

## Configuration

Simply add the library to your environment using your chosen package management
mechanism. I use [hatch], so my _pyproject.toml_ contains:

```toml
[tool.hatch.envs.default]
dependencies = [ "ietflinks", "mkdocs" ]
```

Then add `ietflinks` as a Markdown extension in your _mkdocs.yml_.

```yaml
markdown_extensions:
  - ietflinks
```

That's it! A surprising bonus is that you don't have to think about the finer points
of referencing IETF documents like which URL template to use for RFCs -- _if you
know what I am talking about, then you will appreciate this feature_. It also takes
care of knowing which RFC currently defines which HTTP header.

### Customization

Since the Internet is always changing, you can add support for new HTTP headers or
even override what I chose by default directly in your configuration file.

```yaml
markdown_extension:
  - ietflinks:
    http_headers:
      overrides:
        content-md5: "https://www.rfc-editor.org/rfc/rfc2616.html#section-14.15"
```

You can also change the URL template if you find a reason to. It defaults to
`https://www.rfc-editor.org/rfc/rfc{rfc}`. The `{rfc}` parameter is replaced by the
RFC number.

```yaml
markdown_extensions:
  - ietflinks:
    link_template: "https://tools.ietf.org/html/rfc{rfc}"
```

You can also disable processing of either syntax by setting the `process` property to `false`.

```yaml
markdown_extensions:
  - ietflinks:
    rfc:
      process: false
```

When a reference style is disabled, the reference is replaced by its text without the brackets.
So `[RFC-9110]` would be replaced by `<span>RFC-9110</span>`. You can enable pure passthrough
functionality by setting `process` to `null`.

A json schema for the configuration is available at the root of the repository.

https://raw.githubusercontent.com/dave-shawley/pymdown-ietf/refs/heads/main/config-schema.json
