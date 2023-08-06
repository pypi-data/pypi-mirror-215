import setuptools

setuptools.setup(
    name="foco_improc",
    version="0.0.0",
    author="UCSF FOCO Lab",
    author_email="focolabdev@gmail.com",
    description="standalone repository for image processing algorithm implementations",
    long_description_content_type=open('README.md').read(),
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy',
          'scipy',
          'opencv-python-headless',
          'scikit-image',
          'matplotlib',
          'pandas',
          'tifffile',
          'pynwb',
          'scipy',
          'matlab'
      ],
    python_requires='>=3.6',
)
