# Transient Metadata Tags


```eval_rst
.. todo::

    - Clean up this metadata tag page ... text below is from old pages
```

**Table of Contents**

{{TOC}}

## What are Metadata Tags?

## Sherlock

Detections in the input data stream that have been aggregated into _objects_ (i.e. groups of detections) and identified as static transients (i.e. not moving objects) are spatially context classified against a large number of archival sources (e.g. nearby galaxies, known CVs, AGNs, etc). The information derived from this context check is injected as an object annotation (e.g. see Lasair object page example below). The software used is called _Sherlock_ and is discussed below.

_Sherlock_ is a software package and integrated massive database system that provides a rapid and reliable spatial cross-match service for any astrophysical variable or transient. The concept originated in the PhD thesis of D. Young at QUB, and has been developed by Young et al. in many iterations and cycles since. It associates the position of a transient with all major astronomical catalogues and assigns a basic classification to the transient. At its most basic, it separates stars, AGN and supernova-like transients. It has been tested within QUB on a daily basis with ATLAS and Pan-STARRS transients, and within PESSTO as part of the PESSTO marshall system that allows prioritising of targets. It is thus a boosted decision tree algorithm. A full paper describing the code, catalogues and algorithms is in preparation (Young et al. in prep). A summary is included in Section 4.2 of "Design and Operation of the ATLAS Transient Science Server" (Smith, Smartt, Young et al. 2020, submitted to PASP: [https://arxiv.org/abs/2003.09052](https://arxiv.org/abs/2003.09052)). We label the current version as the official release of Sherlock 2.0. The major upgrade from previous versions are that it includes Pan-STARRS DR1 (including the Tachibana & Miller 2018 star-galaxy separation index) and Gaia DR2 catalogues, along with some adjustments to the ranking algorithm.

**That section is copied here and users should currently cite that paper ([Smith et al. 2020](https://arxiv.org/abs/2003.09052)) for _Sherlock_ use:**

A boosted decision tree algorithm (internally known as _Sherlock_) mines a library of historical and on-going astronomical survey data and attempts to predict the nature of the object based on the resulting crossmatched associations found. One of the main purposes of this is to identify variable stars, since they make up about 50% of the objects, and to associate candidate extragalactic sources with potential host galaxies. The full details of this general purpose algorithm and its implementation will be presented in an upcoming paper (Young et al. in prep), and we give an outline of the algorithm here.

The library of catalogues contains datasets from many all-sky surveys such as the major Gaia DR1 and DR2 (Gaia Collaboration et al. 2016, 2018), the Pan-STARRS1 Science Consortium surveys (Chambers et al. 2016; Magnier, Chambers, et al. 2016; Magnier, Sweeney, et al. 2016; Magnier, Schlafly, et al. 2016; Flewelling et al. 2016) and the catalogue of probabilistic classifications of unresolved point sources by (Tachibana and Miller 2018) which is based on the Pan-STARRS1 survey data. The SDSS DR12 PhotoObjAll Table, SDSS DR12 SpecObjAll Table (Alam et al. 2015) usefully contains both reliable star-galaxy separation and photometric redshifts which are useful in transient source classification. Extensive catalogues with lesser spatial resolution or colour information that we use are the GSC v2.3 (Lasker et al. 2008) and 2MASS catalogues (Skrutskie et al. 2006). _Sherlock_ employs many smaller source-specific catalogues such as Million Quasars Catalog v5.2 (Flesch 2019), Veron-Cett AGN Catalogue v13 (Véron-Cetty and Véron 2010), Downes Catalog of CVs (Downes et al. 2001), Ritter Cataclysmic Binaries Catalog v7.21 (Ritter and Kolb 2003). For spectroscopic redshifts we use the GLADE Galaxy Catalogue v2.3 (Dálya et al. 2018) and the NED-D Galaxy Catalogue v13.1[1](https://lasair-ztf.lsst.ac.uk/sherlock#fn1). _Sherlock_ also has the ability to remotely query the NASA/IPAC Extragalactic Database, caching results locally to speed up future searches targeting the same region of sky, and in this way we have built up an almost complete local copy of the NED catalogue. More catalogues are continually being added to the library as they are published and become publicly available.

At a base-level of matching _Sherlock_ distinguishes between transient objects _synonymous_ with (the same as, or very closely linked, to) and those it deems as merely _associated_ with the catalogued source. The resulting classifications are tagged as _synonyms_ and _associations_, with synonyms providing intrinsically more secure transient nature predictions than associations. For example, an object arising from a variable star flux variation would be labeled as _synonymous_ with its host star since it would be astrometrically coincident (assuming no proper motion) with the catalogued source. Whereas an extragalactic supernova would typically be _associated_ with its host galaxy - offset from the core, but close enough to be physically associated. Depending on the underpinning characteristics of the source, there are 7 types of predicted-nature classifications that Sherlock will assign to a transient:

1.  **Variable Star** (VS) if the transient lies within the synonym radius of a catalogued point-source,
    
2.  **Cataclysmic Variable** (CV) if the transient lies within the synonym radius of a catalogued CV,
    
3.  **Bright Star** (BS) if the transient is not matched against the synonym radius of a star but is associated within the magnitude-dependent association radius,
    
4.  **Active Galactic Nucleus** (AGN) if the transient falls within the synonym radius of catalogued AGN or QSO.
    
5.  **Nuclear Transient** (NT) if the transient falls within the synonym radius of the core of a resolved galaxy,
    
6.  **Supernova** (SN) if the transient is not classified as an NT but is found within the magnitude-, morphology- or distance-dependant association radius of a galaxy, or
    
7.  **Orphan** if the transient fails to be matched against any catalogued source.
    

For Lasair the synonym radius is set at 1.5″. This is the crossmatch-radius used to assign predictions of VS, CV, AGN and NT. The process of attempting to associate a transient with a catalogued galaxy is relatively nuanced compared with other crossmatches as there are often a variety of data assigned to the galaxy that help to greater inform the decision to associate the transient with the galaxy or not. The location of the core of each galaxy is recorded so we will always be able to calculate the angular separation between the transient and the galaxy. However we may also have measurements of the galaxy morphology including the angular size of its semi-major axis. For Lasair we reject associations if a transient is separated more than 2.4 times the semi-major axis from the galaxy, if the semi-major axis measurement is available for a galaxy. We may also have a distance measurement or redshift for the galaxy enabling us to convert angular separations between transients and galaxies to (projected) physical-distance separations. If a transient is found more than 50 Kpc from a galaxy core the association is rejected.

Once each transient has a set of independently crossmatched synonyms and associations, we need to self-crossmatch these and select the most likely classification. The details of this will be presented in a future paper (Young et al. in prep). Finally the last step is to calculate some value added parameters for the transients, such as absolute peak magnitude if a distance can be assigned from a matched catalogued source, and the predicted nature of each transient is presented to the user along with the lightcurve and other information (see Figure [1](https://lasair-ztf.lsst.ac.uk/sherlock#fig:webcandidatepage2019tua)).

We have constructed a multi-billion row database which contains all these catalogues. It currently consumes about 4.5TB and sits on a separate, similarly specified machine to that of the Lasair database. It will grow significantly as new catalogues are added (e.g. Pan-STARRS 3_π_ DR2, VST and VISTA surveys, future Gaia releases etc).

![Lasair object page. Non-detections are shown as faint diamonds, which display the 5\sigma limiting magnitude. The object was context classified as a SN by Sherlock, and (probable) host annotations are highlighted in the red box. ](https://lasair-ztf.lsst.ac.uk/lasair/static/img/Lasair_object.png)

**Lasair object page.** Non-detections are shown as faint diamonds, which display the 5_σ_ limiting magnitude. The object was context classified as a SN by _Sherlock_, and (probable) host annotations are highlighted in the red box.

The _Sherlock_ code is open source and can be found at: [https://github.com/thespacedoctor/sherlock](https://github.com/thespacedoctor/sherlock). Documentation is also available online here: [https://qub-sherlock.readthedocs.io/en/stable/](https://qub-sherlock.readthedocs.io/en/stable/).

Although the code for _Sherlock_ is public, it requires access to a number of large databases which are custom built from their original, public, releases. The latter is proprietary and therefore would require some effort from users to reproduce. As part of the Lasair project we are exploring public access to the integrated _Sherlock_ code and database information through an API.

Sherlock 2.0 was reviewed as a LSST:UK Deliverable in March 2020. The review noted that an algorithm enhancement would be desirable to take into account stellar proper motions, since some proper motion stars will be variable and if cross-matched with a static catalogue will fall outside the nominal match radius. This is an enhancement we will taken forward for future versions.

##### References

Alam, Shadab, Franco D Albareti, Carlos Allende Prieto, F Anders, Scott F Anderson, Timothy Anderton, Brett H Andrews, et al. 2015. “The Eleventh and Twelfth Data Releases of the Sloan Digital Sky Survey: Final Data from SDSS-III.” _The Astrophysical Journal Supplement Series_ 219 (1). IOP Publishing: 12. [https://doi.org/10.1088/0067-0049/219/1/12](https://doi.org/10.1088/0067-0049/219/1/12).

Chambers, K. C., E. A. Magnier, N. Metcalfe, H. A. Flewelling, M. E. Huber, C. Z. Waters, L. Denneau, et al. 2016. “The Pan-STARRS1 Surveys.” _ArXiv E-Prints_, December.

Dálya, G, G Galgóczi, L Dobos, Z Frei, I S Heng, R Macas, C Messenger, P Raffai, and R S de Souza. 2018. “GLADE: A galaxy catalogue for multimessenger searches in the advanced gravitational-wave detector era.” _Monthly Notices of the Royal Astronomical Society_ 479 (2): 2374–81. [https://doi.org/10.1093/mnras/sty1703](https://doi.org/10.1093/mnras/sty1703).

Downes, Ronald A, Ronald F Webbink, Michael M Shara, Hans Ritter, Ulrich Kolb, and Hilmar W Duerbeck. 2001. “A Catalog and Atlas of Cataclysmic Variables: The Living Edition.” _The Publications of the Astronomical Society of the Pacific_ 113 (7): 764–68. [https://doi.org/10.1086/320802](https://doi.org/10.1086/320802).

Flesch, Eric W. 2019. “The Million Quasars (Milliquas) Catalogue, v6.4.” _arXiv.org_, December, arXiv:1912.05614. [http://arxiv.org/abs/1912.05614v1](http://arxiv.org/abs/1912.05614v1).

Flewelling, H. A., E. A. Magnier, K. C. Chambers, J. N. Heasley, C. Holmberg, M. E. Huber, W. Sweeney, et al. 2016. “The Pan-STARRS1 Database and Data Products.” _ArXiv E-Prints_, December.

Gaia Collaboration, A. G. A. Brown, A. Vallenari, T. Prusti, J. H. J. de Bruijne, C. Babusiaux, C. A. L. Bailer-Jones, et al. 2018. “Gaia Data Release 2. Summary of the contents and survey properties” 616 (August): A1. [https://doi.org/10.1051/0004-6361/201833051](https://doi.org/10.1051/0004-6361/201833051).

Gaia Collaboration, A. G. A. Brown, A. Vallenari, T. Prusti, J. H. J. de Bruijne, F. Mignard, R. Drimmel, et al. 2016. “Gaia Data Release 1. Summary of the astrometric, photometric, and survey properties” 595 (November): A2. [https://doi.org/10.1051/0004-6361/201629512](https://doi.org/10.1051/0004-6361/201629512).

Lasker, Barry M, Mario G Lattanzi, Brian J McLean, Beatrice Bucciarelli, Ronald Drimmel, Jorge Garcia, Gretchen Greene, et al. 2008. “The Second-Generation Guide Star Catalog: Description and Properties.” _The Astronomical Journal_ 136 (2). IOP Publishing: 735–66. [https://doi.org/10.1088/0004-6256/136/2/735](https://doi.org/10.1088/0004-6256/136/2/735).

Magnier, E. A., K. C. Chambers, H. A. Flewelling, J. C. Hoblitt, M. E. Huber, P. A. Price, W. E. Sweeney, et al. 2016. “Pan-STARRS Data Processing System.” _ArXiv E-Prints_, December.

Magnier, E. A., E. F. Schlafly, D. P. Finkbeiner, J. L. Tonry, B. Goldman, S. Röser, E. Schilbach, et al. 2016. “Pan-STARRS Photometric and Astrometric Calibration.” _ArXiv E-Prints_, December.

Magnier, E. A., W. E. Sweeney, K. C. Chambers, H. A. Flewelling, M. E. Huber, P. A. Price, C. Z. Waters, et al. 2016. “Pan-STARRS Pixel Analysis : Source Detection & Characterization.” _ArXiv E-Prints_, December.

Ritter, H, and U Kolb. 2003. “Catalogue of cataclysmic binaries, low-mass X-ray binaries and related objects (Seventh edition).” _Astronomy and Astrophysics_ 404 (1). EDP Sciences: 301–3. [https://doi.org/10.1051/0004-6361:20030330](https://doi.org/10.1051/0004-6361:20030330).

Skrutskie, M. F., R. M. Cutri, R. Stiening, M. D. Weinberg, S. Schneider, J. M. Carpenter, C. Beichman, et al. 2006. “The Two Micron All Sky Survey (2MASS)” 131 (February): 1163–83. [https://doi.org/10.1086/498708](https://doi.org/10.1086/498708).

Tachibana, Yutaro, and A. A. Miller. 2018. “A Morphological Classification Model to Identify Unresolved PanSTARRS1 Sources: Application in the ZTF Real-time Pipeline” 130 (994): 128001. [https://doi.org/10.1088/1538-3873/aae3d9](https://doi.org/10.1088/1538-3873/aae3d9).

Véron-Cetty, M P, and P Véron. 2010. “A catalogue of quasars and active nuclei: 13th edition.” _Astronomy and Astrophysics_ 518 (July). EDP Sciences: A10. [https://doi.org/10.1051/0004-6361/201014188](https://doi.org/10.1051/0004-6361/201014188).

* * *

1.  https://ned.ipac.caltech.edu/Library/Distances/[↩](https://lasair-ztf.lsst.ac.uk/sherlock#fnref1)


## Gravitational Wave Regions


## alerce_lc  

The [ALeRCE light curve classifier](https://arxiv.org/abs/2008.03311) uses variability features computed from the ZTF alert stream, and colors obtained from AllWISE and ZTF photometry. We apply a Balanced Random Forest algorithm with a two-level scheme, where the top level classifies each source as periodic, stochastic, or transient, and the bottom level further resolves each of these hierarchical classes, amongst 15 total classes. This classifier corresponds to the first attempt to classify multiple classes of stochastic variables (including core- and host-dominated active galactic nuclei, blazars, young stellar objects, and cataclysmic variables) in addition to different classes of periodic and transient sources, using real data.  
Reproduced with permission from the [Alerce Community Broker.](http://alerce.science/).  
_responsible user: Roy Williams_

The [Alerce Stamp Classifier](https://arxiv.org/abs/2008.03309) is based on a convolutional neural network, trained on alerts ingested from the Zwicky Transient Facility (ZTF). Using only the science, reference and difference images of the first detection as inputs, along with the metadata of the alert as features, the classifier is able to correctly classify alerts from active galactic nuclei, supernovae (SNe), variable stars, asteroids and bogus classes, with high accuracy (94 percent) in a balanced test set.  
Reproduced with permission from the [Alerce Community Broker.](http://alerce.science/)  
_responsible user: Roy Williams_

## fastfinder

Fastfinder is an early-time, fast transient alerting system in development at Queen's University Belfast. The purpose of Fastfinder is to identify any fast-evolving extragalactic transients, such as Kilonovae, from the LSST alert-stream using only the transient's early-time photometry. By comparing the transient's photometric characteristics to that of the parameter space of known fast-evolving transient classes, Fastfinder generates probabilistic scores on the likelihood of the transient's spectral type.  
_responsible user: Michael Fulton_

## fink_early_sn

[Fink](https://fink-broker.org/) is a LSST Community Alert Broker being developed by an international community of researchers with a large variety of scientific interests, including among others multi-messenger astronomy, supernovae, solar system, anomalies identification, microlensing and gamma-ray bursts optical counterparts. This sub-stream focuses on early supernova type Ia. In order to tag an alert as an early supernova Ia candidate, Fink mainly uses 2 criteria: (a) Ia probability larger than 50% from the [early supernova Ia module](https://arxiv.org/abs/2111.11438) , (b) Ia probability larger than 50% from either one of the deep learning classifier based on [SuperNNova](https://arxiv.org/abs/1901.06384). These candidates are also sent nightly to TNS for spectroscopic follow-up. Users should expect about 90% purity based on current performance. See also the [filter code](https://github.com/astrolabsoftware/fink-filters/blob/master/fink_filters/filter_early_sn_candidates/filter.py).  
Reproduced with permission from the [Fink Community Broker.](https://fink-broker.org/)  
_responsible user: Roy Williams_


