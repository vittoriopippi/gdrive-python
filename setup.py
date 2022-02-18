from setuptools import setup

setup(
    name='gdrive-python',
    version='1.0.1',    
    description='Python wrapper for Google Drive',
    url='https://github.com/vittoriopippi/gdrive-python',
    author='Vittorio Pippi',
    author_email='vittorio.pippi@unimore.it',
    license='BSD 2-clause',
    packages=['gdrive-python'],
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
    ],
)