from setuptools import setup

setup(
    data_files = [
        ('share/man/man1', [
            'doc/zennin.1',
            ]),
        ('share/doc/zennin/', [
            'zennin/quotebook.txt',
            ]),
    ],
)
