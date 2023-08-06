"""Module containing the base parser for arguments of Cmon."""
import argparse

from cmon.parsers.helper import _chf


def set_base_parser():
    """Set the base parser

    :return: the parser
    """
    from cmon import __version__
    from cmon.helper import colored, format_full_version_info, get_full_version

    # create the top-level parser
    urls = {
        'Code': ('💻', 'https://oss.cmon.ai'),
        'Docs': ('📖', 'https://docs.cmon.ai'),
        'Help': ('💬', 'https://discord.cmon.ai'),
        'Hiring!': ('🙌', 'https://jobs.cmon.ai'),
    }
    url_str = '\n'.join(
        f'- {v[0]:<10} {k:10.10}\t{colored(v[1], "cyan", attrs=["underline"])}'
        for k, v in urls.items()
    )

    parser = argparse.ArgumentParser(
        epilog=f'''
Cmon v{colored(__version__, "green")}: Build multimodal AI services via cloud native technologies.

{url_str}

''',
        formatter_class=_chf,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
        help='Show Cmon version',
    )

    parser.add_argument(
        '-vf',
        '--version-full',
        action='version',
        version=format_full_version_info(*get_full_version()),
        help='Show Cmon and all dependencies\' versions',
    )
    return parser
