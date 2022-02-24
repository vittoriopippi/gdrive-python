import platform
from typing import Sequence
import requests
import tarfile
import os
import subprocess
import sys
# import webbrowser
import threading

class GDriveThread(threading.Thread):
    def set_fun(self, function, *args, **kwargs):
        self.function = function
        self.function_args = args
        self.function_kwargs = kwargs

    def run(self):
        return self.function(*self.function_args, **self.function_kwargs)

class GDrivePath:
    def __init__(self, gdrive, path):
        self.gdrive = gdrive
        assert path.startswith('/'), f'Only absolute path (strats with "/") are accepted. Your path: "{path}"'
        self.path = path
        self.path_list = [p for p in path.split('/') if p != '']
        self.root_id = self.gdrive.info('root')['Id']

    def shortcut(self):
        if len(self.path_list) == 0: return self.root_id
        return self.gdrive.get_id(self.path_list[-1])

    def tree(self, depth=100):
        elements_ids = [('root', self.root_id)]
        for filename in self.path_list:
            elements = self.gdrive.list_dirs(max=depth, parent=elements_ids[-1][1])
            elements = {el['Name']:el for el in elements}
            if filename not in elements:
                elements_ids.append((filename, None))
                break
            elements_ids.append((filename, elements[filename]['Id']))
        return elements_ids

    def id(self, depth=100):
        id = self.shortcut()
        if isinstance(id, str):
            return id
        id = self.tree(depth=depth)[-1][1]
        if id is not None:
            return id
        raise FileNotFoundError(f'File "{self.path}" not found inside the your Google Drive. If you are sure that the file/folder exists maybe you could try to increase the "depth" value.')


