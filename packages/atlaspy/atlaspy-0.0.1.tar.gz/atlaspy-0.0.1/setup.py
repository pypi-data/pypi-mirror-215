from setuptools import setup, find_packages

setup(
    name='atlaspy',
    version='0.0.1',
    description='Python library for working with brain atlases',
    author='Alfredo Lucas',
    author_email='alfredo1238@gmail.com',
    packages=['atlaspy'],
    package_data={
        'atlaspy': ['source_data/*','source_data/*/*','source_data/*/*/*'],
    },
    include_package_data=True,
    install_requires=['pyvista', 'seaborn', 'pandas', 'matplotlib', 'nibabel'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
