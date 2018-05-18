from setuptools import setup, find_packages

setup(name='ftb_overlay',
      version='0.2a',
      description="FTB Modpack Customizing Tool",
      long_description="FTB Modpack Customizing Tool",
      classifiers=[],
      keywords='',
      author='R. Dragone',
      author_email='rdragone@saturnblack.com',
      url='https://github.com/oneirosFade/ftb-overlay',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=[
          ### Required to build documentation
          # "Sphinx >= 1.0",
          ### Required for testing
          # "nose",
          # "coverage",
          ### Required to function
          'cement',
      ],
      setup_requires=[],
      entry_points="""
        [console_scripts]
        ftb_overlay = ftb_overlay.cli.main:main
    """,
      namespace_packages=[],
      )
