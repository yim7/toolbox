import subprocess
from functools import partial
from concurrent import futures

import click
from .decode import data_url_decode


ok = partial(click.secho, fg="green")
error = partial(click.secho, fg="red")


@click.group()
def cli():
    pass


@cli.command()
@click.argument('src', type=click.File())
@click.argument('dst', type=click.Path(dir_okay=False))
def decode(src, dst):
    """Decode Data URL and save to file."""
    data_url_decode(src.read(), dst)
    ok(f"save to > {click.format_filename(dst)}")


def download_url(url, output_dir=None, playlist=None):
    args = ['you-get', url]
    if output_dir is not None:
        args.append('-o')
        args.append(output_dir)
    if playlist:
        args.append('--playlist')
    subprocess.run(args, stdout=subprocess.DEVNULL)


@cli.command()
@click.option('-o', '--output-dir')
@click.option('-p', '--playlist', is_flag=True, default=False)
@click.option('-f', '--from-file', 'file', type=click.File())
@click.argument('urls', nargs=-1)
def download(urls, file, output_dir, playlist):
    """Using `you-get` to download resources concurrently."""
    if file:
        urls = file
    with futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(download_url, url, output_dir, playlist): url for url in urls}
        for future in futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                error('%r generated an exception: %s' % (url, exc))
            else:
                ok('%r download successfully!' % url)
