from setuptools import setup, find_packages
from setuptools.command.install import install
import atexit
import subprocess


def run_auto_script():
    print('========================================== starting compilation ==========================================')
    subprocess.check_call(['pip', 'install', './pypdfe_builder'])
    print('===========================================================================================================')
    print('================ The installation was successful. Ignore all errors beneath this message. =================')
    print('===========================================================================================================')

class CustomInstallCommand(install):
    def run(self):
        # install.run(self)
        atexit.register(run_auto_script)
        # subprocess.check_call(['pip', 'uninstall', 'pypdfe_builder'])


setup(
    name='pypdfe',
    version='0.1.1',
    author='Your Name',
    author_email='your_email@example.com',
    description="A python package for Dr. Jennifer Farmer's PDF-Estimator",
    long_description='A longer description',
    url='https://github.com/your_username/your_package_name',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords='your, keywords, here',
    install_requires=[
        'numpy',
        'wheel',
    ],
    cmdclass={
        'install': CustomInstallCommand
    },
)
