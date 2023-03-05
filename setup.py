from setuptools import setup, find_packages
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(BASE_DIR / 'VERSION') as file:
        return file.readline().strip()


def get_license():
    with open(BASE_DIR / 'LICENSE') as file:
        return file.read().strip()


def get_desc():
    with open(BASE_DIR / 'README.md') as file:
        return file.read().strip()


setup(
    name='asrv',
    version='0.1.1',
    author='ME',
    author_email='me@gmail.com',
    # url='',
    packages=find_packages(
        '.', include=['asrv', 'asrv.*'], exclude=['*tests*.py', 'test*']
    ),
    package_dir={'asrv.*': 'asrv'},
    include_package_data=True,
    license=get_license(),
    description='important info',
    long_description=get_desc(),
    long_description_content_type='text/markdown',
    install_requires=['lib', 'lib'],
    python_requires='>3.9',
    classifiers=[
        'Framework :: AnyIO',
        'Framework :: Django :: 2',
        'Development Status :: 3 - Alpha'
        if 'dev' in get_version()
        else 'Development Status :: 4 Beta'
        if 'rc' in get_version()
        else 'Development Status :: 5 Production/Stable'
    ],
    entry_points={
        'console_scripts': ['asrv_runer = asrv.app:run']
    }
)
