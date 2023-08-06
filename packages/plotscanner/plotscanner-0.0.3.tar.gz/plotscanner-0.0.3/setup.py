from setuptools import setup

with open("README.md", "r") as fin:
    long_description = fin.read()

setup(name='plotscanner',
      version='0.0.3',
      description='The application for digitizing images of plots.',
      packages=['plotscanner'],
      py_modules = ['plotscanner'],
      author_email='silru@internet.ru',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/IlS0/Plot-digitization",
      install_requires=[
          'matplotlib>=3.7.1',
          'numpy>=1.25.0',
          'PyQt5>=5.15.9',
          'opencv-python-headless>=4.7.0.72',
          'pandas>=1.5.3',
          'openpyxl>=3.1.2'
      ],
      entry_points={
          'console_scripts': [
          'plotscanner = plotscanner.GUI:main',
      	]
      },
      include_package_data=True,
      package_data={
        'plotscanner': ['ui/*.ui','readme_imgs/*']
      }
      )
