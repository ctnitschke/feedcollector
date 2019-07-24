# Feedcollector

This is a simple tool to archive feed contents. It downloads feed
files and, if called repeatedly, appends new content while keeping old
entries.

Currently, only RSS feeds are supported, which
is sufficient for my particular usecase. Extending support to other
feed types is planned. 
The tool may experience erratic bursts of heavy development, involving
harsh changes in config etc., so use at your own risk.

## Files

- `<APP_DATA_DIR>/feedcollector/*.rss` - feed files
- `<APP_DATA_DIR>/feedcollector/feedcollector.opml` - feed list

On Linux systems (which I mostly use), `<APP_DATA_DIR>` is usually set to
`~/.local/share/` or set by the environment variable `XDG_DATA_DIR`.

## Roadmap

- Support for Atom feeds
- Support for JSON feeds
- Feed type discovery
