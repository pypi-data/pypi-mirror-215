from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Get geocode from google map'
LONG_DESCRIPTION = 'A package that based on google maps search to find location based on address'

# Setting up
setup(name="gmaps-locator",
      version=VERSION,
      author="Akbar Tolandy",
      author_email="<akbartolandy@gmail.com>",
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=long_description,
      packages=find_packages(),
      install_requires=['requests-html'],
      keywords=['python', 'gmaps', 'geocode'],
      project_urls={
          "Homepage": "https://github.com/AkbarTolandy/gmaps_locator.git"
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])