from setuptools import find_packages, setup

setup(
    name='feedcollector',
    version='0.1',
    packages=['feedcollector'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
    ],
    extras_require={
        'namespaces': 'lxml',
    },
    entry_points={
        'console_scripts': [
            'feedcollector = feedcollector.__main__:main'
        ]
    },
)
