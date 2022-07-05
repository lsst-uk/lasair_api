# Sky Regions

**Table of Contents**

{{TOC}}

```eval_rst
.. todo::

    - Flesh out how to use the sky region maps ... text below is from old pages
```

The current list of available skymaps is shown at https://lasair.roe.ac.uk/skymap/. It is a much longer list than when the page was designed. Below is a typical example.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig1.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig1.png)

The name of the GW skymap comes from the official LVC sources, as linked from the header test (top red oval). Now look at the distance, and the event-type. A BNS (binary neutron star) event at a "near" location (less than 100 mega-parsecs) would be most exciting, as there would be a good chance for optical and other telescopes to identify it. Below we describe how the three checkboxes in the green box can provide further information.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig2.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig2.png)

The lower display shows the probability distribution of where in the sky the GW source was. The AladinLite display allows arbitrary zoom and many different sky layers from gamma to radio. The contour lines of the probability are percentiles. Red outside: 90%, and violet inside: 10%. There is also a list of galaxies and the probability each has the counterpart. This is great for the nearby event (50 Mpc) but when the event is at 1000 Mpc, there are galaxies everywhere, and the list is no help.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig3.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig3.png)

The checkbox "Show galaxies from GLADE" puts a yellow square around each galaxy where the GW counterpart might be found. From the GLADE catalogue, they are selected for sky probability and the distance estimate in the skymap. However a maximum of 200 galaxies are shown, there may be many more for a distant source. Choose the PanSTARRS layer, and zoom in. Doubleclick in a yellow square to centre the image in the source, then use the "+" zoom icon at the right. There is also a link to the galaxy data next to the checkbox.

[![](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig4.png)](https://lasair-ztf.lsst.ac.uk/lasair/static/cookbook/skymaps/fig4.png)

The checkbox about ZTF candidates show all candidates in the 90%, and are within the given time constraint in the form - days before and days after the GW event. It may be slow when you click submit as there may be 1000s of candidates. You can zoom in and click on one of them, and a link pops up that can take you to that object's page.



