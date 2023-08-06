from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='grpcrest',
      version='0.3',
      description='REST Wrapper for GRPC',
      url='http://github.com/storborg/notfound',
      author='Dinesh RVL',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['grpcrest'],
      entry_points = {
        'console_scripts': ['start-grpc-rest=grpcrest.grpc_rest:main'],
        },
      install_requires=[
          'flask',
      ],
      zip_safe=False)
