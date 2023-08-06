.. image:: https://img.shields.io/pypi/v/backports.datetime_timestamp.svg
   :target: https://pypi.org/project/backports.datetime_timestamp

.. image:: https://img.shields.io/pypi/pyversions/backports.datetime_timestamp.svg

.. image:: https://github.com/jaraco/backports.datetime_timestamp/workflows/tests/badge.svg
   :target: https://github.com/jaraco/backports.datetime_timestamp/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/PROJECT_RTD/badge/?version=latest
..    :target: https://PROJECT_RTD.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2023-informational
   :target: https://blog.jaraco.com/skeleton

Backport of the `datetime.timestamp()
<http://docs.python.org/3.3/library/datetime.html#datetime.datetime.timestamp>`_ method added in Python 3.3.

Used as::

    from backports.datetime_timestamp import timestamp
    import datetime

    dt = datetime.datetime.utcnow()
    # instead of dt.timestamp(), use
    timestamp(dt)
