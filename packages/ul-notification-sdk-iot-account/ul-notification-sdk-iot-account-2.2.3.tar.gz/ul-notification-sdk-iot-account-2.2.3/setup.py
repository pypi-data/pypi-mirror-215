from os import path
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ul-notification-sdk-iot-account',
    version='2.2.3',
    description='Notification service sdk for IoT account',
    author='Unic-lab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['notification_sdk'],
    package_data={
        "notification_sdk": [
            'py.typed',
        ],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent"
        ],
    platforms='any',
    install_requires=[
        # 'ul-api-utils==7.2.8',
        # 'ul-py-tool==1.15.20',
        # 'ul-db-utils==2.10.7',
    ],
)
