from setuptools import setup

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pps',
    version='0.1',
    description='Web server and cli for github issue assigner',
    long_description=long_description,
    author='Filip Machala',
    author_email='machafi1@fit.cvut.cz',
    keywords='',
    license='Public Domain',
    packages=['pps'],
    package_data={'pps': ['templates/*.html', 'static/*.css']},
    tests_require=['pytest==5.0.1'],
    setup_requires=['pytest-runner'],
    url='https://github.com/philips558/ghia3',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Framework :: Flask',
        ],
    install_requires=['requests', 'rq', 'Flask', 'wheel', 'configparser'],
    python_requires='>=3.6',
)
