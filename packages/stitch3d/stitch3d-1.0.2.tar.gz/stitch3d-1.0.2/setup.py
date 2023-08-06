import setuptools
from setuptools import Extension, dist, find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
      'torch>=1.6.0, <=1.13.1',
      'scanpy==1.7.2',
      'anndata==0.7.6',
      'pandas==1.1.5',
      'numpy>=1.19.0',
      'leidenalg>=0.7.0',
      'umap-learn>=0.4.6',
      'pot>=0.8.0',
      'numba>=0.49.1',
      'matplotlib<3.7',
      'louvain'
]
setup(name='stitch3d',
      version='1.0.2',
      description='A computational method for tissue 3D reconstruction by joint modeling of multiple spatial transcriptomics slices.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/YangLabHKUST/STitch3D',
      author='Gefei Wang',
      author_email='gwangas@connect.ust.hk',
      license='MIT',
      packages=['STitch3D'],
      install_requires=install_requires,
      zip_safe=False,
      python_requires='>=3.7',)