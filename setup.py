from setuptools import setup

setup(
    name='gdrive-python',
    version='1.0.8',    
    description='Python wrapper for Google Drive',
    url='https://github.com/vittoriopippi/gdrive-python',
    author='Vittorio Pippi',
    author_email='vittorio.pippi@unimore.it',
    license='BSD 2-clause',
    packages=['gdrive'],
    install_requires=['requests'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)