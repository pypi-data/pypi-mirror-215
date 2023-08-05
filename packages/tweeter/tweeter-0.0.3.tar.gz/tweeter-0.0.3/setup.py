from setuptools import setup

VERSION = "0.0.3"
SHORT_DESCRIPTION = "TweeterPy is a python library to extract data from Twitter. TweeterPy API lets you scrape data from a user's profile like username, userid, bio, followers/followings list, profile media, tweets, etc."

setup(
    name="tweeter",
    version=VERSION,
    author="Sarabjit Dhiman",
    author_email='hello@sarabjitdhiman.com',
    url="https://pypi.python.org/pypi/tweeterpy",
    description=SHORT_DESCRIPTION,
    long_description="""This is a copy of TweeterPy package. Check more details on [TweeterPy](https://pypi.python.org/pypi/tweeterpy).""",
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=['tweeterpy'],
    keywords=["twitterpy", "twitter scraper", "tweet scraper",
              "twitter data extraction", "twitter api",
              "twitter python", "tweet api", "tweetpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3"
    ]
)
