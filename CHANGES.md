# Release Notes

### Version 0.1.1 (2025-01-24)
- The object and the 2 sherlock mothods are all singular now
- The object method has two new arguments
    - `lite=True` means only some of the attributes from LSST are returned
    - `lasair_added=False` means just the LSST atrtributes
    - `lasair_added=True` includes the sherlock, cutouts, etc as well
- The `lightcurves` method is deprecated, it is replaced with `object(lasair_added=False)`
