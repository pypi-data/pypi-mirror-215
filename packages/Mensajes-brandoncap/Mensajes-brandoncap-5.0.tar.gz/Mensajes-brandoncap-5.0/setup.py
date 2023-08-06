from setuptools import setup, find_packages

setup(
    name='Mensajes-brandoncap',
    version='5.0',
    description='un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Brandon Fornes',
    author_email='Brandon@gmail.com',
    url='https://www.brandon.dev',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Academic Free License (AFL)',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Desktop Environment :: File Managers',
    ]
    
)