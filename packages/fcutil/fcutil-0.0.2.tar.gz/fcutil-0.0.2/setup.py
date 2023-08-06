from setuptools import setup, find_packages

setup(
    name='fcutil',
    version='0.0.2',
    author='Christian Fugini',
    author_email='fuginic@gmail.com',
    description='Piccola libreria di utility',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    #url='https://github.com/tuo_username/my_package',
    #packages=['my_package'],
    # install_requires=[
    #     'numpy>=1.18.0',
    #     'matplotlib>=3.0.0',
    # ],
)