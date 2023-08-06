.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.


====================================
collective.abovecontenttitleportlets
====================================

Show portlets above the content body.


Features
--------

- Plone 6 has left/right/footer portlets.  This package adds abovecontenttitle portlets.
- They show above the title.

If you want a portlet slot between the content title/description and the content instead,
use `collective.abovecontentbodyportlets <https://github.com/collective/collective.abovecontentbodyportlets>`_.


Installation
------------

Install collective.abovecontenttitleportlets by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.abovecontenttitleportlets


and then running ``bin/buildout``, starting Plone, and activating it in the Modules control panel.


Contributors
------------

Put your name here, you deserve it!

- Maurits van Rees


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.abovecontenttitleportlets/issues
- Source Code: https://github.com/collective/collective.abovecontenttitleportlets


License
-------

The project is licensed under the GPLv2.
