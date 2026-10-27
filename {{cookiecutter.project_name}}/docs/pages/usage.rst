Usage
=====

Import the package using its Python module name:

.. code-block:: python

   import {{ cookiecutter.project_name.lower().replace('-', '_') }}

   # Use the library's public API here.

The installed package exposes its version metadata:

.. doctest::

   >>> from {{ cookiecutter.project_name.lower().replace('-', '_') }}.__metadata__ import __version__
   >>> isinstance(__version__, str)
   True
