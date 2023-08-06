from setuptools import setup, Extension


setup(
    name='dequeai',
    version='0.00000800',
    description='Python Package for DEQUE AI Platform',
    author="The DEQUE AI Team",
    author_email='team@deque.app',
    packages=["dequeai"],
    url='https://dequeapp-deque.gitbook.io/deque-docs/getting-started/dequeai-experiment-tracking',
    keywords='deque client for experiment tracking, sweep and other deep learning tooling',
    install_requires=[
          "coolname","requests","numpy","pillow","psutil","GPUtil","ipython","tabulate"
      ],
)