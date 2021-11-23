#!/usr/bin/env python3

import click
import os
import feedparser
import base64
import json

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--dry-run', is_flag=True, help='Do not update cache files')
@click.option('--path', default=".", type=click.Path(exists=True,writable=True,resolve_path=True), help='Path where to store backup files')
@click.argument('url')
def rssbackup(verbose, dry_run,
              path, url):
    click.echo(click.format_filename(path))
    feed = feedparser.parse(url)
    for e in feed['entries']:
        g = e.id
        n = (base64.urlsafe_b64encode(g.encode())).decode("ASCII") + ".json"
        if os.path.exists(n):
            if verbose:
                print('Skipping: "%s"' % e.title)
        else:
            if verbose:
                print('Saving: "%s" as %s' % (e.title,n) )
        if not dry_run:
            with open(n,"w") as f:
                json.dump(e,f,ensure_ascii=False)

if __name__ == '__main__':
    rssbackup()
