try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Streaming Distributed Bootstrap',
    'author': 'William High',
    'url': 'https://github.com/fwhigh/sdbootstrap',
    'download_url': 'https://github.com/fwhigh/sdbootstrap',
    'author_email': 'fwhigh@gmail.com',
    'version': '0.1',
    'install_requires': ['nose','scikit-learn','argparse','matplotlib','scipy','numpy'],
    'packages': ['sdbootstrap'],
    'scripts': [],
    'name': 'sdbootstrap'
}

setup(**config)
