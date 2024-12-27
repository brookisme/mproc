from distutils.core import setup
setup(
  name = 'mproc',
  py_modules = ['mproc'],
  version = '0.0.0.4',
  description = 'Python Multiprocessing helpers',
  author = 'Brookie Guzder-Williams',
  author_email = 'brook.williams@gmail.com',
  url = 'https://github.com/brookisme/mproc',
  download_url = 'https://github.com/brookisme/mproc/tarball/0.1',
  keywords = ['Multiprocessing','Pool','Threadpool'],
  include_package_data=True,
  data_files=[
    (
      'config',[]
    )
  ],
  classifiers = [],
  entry_points={
      'console_scripts': [
      ]
  }
)