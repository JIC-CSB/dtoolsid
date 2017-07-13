from setuptools import setup

url = "https://github.com/JIC-CSB/dtoolsid"
version = "0.1.0"
readme = open('README.rst').read()

setup(name="dtoolsid",
      packages=["dtoolsid"],
      version=version,
      description="Experimental branch for dtool CLI",
      long_description=readme,
      include_package_data=True,
      author="Matthew Hartley",
      author_email="Matthew.Hartley@jic.ac.uk",
      url=url,
      install_requires=[
          "click",
          "dtool",
          "pygments",
      ],
      entry_points={
          'console_scripts': ['dtoolsid=dtoolsid.cli:cli']
      },
      download_url="{}/tarball/{}".format(url, version),
      license="MIT")
