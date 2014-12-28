# vim: set et ts=4 sw=4 sts=4 ai:

from distutils.core import setup
import tuhinga

long_desc = '''
Tuhinga is a minimalistic markup language that translates to XML/HTML.
'''

setup(
    name='tuhinga',
    version=tuhinga.__version__,
    description=tuhinga.__doc__,
    author=tuhinga.__author__,
    author_email='benjamin@babab.nl',
    # url='http://github.com/babab/tuhinga',
    # download_url='http://github.com/babab/tuhinga',
    py_modules=['tuhinga'],
    license='ISC',
    long_description=long_desc,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
        'Programming Language :: Python :: 3.4',
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
    ],
    scripts=['tuh'],
    )
