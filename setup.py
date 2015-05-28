# vim: set et ts=4 sw=4 sts=4 ai:

from setuptools import setup
import tuhinga

setup(
    name='tuhinga',
    version=tuhinga.__version__,
    description=tuhinga.__doc__,
    author=tuhinga.__author__,
    author_email='benjamin@babab.nl',
    url='http://github.com/babab/tuhinga',
    download_url='https://pypi.python.org/pypi/tuhinga',
    py_modules=['tuhinga'],
    license='ISC',
    long_description=open('README.rst').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Adaptive Technologies',
        'Topic :: Documentation',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',

        'BLOCK FROM REGISTRATION/UPLOAD - REMOVE BEFORE SUBMIT',
    ],
    scripts=['tuh'],
)
