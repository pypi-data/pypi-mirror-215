from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]


 
setup(
  name='presslink',
  version='0.0.2',
  description='link mechanisms of mechanical press',
  long_description="This package contains set of modules for various link mechanisms used in mechanical presses",
  url='',  
  author='Sanchit',
  author_email='sanchitsharma84@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mechanical press link mechanism', 
  packages=find_packages(),
  install_requires=["numpy", "xlsxwriter", "matplotlib", "mechpress"],
)