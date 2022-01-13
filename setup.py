from distutils.core import setup
setup(
  name = 'pyCKW',
  packages = ['pyCKW'],
  version = '0.1',
  license='MIT',
  description = 'Access your myCKW smartmeter data.',
  author = 'jeremy Diaz',
  author_email = 'jd@diaznet.fr',
  url = 'https://github.com/diaznet/pyCKW',
  download_url = 'https://github.com/diaznet/pyCKW/archive/pyCKW-0.1.tar.gz',
  keywords = ['myCKW', 'smartmeter', 'data', 'power', 'consumption'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)