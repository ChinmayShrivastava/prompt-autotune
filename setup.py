from setuptools import setup, find_packages

setup(
    name='prompt_autotune',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        "llama_index==0.10.20",
        "python-dotenv",
    ],
    # Additional metadata about your package.
    author='Chinmay Shrivastava',
    author_email='cshrivastava99@gmail.com',
    description='A light weight library that takes in a `task description` and a `prompt` and tunes the prompt to perform better.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChinmayShrivastava/prompt-autotune',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Entry points create executable commands and tools for your package.
    entry_points={
        'console_scripts': [
            'tune=prompt_autotune.main:main',
        ],
    },
)