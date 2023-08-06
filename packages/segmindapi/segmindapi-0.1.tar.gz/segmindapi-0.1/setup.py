from setuptools import setup

setup(name='segmindapi',
      version='0.1',
      description='Package for Using Segmind APIs in Python',
      url='https://docs.segmind.com/apis',
      author='Yatharth Gupta',
      license='MIT',
      packages=['segmindapi'],
      author_email='yatharth1.g@gmail.com',
      install_requires=[
          'pillow',
      ],
      zip_safe=False)