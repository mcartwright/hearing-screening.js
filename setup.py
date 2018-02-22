from setuptools import setup

setup(
    name='hearing_screening',
    version='1.0.1dev1',
    packages=['hearing_screening'],
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "Flask==0.12.2",
        "Flask-SQLAlchemy==2.3.2",
    ],
)