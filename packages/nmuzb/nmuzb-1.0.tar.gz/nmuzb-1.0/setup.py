from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='nmuzb',
    version='1.0',
    description="O'zbek ismlarining to'liq, batafsil ma'nosi, kelib chiqishi, shakllari. O'zingiz va yaqinlaringizni ismlari ma'nosini bilib oling.",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='XUDOBERDI GAYRATOV',
    author_email='xudoberdigayratov@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='name meaning',
    packages=find_packages(),
    install_requires=['']
)
