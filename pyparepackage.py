import sys
import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class PackageNode:
    name: str
    version: str
    full_n_v: str
    prev: Optional[Any]

class PackagesStack:
    def __init__(self) -> None:
        self.length: int = 0
        self.head: Optional[PackageNode] = None

    def push(self, n: str, v: str):
        pkg_node = PackageNode(
            name=n,
            version=v,
            full_n_v=f'{n}@{v}',
            prev=None
        )

        self.length += 1
        if not self.head:
            self.head = pkg_node
            return

        pkg_node.prev = self.head
        self.head = pkg_node

    def pop(self) -> Optional[str]:
        self.length = max([0, self.length - 1])
        if self.length == 0:
            head = self.head
            if head:
                self.head = None
                return head.full_n_v
            else:
                return None

        head = self.head
        self.head = head.prev

        return head.full_n_v

def check_fileobject(path: str, fileobject: str):
    try:
        if fileobject == 'file' and not Path(path).is_file():
            raise FileNotFoundError(path, fileobject)
        if fileobject == 'directory' and not Path(path).is_dir():
            raise FileNotFoundError(path, fileobject)
    except FileNotFoundError as err:
        p, o = err.args
        print(f'Invalid {o}, missing {p} in:')
        print(Path.cwd())
        exit(1)

def main(args):
    base_dir = args.base_dir
    pkg_list = args.pkg_list

    check_fileobject(base_dir, 'directory')
    check_fileobject(pkg_list, 'file')

    packages = PackagesStack()

    for _filename in Path(base_dir).iterdir():
        if _filename.suffix == '.yaml':
            pkg_yaml = _filename.open().read()
            yaml_data = yaml.safe_load(pkg_yaml)
            [
                packages.push(
                    n=_filename.stem,
                    v=version
                )
                for version in yaml_data['versions'].keys()
            ]

    # show debug of extracted data      
    total_packages = packages.length + 1 # force 1 None
    print(total_packages)
    i: int = 0
    while i < total_packages:
        pkg = packages.pop()
        if pkg:
            print(pkg)
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir')
    parser.add_argument('pkg_list')
    args = parser.parse_args()
    exit(main(args=args))
