from setuptools import setup, find_packages

setup(
    name='timetable_exporter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'icalendar'
    ],
    entry_points={
        'console_scripts': [
            'timetable-exporter=timetable_exporter.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'timetable_exporter': ['config/config.json', 'config/filters.json'],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A module to generate iCal files from timetabling Excel sheets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ical-timetable-project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)