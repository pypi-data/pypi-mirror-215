from setuptools import setup, find_packages



with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='anonpi',
    version='0.1.2',
    author='Adistar',
    author_email='adityasamalllll6@gmail.com',
    description='The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests','flask','colorama'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT'
)