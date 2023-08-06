from setuptools import setup

name = "types-pyinstaller"
description = "Typing stubs for pyinstaller"
long_description = '''
## Typing stubs for pyinstaller

This is a PEP 561 type stub package for the `pyinstaller` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyinstaller`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyinstaller. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `ca13bcc286d0ee672bd55f1c3ca79cefb8a47ad5` and was tested
with mypy 1.3.0, pyright 1.1.315, and
pytype 2023.6.2.
'''.lstrip()

setup(name=name,
      version="5.13.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyinstaller.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-setuptools'],
      packages=['PyInstaller-stubs', 'pyi_splash-stubs'],
      package_data={'PyInstaller-stubs': ['__init__.pyi', '__main__.pyi', 'building/__init__.pyi', 'building/api.pyi', 'building/build_main.pyi', 'building/datastruct.pyi', 'building/splash.pyi', 'compat.pyi', 'depend/__init__.pyi', 'depend/analysis.pyi', 'depend/imphookapi.pyi', 'isolated/__init__.pyi', 'isolated/_parent.pyi', 'lib/__init__.pyi', 'lib/modulegraph/__init__.pyi', 'lib/modulegraph/modulegraph.pyi', 'utils/__init__.pyi', 'utils/hooks/__init__.pyi', 'utils/hooks/conda.pyi', 'utils/hooks/win32.pyi', 'utils/win32/versioninfo.pyi', 'utils/win32/winmanifest.pyi', 'METADATA.toml'], 'pyi_splash-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
