# Feedcollector

This is a simple tool to archive feed contents. It downloads feed
files and, if called repeatedly, appends new content while keeping old
entries.

Currently, only RSS feeds are supported, which
is sufficient for my particular usecase. Extending support to other
feed types is planned. Furthermore, because of directory naming
conventions, the feedcollector tool only runs on Linux for now, but
that might change in the future.

The tool may experience erratic bursts of heavy development, involving
harsh changes in config etc., so use at your own risk.

## Files

- `$XDG_DATA_HOME/feedcollector/*.rss` - feed files
- `$XDG_DATA_HOME/feedcollector/feedcollector.opml` - feed list

`$XDG_DATA_HOME` usually is `~/.local/share/`, which also is the default.

## Roadmap

- Support for Atom feeds
- Support for JSON feeds
- Feed type discovery
