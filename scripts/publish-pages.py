#!/usr/bin/env python3
"""Publish the checked static artifact to the dedicated Pages branch."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REMOTE = 'https://github.com/sbenson2/PocketCPU.git'


def run(arguments, cwd=ROOT, capture=False):
    return subprocess.run(arguments, cwd=cwd, check=True, text=True,
                          capture_output=capture, timeout=120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true', help='commit and push to gh-pages')
    args = parser.parse_args()
    run(['python3', 'scripts/build-site.py'])
    if not args.publish:
        print('Checked artifact is ready in _site/. Add --publish to update GitHub Pages.')
        return
    if run(['git', 'status', '--porcelain'], capture=True).stdout.strip():
        raise SystemExit('Commit or set aside source changes before publishing.')
    # Keep the source checkout and its branch untouched. Push normally so a
    # concurrent publication is rejected instead of overwritten.
    with tempfile.TemporaryDirectory(prefix='pocketcpu-pages-') as temporary:
        checkout = Path(temporary) / 'site'
        run(['git', 'clone', '--quiet', '--single-branch', '--branch', 'gh-pages', REMOTE, str(checkout)])
        for setting in ('user.name', 'user.email'):
            value = run(['git', 'config', '--get', setting], capture=True).stdout.strip()
            run(['git', 'config', setting, value], cwd=checkout)
        run(['git', 'rm', '-r', '--quiet', '--ignore-unmatch', '.'], cwd=checkout)
        shutil.copytree(ROOT / '_site', checkout, dirs_exist_ok=True)
        run(['git', 'add', '.'], cwd=checkout)
        changed = run(['git', 'diff', '--cached', '--name-only'], cwd=checkout, capture=True).stdout.strip()
        if changed:
            source = run(['git', 'rev-parse', '--short', 'HEAD'], capture=True).stdout.strip()
            run(['git', 'commit', '-m', 'Publish PocketCPU site from ' + source], cwd=checkout)
            run(['git', 'push', 'origin', 'gh-pages'], cwd=checkout)
        else:
            print('The published branch already matches the checked artifact.')
    run(['gh', 'api', '--method', 'POST', 'repos/sbenson2/PocketCPU/pages/builds'])
    print('Pages build requested. Verify https://sbenson2.github.io/PocketCPU/ before calling it deployed.')


if __name__ == '__main__':
    main()