class GDrive:
    print_output = False
    folder_name = 'gdrive_folder'
    gdrive = None
    gdrive_names = {
        'windows': 'gdrive.exe',
        'linux': 'gdrive',
        'darwin': 'gdrive',
    }
    token_file = 'token_v2.json'

    def __init__(self, gdrive_path=None, download=False, version=None, os_name=None, arch=None, url=None):
        if download:
            gdrive_path = GDrive.download_script(version=version, os_name=os_name, arch=arch, url=url)

        os.makedirs(self.folder_name, exist_ok=True)
        self.gdrive = os.path.join(self.folder_name, self.gdrive_names[platform.system().lower()])
        if gdrive_path is not None and os.path.exists(gdrive_path):
            self.gdrive = gdrive_path
        if not os.path.exists(self.gdrive):
            raise FileNotFoundError('No gdrive script found.')
        
    @staticmethod
    def download_script(version='2.1.1', os_name=None, arch=None, url=None):
        os_name = os_name if os_name is not None else platform.system().lower()
        this_arch = 'amd64' if platform.architecture()[0] == '64bit' else '386'
        arch = arch if arch is not None else this_arch

        if url is None:
            url = f'https://github.com/prasmussen/gdrive/releases/download/{version}/gdrive_{version}_{os_name}_{arch}.tar.gz'

        r = requests.get(url, allow_redirects=True)
        assert r.status_code == 200

        filename = url.split('/')[-1]
        with open(filename, 'wb') as file:
            file.write(r.content)

        with tarfile.open(filename) as file:
            os.makedirs('gdrive_folder', exist_ok=True)
            file.extractall('gdrive_folder')
        
        folder_files = [f for f in os.listdir('gdrive_folder') if f.startswith('gdrive')]
        assert len(folder_files) == 1
        return os.path.join(os.getcwd(), 'gdrive_folder', folder_files[0])

    def about(self):
        text = ''
        commands = ['--config', self.folder_name, 'about']
        for char in self._exec(commands):
            if self.print_output: sys.stdout.write(char)
            text += char
            if text.startswith('Authentication') and text.endswith('code:'):
                urls = [line for line in text.split('\n') if line.startswith('http')]
                assert len(urls) == 1
                # webbrowser.open(urls[0])
                print()
        if text.startswith('Authentication'):
            return None
        return self._to_dict(text)
    
    def logout(self):
        if os.path.exists(os.path.join(self.folder_name, self.token_file)):
            os.remove(os.path.join(self.folder_name, self.token_file))
    
    def list(self, max=30, querys=[], sort_order=None, name_width=0, absolute=False, no_header=False, bytes=None, parent=None):
        text = ''
        commands = [
            '--config', self.folder_name,
            'list',
            '--max', max,
            '--name-width', name_width,
        ]
        if sort_order: commands += ['--order', sort_order]
        if absolute: commands += ['--absolute']
        if no_header: commands += ['--no-header']
        if bytes: commands += ['--bytes']

        if parent:
            querys.append(f"'{parent}' in parents")

        if len(querys) > 0:
            commands += ['--query', ' and '.join(querys)]
        for char in self._exec(commands):
            if self.print_output: sys.stdout.write(char)
            text += char
        
        return self._to_tabular(text)
    
    def list_dirs(self, *args, **kwargs):
        return self.list(querys=["mimeType = 'application/vnd.google-apps.folder'"], *args, **kwargs)

    def list_files(self, *args, **kwargs):
        return self.list(querys=["mimeType != 'application/vnd.google-apps.folder'"], *args, **kwargs)

    def get_id(self, name):
        elements = self.list(querys=[f"name = '{name}'"])
        if len(elements) == 1:
            return elements[0]['Id']
        elif len(elements) > 1:
            return [el['Id'] for el in elements]
        elif len(elements) == 0:
            return None

    def info(self, id):
        text = ''
        commands = ['--config', self.folder_name, 'info', id]
        for char in self._exec(commands):
            if self.print_output: sys.stdout.write(char)
            text += char
        return self._to_dict(text)

    def upload(self, filename, parent_id=None, parent=None, recursive=True, name=None, description=None,
                mime=None, share=None, timeout=None, chunksize=None, delete=False, thread=False):
        assert os.path.exists(filename)

        if thread:
            t = GDriveThread()
            t.set_fun(self.upload, filename, parent_id, parent, recursive, name, description, mime, share, timeout, chunksize, delete)
            return t
        
        text = ''
        commands = ['--config', self.folder_name, 'upload']
        if recursive: commands += ['--recursive']

        if parent_id is not None:
            commands += ['--parent', parent_id]
        elif parent is not None:
            commands += ['--parent', GDrivePath(self, parent).id()]
            

        if name: commands += ['--name', name]
        if description: commands += ['--description', description]
        if mime: commands += ['--mime', mime]
        if share: commands += ['--share']
        if delete: commands += ['--delete']
        if timeout: commands += ['--timeout', timeout]
        if chunksize: commands += ['--chunksize', chunksize]
        commands += [filename]

        for char in self._exec(commands):
            if self.print_output: sys.stdout.write(char)
            text += char

    def upload_tar(self):
        raise NotImplementedError

    @staticmethod
    def _to_tabular(text):
        header = text.split('\n')[0]
        columns = [c.strip() for c in header.split('  ') if c != '']
        columns_idx = [header.index(c) for c in columns] + [None, ]

        lines = [l for l in text.split('\n')[1:] if l.strip() != '']
        all_files = []
        for line in lines:
            file = {}
            for column, start_idx, end_idx in zip(columns, columns_idx[:-1], columns_idx[1:]):
                file[column] = line[start_idx:end_idx].strip()
            all_files.append(file)
        return all_files

    @staticmethod
    def _to_dict(text):
        data = {}
        for line in text.split('\n'):
            if line.strip() == '': continue
            key, value = line.split(': ')
            data[key] = value
        return data
                
    def _exec(self, cmd):
        if isinstance(cmd, str):
            cmd = cmd.split()
        elif isinstance(cmd, Sequence):
            cmd = [str(c) for c in cmd]
        script = [self.gdrive, ] + cmd
        if self.print_output: print('CMD: ' + ' '.join(script))
        return run_process([self.gdrive, ] + cmd)

def run_process(exe):
    proc = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        # returns None while subprocess is running
        return_code = proc.poll()
        char = proc.stdout.read(1)

        if return_code is not None and len(char) == 0:
            break
        yield char.decode('utf-8')

if __name__ == '__main__':
    # if len(sys.argv) > 1 and sys.argv[1] == 'about':
    #     path = GDrive.download_script()
    #     drive.print_output = True
    #     drive.about()

    drive = GDrive()
    for d in drive.list():
        print(d)
    # print(drive.list_dirs(max=100, parent='root'))
    # print(drive.list_files(max=30, parent='my-drive'))
    # drive.info('root')
    # id = drive.get_id('root')
    # print(id)

    # t = drive.upload('main.py', parent='/Cracovia', thread=True)
    # t.start()
    # t.join()
