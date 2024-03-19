from setuptools import setup, find_packages

setup(
    name='prompt_autotune',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        "llama_index==0.10.20",
        "python-dotenv",
    ],
    # Additional metadata about your package.
    author='Chinmay Shrivastava',
    author_email='cshrivastava99@gmail.com',
    description='A short description of the package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/package_name',
    license='MIT',
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
    ],
    # Entry points create executable commands and tools for your package.
    entry_points={
        'console_scripts': [
            'tune=prompt_autotune.main:main',
        ],
    },
)