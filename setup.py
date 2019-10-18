from setuptools import setup

setup(
    name='faceR',
    version='0.1',
    packages=['utils', 'utils.dbUtils'],
    url='',
    license='',
    author='wjn',
    author_email='',
    description='人像对比',
    install_requires = [  # 依赖列表
        'flask' >= '1.1.1',
        'pymongo' >= '3.7.1'
    ]
)
