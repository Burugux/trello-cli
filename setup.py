from setuptools import setup

setup(
    name='trello-cli',
    version='0.1',
    py_modules=['trello'],
    install_requires=[
        'Click',
        'requests',
        'python-dotenv',
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        trello=trello:cli
    ''',
)
