An add-on to provide a full-featured **cookie consent** solution for your site.
It's mainly target to the recent `European Cookie Law`_ but can be used anywhere if you care about user's privacy.

.. contents:: **Table of contents**

How it works
============

This add-on gives two kind of different features:

* A cookie consent confirmation banner, which should link (but it's not required) the user to a **Privacy Policy**.
* An **opt-out dashboard** for accept/reject single cookies

This add-on is also compatible with internationalized sites (`LinguaPlone`_ supported).

Cookie consent banner
---------------------

This is provided using a slightly modified version of the `Silktide Cookie Consent JavaScript plugin`_

.. image:: https://raw.githubusercontent.com/PloneGov-IT/rer.cookieconsent/master/docs/images/rer.cookieconsent-0.1.0-01.png
   :alt: Cookie consent banner

Apart some accessibility enhancement (see `here`__, `here`__, `here`__ and `here`__) it's content and
behavior can be customized by a control panel. 

__ https://github.com/silktide/cookieconsent2/issues/59
__ https://github.com/silktide/cookieconsent2/issues/60
__ https://github.com/silktide/cookieconsent2/issues/61
__ https://github.com/silktide/cookieconsent2/issues/63

Opt-out dashboard
-----------------

Additionally an opt-out dashboard (a view callable as ``/@@optout-dashboard``) is available to restricts 3rd-party cookies.

The dashboard composition can be configured by the control panel, but is above che scope of this add-on to manage
how those cookies are processed.
Third-party party add-ons must take care of this.

A cookie is always in the form ``NAME-optout`` and can have a value equals to ``true`` or ``false``.

Know add-ons which support opt-out cookies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here follow a list of common add-ons that can be used with opt-out cookies:

`sc.social.like`_ (version >= 2.3) - server side
   A cookie named ``social-optout`` valued to ``true`` will automatically activate the
   "*Do not track users*" option for the current user. 
`collective.analyticspanel`_ (version >= 0.5.0) - server side
   If properly configure, a cookie named ``analytics-optout`` valued to ``true`` will not load the analytics code.
   Although the add-on works server side, you are free to provide an analytics code that conditionally load when
   this cookie is present working totally on client side.
`Products.Maps`_ (version >= 0.4) - client side
   If a cookie named ``maps-optout`` is provided valued to ``true`` the Google map is not directly displayed in the page.
`redturtle.video`_ (version >= 1.2.0) - server side
   Not directly RedTurtle Video, but extensions like `collective.rtvideo.youtube`_ (>=0.4.0)
   and `collective.rtvideo.vimeo`_ (>=0.3.0) will not display the video directly if a ``video-optout`` cookie valued
   ``true`` is provided

Configuration
=============

Add-on configuration can be reached from the "*Cookie consent configuration*" entry in the Plone control panel.

Cookie consent banner
---------------------

In the banner configuration you can:

* activate an auto-grant-on-click feature. With this every click on whatever link in the site is interpreted
  as accepting the Privacy Policy  
* Customizing the banner text for every language used in the site (not required if your site use a single language).

.. image:: https://raw.githubusercontent.com/PloneGov-IT/rer.cookieconsent/master/docs/images/rer.cookieconsent-0.1.0-02.png
   :alt: Cookie consent banner - configuration

The banner text will normally contains a link to the Privacy Policy.

Opt-out dashboard
-----------------

The opt-out dashboard configuration is only needed if you are using 3rd party add-ons or external software that
handle opt-out cookies.

Configuring this panel will select which cookies must the available to the user's preferences.

You must provide:

* an application id
* a list of one or more prefix, used for build cookies name
* a title and description for describing to users how this opt-out works if activated.
  Again: you can provide a description for every involed language

.. image:: https://raw.githubusercontent.com/PloneGov-IT/rer.cookieconsent/master/docs/images/rer.cookieconsent-0.1.0-03.png
   :alt: Opt-out dashboard - configuration

Issues/Troubleshooting
======================

Varnish
-------

TODO

Control panel
-------------

TODO

HttpOnly
--------

TODO

Credits
=======

Developed with the support of `Regione Emilia Romagna`__;
Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/


.. _`European Cookie Law`: http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32009L0136
.. _`LinguaPlone`: https://pypi.python.org/pypi/Products.LinguaPlone
.. _`Silktide Cookie Consent JavaScript plugin`: https://silktide.com/tools/cookie-consent/
.. _`sc.social.like`: https://pypi.python.org/pypi/sc.social.like/
.. _`collective.analyticspanel`: https://pypi.python.org/pypi/collective.analyticspanel
.. _`Products.Maps`: https://pypi.python.org/pypi/Products.Maps
.. _`redturtle.video`: https://plone.org/products/redturtle.video
.. _`collective.rtvideo.youtube`: https://pypi.python.org/pypi/collective.rtvideo.youtube
.. _`collective.rtvideo.vimeo`: https://pypi.python.org/pypi/collective.rtvideo.vimeo
