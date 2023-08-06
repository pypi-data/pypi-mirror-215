from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='grpcrest',
      version='0.17',
      description='REST Wrapper for GRPC',
      long_description=readme(),
      url='http://github.com/storborg/notfound',
      author='Dinesh RVL',
      author_email='dineshlakshmanan1990@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=['grpcrest'],
      entry_points = {
        'console_scripts': ['start-grpc-rest=grpcrest.grpc_rest:main'],
        },
      install_requires=[
          'flask',
      ],
      zip_safe=False)
