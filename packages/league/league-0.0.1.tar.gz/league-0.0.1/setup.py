import league
import setuptools

url = 'https://github.com/timothyckl/league.py'
readme = open('README.md', 'r')
long_description = readme.read()

setuptools.setup(
    name="league",
    license="MIT",
    author="timothyckl",
    description=league.__doc__,
    version=league.__version__,

    url=url,
    project_urls={
        "Source Code": url,
        "Pull Requests": url + "/pulls",
        "Issue Tracker": url + "/issues",
    },

    long_description=readme,
    long_description_content_type="text/markdown",

    python_requires=">=3.8.0",
    zip_safe=False,
    packages=['league', 'league.objects'],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development"
    ]
)