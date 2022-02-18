from . import GDrive
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to do", type=str)
parser.add_argument("--arch", help="Architecture", type=str, default=None)
parser.add_argument("--version", help="Script version", type=str, default='2.1.1')
parser.add_argument("--os-name", help="Operating system", type=str, default=None)
parser.add_argument("--url", help="Script url", type=str, default=None)
args = parser.parse_args()

if args.action == 'about':
    path = GDrive.download_script(version=args.version, os_name=args.os_name, arch=args.arch, url=args.url)
    drive = GDrive(path)
    drive.print_output = True
    drive.about()