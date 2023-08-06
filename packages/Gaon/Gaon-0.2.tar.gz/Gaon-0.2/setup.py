from setuptools import setup, find_packages

setup(
    name='Gaon',
    version='0.2',
    packages=find_packages(),
    license='MIT',
    description='AI library for Sidedrawer',
    long_description=open('README.md').read(),
    install_requires=['pdf2image', 'opencv-python', 'pytesseract', 'numpy', 'pandas', 'scikit-learn'], # add other required packages
    author='Gaon.ai',
    author_email='support@gaon.ai'
)
