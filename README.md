# gdrive-python
`gdrive-python` is a wrapping module in python of [gdrive](https://github.com/prasmussen/gdrive) made by [@prasmussen](https://github.com/prasmussen).

- [Installation](#installation)
  - [`FileNotFoundError`](#filenotfounderror)
- [Usage](#usage)
  - [`GDrive`](#gdrive)
    - [`__init__`](#__init__self-gdrive_pathnone)
    - [`download_script`](#staticmethod-download_scriptversion211-os_namenone-archnone-urlnone)
    - [`upload`](#uploadself-filename-parent_idnone-parentnone-recursivetrue-namenone-descriptionnone-mimenone-sharenone-timeoutnone-chunksizenone-deletefalse-threadfalse)
      - [thread](#thread)
    - [`about`](#aboutself)
    - [`logout`](#logoutself)
    - [`list`](#listself-max30-querys-sort_ordernone-name_width0-absolutefalse-bytesnone-parentnone)
    - [`list_dirs`](#list_dirsself-args-kwargs)
    - [`list_files`](#list_filesself-args-kwargs)
    - [`get_id`](#get_idself-name)
    - [`info`](#infoself-id)

## Installation
First of all to install the package you can execute:
```
pip install gdrive-python
```
Than you have to login inside your Google account with the command and than follow the instructions:
```
python -m gdrive about [options]

options:
  --version     Version of the gdrive script to download
  --os-name     Operating system name, by default it gets current os. Options: ['windows', 'linux', 'darwin']
  --arch        Architecture. Options: ['amd64', '386']
  --url         Url of the gdrive script
```
Example output:
```
vpippi$ python -m gdrive about
CMD: gdrive_folder/gdrive --config gdrive_folder about
Authentication needed
Go to the following url in your browser:
https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=############.apps.googleusercontent.com&redirect_uri=#########&response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&state=state

Enter verification code:
# paste here the code and press enter
```

### FileNotFoundError
Somethimes it can happen that the command `python -m gdrive about` returns the `FileNotFoundError`
```
vpippi$ python -m gdrive about
CMD: gdrive_folder/gdrive --config gdrive_folder about
Traceback (most recent call last):
  ...
FileNotFoundError: [Errno 2] No such file or directory: 'gdrive_folder/gdrive'
```

In my case it happened because the current system architecture is `amd64` but this version don't works in that system. You can avoid that problem by installing the `386` architecture.
```
python -m gdrive about --arch 386
```

## Usage
import the `gdrive` classes in that way: 
```python
form gdrive import GDrive, GDrivePath, GDriveThread
```
### GDrive
```python
drive = GDrive()
```
If you whant you can also enable the printing commands setting:
```python
drive.print_output = True
```
### \_\_init\_\_(self, gdrive_path=None)
- `gdrive_path` defines the gdrive script location path. If not specified it gets the default location `gdrive_folder/gdrive`

### `@staticmethod` download\_script(version='2.1.1', os_name=None, arch=None, url=None)

- `version` is the version of the gdrive script to download
- `os_name` is the operating system name, by default it gets current os. Options: `['windows', 'linux', 'darwin']`
- `arch` is the architecture. Options: `['amd64', '386']`
- `url` is the url of the gdrive script. If an url is provided the other fields are ignored.

The script download the specified version in the current directory (eg. `gdrive_2.1.1_windows_amd64.tar.gz`) and than extract the archive inside the directory `gdrive_folder`. 

Returns None.

### upload(self, filename, parent\_id=None, parent=None, recursive=True, name=None, description=None, mime=None, share=None, timeout=None, chunksize=None, delete=False, thread=False)
- `filename` path of the file/folder to upload
- `parent` parent directory by name (eg. `/path/foldername`)
- `parent_id` parent id, used to upload file to a specific directory, if specified `parent` folder is ignored.
- `recursive` upload directory recursively
- `name` filename
- `description` file description
- `mime` force mime type
- `share` share file
- `timeout` set timeout in seconds, use 0 for no timeout. Timeout is reached when no data is transferred in set amount of seconds, default: 300
- `chunksize` set chunk size in bytes, default: 8388608
- `delete` delete local file when upload is successful
- `thread` defines if you want to upload the file in a separate thread (see the thread section)

While uploading a large file could be useful set `print_output = True`

**Example:**
```python
>>> drive.print_output = True
>>> drive.upload('File99.mp4')
CMD: gdrive_folder\gdrive.exe --config gdrive_folder upload --recursive checkpoint_042.pth
Uploading checkpoint_042.pth
1.1 GB / 2.0 GB, Rate: 13.7 MB/s
```

#### thread
When `thead=True` the methods return a `GDriveThread(threading.Thread)` object.

**Usage:**
```python
>>> thread = drive.upload('File99.mp4', thread=True)
>>> thread.start()
>>> # do whatever you want
>>> thread.join()
```

### about(self)
Returns a dictionary that shows the account info.

**Example:**
```python
>>> drive.about()
{
    'User': 'name username, email@example.com',
    'Used': '51 GB',
    'Free': '9 GB',
    'Total': '60 GB',
    'Max upload size': '60 GB',
}
```
### logout(self)
The `logout` function delete the file `gdrive_folder/token_v2.json` which contains the google info. After this command the login is required again (see installation procedure).
### list(self, max=30, querys=[], sort\_order=None, name\_width=0, absolute=False, bytes=None, parent=None)
- `max` max files to list
- `querys` query list to execute. See https://developers.google.com/drive/search-parameters
- `sort_order` sort order. See https://godoc.org/google.golang.org/api/drive/v3#FilesListCall.OrderBy
- `name_width` width of name column, minimum: 9, use 0 for full width
- `absolute` show absolute path to file (will only show path from first parent)
- `bytes` return size in bytes
- `parent` list files inside the given parent folder. By default it uses the root directory.

Returns a list of dictionaries.
**Example:**
```python
>>> drive.list()
[
    {'Id': '######', 'Name': 'File01.mp4', 'Type': 'bin', 'Size': '196.1 MB', 'Created': '2022-01-13 19:42:00'},
    {'Id': '######', 'Name': 'File02.mp4', 'Type': 'bin', 'Size': '210.7 MB', 'Created': '2022-01-13 19:42:00'},
    {'Id': '######', 'Name': 'File03.mp4', 'Type': 'bin', 'Size': '197.5 MB', 'Created': '2022-01-13 19:42:00'},
    {'Id': '######', 'Name': 'File04.mp4', 'Type': 'bin', 'Size': '191.5 MB', 'Created': '2022-01-13 19:42:00'},
    {'Id': '######', 'Name': 'File05.mp4', 'Type': 'bin', 'Size': '176.1 MB', 'Created': '2022-01-13 19:42:00'},
    {'Id': '######', 'Name': 'File06.mp4', 'Type': 'bin', 'Size': '178.0 MB', 'Created': '2022-01-13 19:42:00'},
    ...
]
```
### list\_dirs(self, \*args, \*\*kwargs)
Same parameters as the `list` method.

Returns only the a list of dirs.
### list\_files(self, \*args, \*\*kwargs)
Same parameters as the `list` method.

Returns only the a list of files.
### get\_id(self, name)
- `name` name of the file/folder that you want the id

Since Google Drive allows different files/directories with the same name, the function returns:
- `string` if only one element is found
- `list` of the ids if more than one file is returned
- `None` if only no one element is found

**Example:**
```python
>>> drive.get_id('File01.mp4')
'BWoSkGeDNbYqyumaRXtQvzgHndUMET'

>>> drive.get_id('File00.mp4')
['BWoSkGeDNbYqyumaRXtQvzgHndUMET', 'vzgHndUMETscKflCxpVOwhjrAiPLFI']

>>> drive.get_id('File99.mp4')
None
```
### info(self, id)
- `id` id of the file/folder

Returns a dictionary of all info values of the given element.
