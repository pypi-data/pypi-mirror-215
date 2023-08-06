import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='habitat-tools',  
     version='0.2.0',
     author="Warren Snowden",
     author_email="warren.snowden@gmail.com",
     description="A habitat API utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=setuptools.find_packages()
 )