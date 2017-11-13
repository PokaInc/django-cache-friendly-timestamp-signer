from setuptools import setup, find_packages

f = open('README.md')
readme = f.read()
f.close()

version = '0.0.1'

setup(
    name='django-cache-friendly-timestamp-signer',
    version=version,
    description="Cached URLs that can be kept in browser's cache",
    long_description=readme,
    keywords="signed url timestamp cache django",
    author='Raphael Riel',
    author_email='rriel@poka.io',
    maintainer='Raphael Riel',
    maintainer_email='rriel@poka.io',
    url='https://github.com/PokaInc/django-cache-friendly-timestamp-signer',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    zip_safe=False,
)