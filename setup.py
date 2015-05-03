try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Online distributed bootstrap',
    'author': 'Netflix Science & Algorithms',
    'url': 'https://github.com/fwhigh/online-blb',
    'download_url': 'https://github.com/fwhigh/online-blb',
    'author_email': 'fwhigh@gmail.com',
    'version': '0.1',
    'install_requires': ['nose','scikit-learn','argparse','matplotlib','scipy','numpy'],
    'packages': ['oblb'],
    'scripts': [],
    'name': 'oblb'
}

setup(**config)
