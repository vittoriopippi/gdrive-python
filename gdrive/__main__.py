from . import GDrive
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to do", type=str)
parser.add_argument("--arch", help="Architecture", type=str, default=None)
parser.add_argument("--version", help="Script version", type=str, default='2.1.1')
parser.add_argument("--os-name", help="Operating system", type=str, default=None)
parser.add_argument("--url", help="Script url", type=str, default=None)

parser.add_argument("--parent_id", help="Script version", type=str, default=None)
parser.add_argument("--parent", help="Script version", type=str, default=None)
parser.add_argument("--no-recursive", help="Script version", action='store_false')
parser.add_argument("--name", help="Script version", type=str, default=None)
parser.add_argument("--description", help="Script version", type=str, default=None)
parser.add_argument("--mime", help="Script version", type=str, default=None)
parser.add_argument("--share", help="Script version", action='store_true')
parser.add_argument("--timeout", help="Script version", type=str, default=None)
parser.add_argument("--chunksize", help="Script version", type=str, default=None)
parser.add_argument("--delete", help="Script version", action='store_true')

parser.add_argument("filename", help="target path", type=str, nargs='?', default=None)

args = parser.parse_args()

if args.action == 'about':
    drive = GDrive(download=True, version=args.version, os_name=args.os_name, arch=args.arch, url=args.url)
    drive.print_output = True
    drive.about()
elif args.action == 'logout':
    if GDrive.logout():
        print('you are now logged out')
    else:
        print('you are not logged in')
elif args.action == 'upload':
    drive = GDrive(download=True, version=args.version, os_name=args.os_name, arch=args.arch, url=args.url)
    drive.print_output = True
    assert args.filename is not None
    drive.upload(args.filename, args.parent_id, args.parent, args.no_recursive, args.name, args.description,
                args.mime, args.share, args.timeout, args.chunksize, args.delete)
elif args.action == 'upload-tar':
    drive = GDrive(download=True, version=args.version, os_name=args.os_name, arch=args.arch, url=args.url)
    drive.print_output = True
    assert args.filename is not None
    drive.upload_tar(args.filename, args.parent_id, args.parent, args.no_recursive, args.name, args.description,
                args.mime, args.share, args.timeout, args.chunksize, args.delete)
else:
    print(f'Command {args.action} not implemented')