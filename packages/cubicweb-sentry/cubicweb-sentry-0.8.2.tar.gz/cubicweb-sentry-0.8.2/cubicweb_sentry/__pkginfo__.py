# pylint: disable=W0622
"""cubicweb-sentry application packaging information"""

modname = "sentry"
distname = "cubicweb-sentry"

numversion = (0, 8, 2)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "support for Sentry (getsentry.com)"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]

__depends__ = {"cubicweb": ">= 3.38.9, < 3.39.0", "sentry-sdk": "<1.26.0"}
__recommends__ = {}
