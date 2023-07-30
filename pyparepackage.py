import sys
import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

@dataclass
class PackageNode(Generic[T]):
    name: str
    version: str
    full_n_v: str
    prev: Optional[T]

class PackagesStack(PackageNode):
    def __init__(self) -> None:
        self.length: int = 0
        self.head: Optional[PackageNode] = None

    def push(self, n: str, v: str):
        pkg_node: PackageNode = PackageNode(
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

    def pop(self):
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
    base_dir = args.main_dir
    base_file = args.pkg_list

    check_fileobject(base_dir, 'directory')
    check_fileobject(base_file, 'file')

    packages = PackagesStack()

    for _filename in Path(base_dir).iterdir():
        if _filename.suffix == '.yaml':
            _pkg_yaml = _filename.open().read()
            yaml_data = yaml.safe_load(_pkg_yaml)
            [
                packages.push(
                    n=_filename.stem,
                    v=version
                )
                for version in yaml_data['versions'].keys()
            ]

    with open(Path(base_file), 'r') as f:
        _filelist_pkgs = list(map(str.strip, f))

    while packages.length:
        package_name_version = packages.pop()
        if package_name_version not in _filelist_pkgs:
            print(package_name_version)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('main_dir')
    parser.add_argument('pkg_list')
    args = parser.parse_args()
    exit(main(args=args))
