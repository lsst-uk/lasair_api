# FAQs

```eval_rst
.. todo::

    - Clean up these FAQs after web refresh
```

**Table of Contents**

{{TOC}}

## What are Lasair-ZTF and Lasair-LSST?

Lasair is an evolving platform. The current Lasair-ZTF is our prototype broker based on the ZTF alert stream, but we have started an intensive planning and technical reviews of the requirements for LSST. We are basing our future requirements on two key LSST documents: [Data Products Definition Document (Juric et al. 2019)](https://lse-163.lsst.io/) and [LSST Alerts: Key Numbers (Graham et al.)](https://dmtn-102.lsst.io/DMTN-102.pdf).

We envisage the following major differences between Lasair-ZTF and Lasair-LSST :

*   the increase in rate of the number of alerts, by a factor 50
*   the multi-colour filter nature of LSST of *ugrizy*,
*   the different surveys : deep drilling fields, wide-fast deep (which may end up splitting the Milky Way from the extragalactic sky), and any additional approved mini-surveys (e.g. target of opportunity observations of gravitational wave sky maps).
*   access to forced photometry and the timescales for that access a deep image of the whole survey footprint which has photometric redshifts and accurate star-galaxy separation for all objects
*   expected large increase in the user base
*   provision to link pubic spectroscopic data to the LSST transients. Both the information derived from the spectra such as type and redshift, but also the data itself.

Given these differences, within Lasair we are reviewing the database architecture and how the lightcurve data are annotated, stored and made available to users. We have developed detailed Science Requirements from the perspective of expert users within the UK and are working particularly with the LSST Science Collaborations (DESC and TVS) to review these. Our main focus is to provide a broker that will allow users to find their transients and eruptive variables of choice and to run filters or analysis code on them. This may be on the Lasair computing platform (the UK's IRIS system) but we will also provide means to bulk download lightcurve data for users to work with locally on their own machines.

This work is intensifying as of April 2020, and we look forward to working with our international colleagues across the LSST community and within the LSST Science Collaborations to define Lasair's functionality for LSST. With this in mind, we are drafting our broker proposal for the June call.

What can I get from this web site?

The Lasair alert broker gives access to millions of astronomical transient detections: when a star or galaxy becomes brighter or fainter than it was at an earlier time.

## What data does Lasair offer?

Whenever a star or galaxy in the sky changes brightness, it is given an "objectId", which can be used to see all the data about that object. Data includes a "light curve" of brightness measurments at different times, in different filters; crossmatching with existing source catalogs, and other data.

## What is here for an amateur astronomer?

A serious amateur telescope would have a 500 mm aperture, with a limiting magnitude of about 16, costing over $40,000. In any year there will be a few supenovae visible to this system.

## How can I ask a question to the Lasair team?

Write to the help email: lasair-help at lists.lasair.roe.ac.uk.

## How can I use my knowledge of SQL to use Lasair?

Each query/filter/stream in Lasair is an SQL SELECT query. The syntax is "SELECT <attributes\> FROM <tables\> WHERE <conditions;\>" The attributes come from the schema -- shown to the right in the query builder page, and can include renaming, for example "magg-magr as mag\_difference", but no sub-queries. The tables are selected from objects, sherlock\_classifications, crossmatch\_tns, as well as any watchlists or areas you choose. The conditions in the WHERE clause allow a simplified SQL, using just comparison operators, without operators such as "group" and "having".

## How can I query the Lasair database?

You can type SQL into the query builder as above, and you can run a query somebody else has made that is public. If you sign up and login to Lasair, you can save your queries and you can copy somebody else's query then modify it.

## What is the difference between a Query and a Filter?

A query operates on the whole database of alerts, but a Filter only runs on new alerts, as they stream from the telescope. You can convert a Query that you own to a Filter in the query builder page.

## What is the schema of the Lasair database?

Can be found at the [schema page](https://lasair-ztf.lsst.ac.uk/schema).

## How do I choose which alerts are interesting to me?

Choosing interesting alerts can be based on several criteria: The characteristics of the light curve; coinicdence of the alert with a galaxy or known variable star; coincidence of the alert with one of the sources in which you are interested (a watchlist); location of the alert in a given area of the sky, for example a gravitational wave skymap.

## Why should I register on the Lasair website?

Registration is easy, and just requires a valid email (signup [here](https://lasair-ztf.lsst.ac.uk/signup)). You can then build and save queries, watchlists, and sky areas, convert those to real-time slert treams, and use the Lasair API.

## Besides Lasair, what other websites carry astronommical transients?

There are seven community brokers that will receive and process LSST alerts in real time: [ALeRCE](http://alerce.science/), [AMPEL](https://ampelproject.github.io/), [ANTARES](https://antares.noirlab.edu/), BABAMUL, [Fink](https://fink-broker.re%3Cdthedocs.io/en/latest/), [Lasair](https://lasair.roe.ac.uk/), and [Pitt-Google](https://pitt-broker.re%3Cdthedocs.io/en/latest/).

## How long has Lasair been operating?

Lasair has been processing, storing, and distributing alerts from the ZTF survey since 2018.

Can I get alerts from a particular region of the sky?

Lasair supports "sky areas", defined by a [MOC](https://cds-astro.github.io/mocpy/), that you build yourself.

Can I get alerts associated with my favourite sources?

You can build a "watchlist" of your favourite sources, and build a corresponding query that includes crossmatch with that watchlist. Instructions are [here](https://lasair-ztf.lsst.ac.uk/cookbook/watchlist/).

## Can Lasair alert me about supernovae and kilonovae?

There are some filters already built that find alerts in the outskirts of galaxies, see [here](https://lasair-ztf.lsst.ac.uk/querylist/promoted/). There are also queries that find supernovae already reported to the [Transient Name Service](https://www.wis-tns.org/).

## Can Lasair alert me about gravitational-wave events?

Lasair receives immediate notification of gravitational wave alerts. See [here](https://lasair-ztf.lsst.ac.uk/skymap)

How can I find out about the ZTF survey?

The Zwicky Transient Factory (ZTF) is the source of the events to which Lasair provides access. It is well summarised with the following set of papers:

*   _The Zwicky Transient Facility: Data Processing, Products, and Archive_, F. Masci et al [arXiv](https://arxiv.org/abs/1902.01872)
*   _The Zwicky Transient Facility: System Overview, Performance, and First Results_, E. Bellm et al [arXiv](https://arxiv.org/abs/1902.01932)
*   _A Morphological Classification Model to Identify Unresolved PanSTARRS1 Sources: Application in the ZTF Real-Time Pipeline_, Y. Tachibana et al, [arXiv](https://arxiv.org/abs/1902.01935)
*   _Machine Learning for the Zwicky Transient Facility_, A. Mahabal et al, [arXiv](https://arxiv.org/abs/1902.01936)
*   _The Zwicky Transient Facility: Science Objectives_, M. Graham et al, [arXiv](https://arxiv.org/abs/1902.01945)
*   _The Zwicky Transient Facility Alert Distribution System_, M. Patterson et al [arXiv](https://arxiv.org/abs/1902.02227)

## How can I find out about the LSST survey and the Vera Rubin Observatory?

General FAQ on LSST and Rubin is [here](https://www.lsst.org/content/rubin-observatory-general-public-faqs), about community alert brokers in particular [here](https://www.lsst.org/scientists/alert-brokers)

## How can I write code and notebooks that use the Lasair database?

The documentation is [here](https://lasair-ztf.lsst.ac.uk/code)

## How can I mine a million Lasair light curves?

Lorem Ipsum

## Does Lasair classify alerst into classes?

Lorem Ipsum

## Does Lasair have an API?

Lorem Ipsum

## What is difference magnitude compare to apparent magnitude?

Lorem Ipsum

## What is an exponantial moving average?

Lorem Ipsum

## What is a cone-search and can Lasair do this?

Lorem Ipsum

## How can I do 1000 cone searches all at once?

Lorem Ipsum

## What is associated (cross-matched) with a Lasair source?

Lorem Ipsum

## Can I see sky images in different wavelengths around a Lasair alert?

Lorem Ipsum

## When I make a query, can I share it with my colleagues?

Lorem Ipsum

## Can I get immediate notification of interesting alerts?

Lorem Ipsum
