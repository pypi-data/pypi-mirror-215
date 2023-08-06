import os
import re

import rich_click as click

click.rich_click.USE_RICH_MARKUP = True


@click.command()
@click.argument("directory", type=click.Path(exists=True, dir_okay=True), default=".")
@click.argument("pattern", type=click.STRING)
@click.argument("prefix", default="")
@click.option(
    "--padding",
    "-p",
    type=int,
    default=1,
    show_default=True,
    help="Increases zero padding, with a padding of 3 files will be 001.",
)
@click.option(
    "--dry-run", "-d", is_flag=True, help="Perform a dry run without renaming files."
)
@click.option(
    "--limit", "-l", type=int, help="Limit the number of files to be renamed."
)
@click.option(
    "--sort-by",
    "-s",
    type=click.Choice(["alphabetical", "creation", "size"]),
    default="alphabetical",
    help="Specify the sorting criterion.",
    show_default=True,
)
@click.version_option("0.1", prog_name="bulk_rename")
def bulk_rename(directory, pattern, prefix, padding, dry_run, limit, sort_by):
    """
    Bulk rename files in a directory with a given pattern, prefix and padding.

    Default directory is the current one.

    Files will be renamed incrementally. e.g: file1, file2, ...

    Pattern must be a regex.

    Prefix is optional.

    [yellow bold]Example Usage:[/]

    [i]Rename all files with png and jpg extension[/]

    [blue]bulk_rename path/to/dir/ ".*.(png|jpg)"[/]

    [i]Rename all files that contain "image", add prefix "Wallpaper" with 2 padding[/]

    [blue]bulk_rename path/to/dir/ "image*" "Wallpaper" -p 2[/]

    [i]Rename all files limited to 10, sorted by size[/]

    [blue]bulk_rename path/to/dir/ "*" -l 10 -s size[/]

    """
    file_list = os.listdir(os.path.expanduser(directory))

    if sort_by == "alphabetical":
        file_list.sort()
    elif sort_by == "creation":
        file_list.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))
    elif sort_by == "size":
        file_list.sort(key=lambda x: os.path.getsize(os.path.join(directory, x)))

    if limit is not None:
        file_list = file_list[:limit]

    for i, file_name in enumerate(file_list):
        item_path = os.path.join(directory, file_name)
        if re.match(pattern, file_name) and os.path.isfile(item_path):
            file_name_parts = os.path.splitext(file_name)
            new_file_name = f"{prefix}{str(i+1).zfill(padding)}{file_name_parts[1]}"

            old_file = os.path.join(directory, file_name)
            new_file = os.path.join(directory, new_file_name)

            if dry_run:
                click.echo(f"Will rename: {file_name} -> {new_file_name}")
            else:
                os.rename(old_file, new_file)
                click.echo(f"Renamed: {file_name} -> {new_file_name}")


if __name__ == "__main__":
    bulk_rename()
