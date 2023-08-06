from setuptools import setup, find_packages

setup(name="mess_clients",
      version="0.1.1",
      description="mess_clients",
      author="Artem Gladkov",
      author_email="2020artem@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
