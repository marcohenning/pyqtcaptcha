from setuptools import setup, find_namespace_packages


with open('README.md', 'r') as fh:
    readme = "\n" + fh.read()

setup(
    name='pyqtcaptcha',
    version='1.0.0',
    author='Marco Henning',
    license='MIT',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        'pyqtcaptcha.files': ['**/*.png', '**/*.mp3'],
        'pyqtcaptcha.hooks': ['*.py']
    },
    install_requires=[
        'QtPy>=2.4.1',
        'pygame>=2.6.0'
    ],
    python_requires='>=3.7',
    description='A modern and fully customizable CAPTCHA library for PyQt and PySide',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/marcohenning/pyqtcaptcha',
    keywords=['python', 'pyqt', 'qt', 'captcha'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)
