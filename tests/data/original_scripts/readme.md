Source Scripts
--------------

This folder contains the original Matlab scripts that were included in the supporting 
information of Paul H. C. Eilers' paper: [A Perfect Smoother](https://pubs.acs.org/doi/10.1021/ac034173t). 

A Perfect Smoother
Paul H. C. Eilers
Analytical Chemistry 2003 75 (14), 3631-3636
DOI: 10.1021/ac034173t


I've modified some of the scripts which begin with "demo", to output a csv which can be
used to test and validate the rust version of the Whittaker smoother. I've included the original ReadMe below.


---

Whittaker Smoother Toolbox
--------------------------

This archive contains a small toolbox of Matlab functions and
scripts to show the versatility of the Whittaker Smoother (WS).
Theory and implementation are described in my paper in Analytical
Chemistry, 2003 (Vol 75, pp 3631–3636).

The functions are:
 - whitsm: for smoothing of a complete data series, sampled at
   equal intervals;
 - whitsmw: for smoothing of a data series, sampled at equal
   intervals; some data may be missing, as indicated by a
   vector of 0/1 weights;
 - whitsmdd: for smoothing of a complete data series, sampled at
   unequal intervals; the sampling positions are given by a
   (monotone) series x;
 - whitsmddw: for smoothing of an incomplete data series, sampled
   at unequal intervals; the sampling positions are given by a
   (monotone) series x;
 - whitscat:  for smoothing of a scatterplot with arbitrary x and
   y data.
All functions return fitted values and, optionally, the RMS
(leave-one-out) cross-validation error. All functions contain
documentation headers to describe input and output.

There are demonstration scripts to illustrate the use of the
functions.

You are free to use and modify these functions in any way you
like, as long as you give proper reference to the original source
and cite the paper.

Paul Eilers


Department of Medical Statistics
Leiden University Medical Centre
P.O. Box 9604
2300 RC Leiden
The Netherlands
e-mail: p.eilers@lumc.nl
