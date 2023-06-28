from setuptools import find_packages, setup

requirements = [
    'aiohttp==3.8.4',
    'pydantic==1.10.7'
]
setup(
    name="proxy6",
    version="1.0.1",
    author="Nikolai Dobrydnev",
    author_email="nidobrydnev@gmail.com",
    license="MIT",
    url="https://github.com/Yessirskiy/Proxy6",
    install_requires=requirements,
    keywords=[
        "proxy",
        "proxysix",
        "proxy6"
    ],
    description="Fast and Asynchronous API Wrapper for proxy6.net",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    platforms='any',
    python_requires=">=3.8",
    include_package_data=True
    # classifiers=[
    #     "Development Status :: 4 - Beta",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     "Topic :: Software Development :: Libraries :: Python Modules",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    # ],
)