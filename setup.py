from distutils.core import setup

setup(
    name='django-verify-email',
    version='0.1.dev',
    author='Ivan Raskovsky (rasca)',
    author_email='raskovsky@gmail.com',
    packages=['verify_email',],
    license='BSD',
    description='verifies email addresses to grant permission to views',
    long_description=open('README.txt').read(),
)
