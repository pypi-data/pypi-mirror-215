import sys
import os
import codecs
from setuptools import setup, find_packages


version = '1.0'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requires = [
    'Django>=2.2',
    'wagtail>=2.16,<5.0'
]

jinja2_requires = [
    'jinja2>=2.9.6',
]

test_requires = [
    'pytest==7.3.0',
    'pytest-cov',
    'pytest-django',
    'pytest-flakes==4.0.5',
    'pytest-pycodestyle==2.3.1',
    'pycodestyle==2.10.0',
    'mock==5.0.1',
    'six==1.16.0',
]

test_requires += jinja2_requires


setup(
    name='wagtail_csp',
    version=version,
    description='Wagtail Content Security Policy support.',
    long_description=read('README.rst'),
    #long_description_content_type='text/markdown',
    author='anti_commute',
    author_email='7478938-anti_commute@users.noreply.gitlab.com',
    url='https://gitlab.com/womens-declaration/wagtail-csp',
    license='BSD',
    packages=find_packages(),
    project_urls={
        "Changelog": "https://gitlab.com/womens-declaration/wagtail-csp/-/blob/wagtail-settings/CHANGES",
        "Bug Tracker": "https://gitlab.com/womens-declaration/wagtail-csp/-/issues",
        "Source Code": "https://gitlab.com/womens-declaration/wagtail-csp/-/tree/wagtail-settings",
    },
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
        'jinja2': jinja2_requires,
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ]
)
