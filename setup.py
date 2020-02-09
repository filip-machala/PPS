from setuptools import setup

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pps',
    version='0.1',
    description='Python print server for managing printing from users.',
    long_description=long_description,
    author='Filip Machala',
    author_email='machafi1@fit.cvut.cz',
    keywords='',
    license='Public Domain',
    packages=['pps'],
    package_data={'pps': ['templates/*.html', 'static/*.css']},
    tests_require=['pytest==5.0.1', 'flexmock'],
    setup_requires=['pytest-runner'],
    url='https://github.com/philips558/PPS',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Flask',
        ],
    install_requires=['requests', 'Flask', 'wheel', 'sqlalchemy'],
    python_requires='>=3.6',
)
