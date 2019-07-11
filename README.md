# Feedcollector

This is a simple tool to archive feed contents. It downloads feed files
and, if called repeatedly, appends new content while keeping old entries.

Currently, only RSS feeds are supported, and because of directory naming
conventions, it only runs on Linux, but that might change in the future.
The tool may experience erratic bursts of heavy development, involving harsh
changes in config etc., so use at your own risk.

## Roadmap

- Import feeds from OPML rather than from an .ini-style file
- Support for Atom feeds
- Support for JSON feeds
- Feed type discovery
