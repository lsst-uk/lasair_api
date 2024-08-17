# Watchlists

**Table of Contents**

{{TOC}}

## Static Watchlists


```eval_rst
.. todo::

    - Flesh out how to use static watchlists ... text below is from old pages
```

## Create new watchlist

A watchlist is a set of points in the sky, together with a radius in arcseconds. It is assumed to be a list of "interesting" sources, so that any transient that falls within the radius of one of the sources might indicate activity of that source. Each user of the Lasair system has their own set of watchlists, and can be alerted when a ZTF transient is coincident with a watchlist source.

You can create a watchlist of sources by preparing a text file, where each comma-separated or |-separated line has RA and Dec in decimal degrees, an identifier, with optional radius in arcseconds. One way to do this is with [Vizier](http://vizier.u-strasbg.fr/viz-bin/VizieR) and a spreadsheet program such as Excel or Numbers. Here is [an example of the data](https://lasair-ztf.lsst.ac.uk/lasair/static/BLLac.txt). The 42 entries are _BL Lac candidates for TeV observations (Massaro+, 2013)_

An "Active" watchlist is one that is run every day, so that it is up to date with the latest objects.

You must be logged in to create a watchlist

### Build a Watchlist of your sources

Many astronomers are interested in transients that are associated with specific astronomical objects, perhaps active galaxies or star formation regions. Once you have an account on Lasair, you can create any number of watchlists, to be used in the query engine. To be specific, suppose we are interested in the 42 objects in the catalogue BL Lac candidates for TeV observations (Massaro+, 2013), that can be found in the Vizier library of catalogues. You can make your watchlist “public”, so other Lasair users can see it and use it in queries, and you can make your watchlist “active”, meaning that the crossmatch (see below) is done automatically every day.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig1.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig1.png)

How to use the Vizier interface to get suitable data to upload. Once you have your catalogue,

*   deselect all the columns
*   select a column that can act as the ID for each source. These need to be unique and not empty: if not, you must edit the resulting file to make it so.
*   Choose “Decimal” for the coordinates
*   Choose “|-separated” for the format
*   Click submit to download the file.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig2.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig2.png)

Fill in the name and description of the watchlist. Choose a default value of the radius to use in matching, in arcseconds. Open the file and paste the contents. Each line should be RA, Dec, ID, and may have a fourth entry, the radius to use in matching, in arcseconds, if different from the default. Then click “Submit Form”.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig3.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig3.png)

Here is a successful creation of a watchlist. Some messages – “Bad line” – because there were some lines without data, but you can ignore these, and look for where it says “Watchlist created successfully”. You can now find it in the list of “My Watchlists”.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig4.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/watchlist/fig4.png)

Click on any of your watchlists, and look for the button “Run Crossmatch”. This finds all the transients that are within the radius of any of the sources of the watchlist. The left four columns come from your input, and the right four from the Lasair crossmatch. There is a clickable objectId, the number of candidates of that object, and other information.

### Find outbursts from my watchlist

Once you have made a watchlist, you may be interested in being notified whenever something unusual – outburst for example – happens to one of your sources. Thus we combine a watchlist with a query on magnitude that detects fast rise. For the watch list see Build a Watchlist of your sources, and for the query we utilise the moving averages of apparent magnitudes that Lasair provides. See this paper for more information.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig1.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig1.png)

For this example, we use a watchlist of 56 AM CVn stars, which are binaries of compact object (eg white dwarf) with a very short orbit – less than an hour. This screenshot shows a recent crossmatch of the watchlist with ZTF.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig2.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig2.png)

This is the active query, that builds a Kafka stream, and joins the object table with the watchlist shown above. The selection criterion at the bottom looks for a magnitude difference between the 2-day moving average (latest\_dc\_mag\_g02), and the 28-day moving average (latest\_dc\_mag\_g28), and requires a difference of at least 0.5 magnitude in both g and r.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig3.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig3.png)

Here is some output from the query in a period of 6 days. The same object appears several times (SDSS J1240-0159).

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig4.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/outbursts/fig4.png)

We see in the light curve the brightening by 5 magnitudes. Make sure you select the “Apparent Magnitude”, which are more more suitable for variable star work.

### Get real-time alerts from ZTF

The Lasair broker can send immediate “push” notifications when your active query/filter sees and interesting alert. Here is how to make that happen with email notification. First make sure you are logged in to your Lasair account (top left of screen, then go to create new stored query. This page is about how to get email alerts from your active query; the process is very similar for Kafka alerts, except that you will fetch the results by machine instead of by email. See article Reading a Kafka Stream.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig1.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig1.png)

Fill in the form as shown here. Name and description, then check the “email” box, and fill in the SELECT as

objects.objectId, objects.latestrmag, jdnow()-objects.jdmax as since

check the “objects” table, and fill in the WHERE as

objects.latestrmag < 12

Then click “Create Query”

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig2.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig2.png)

Nothing will happen immediately. You can run the query in the usual way from the web browser, but you will have to wait for some alerts to arrive before your active query will be triggered. Once that happens, you will get an email at the address you used to create your account. Something like the message shown here. Note that the attributes you chose above are reported (objectId, latestrmag, since), together with the UTC time at which the alert was triggered.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig3.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig3.png)

In addition to the email, the webserver holds the last 1000 alerts that went to this channel. The link is in your list of queries.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig4.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/realtimealerts/fig4.png)

Click on that link and it will show you a page like this one.

## Smart Watchlists

