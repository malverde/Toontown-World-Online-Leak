/* Filename: pandaVersion.h
 * Created by:  drose (26Jan05)
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*******************************************************************
 *  Generated automatically by ppremake 1.22 from pandaVersion.h.pp.
 ***************************** DO NOT EDIT *************************
   Do NOT attempt to edit the version number in this file.  This is a
   generated file, and your changes to this file will not persist.  To
   increment the version number, modify dtool/PandaVersion.pp and
   re-run ppremake.
 ***************************** DO NOT EDIT *************************/
/* Include this file anywhere you need to determine the Panda version
   number at compile time.  If you need the runtime Panda version, use
   pandaSystem.h instead. */
/* Try to avoid including this file from another .h file; include it
   only from .cxx instead.  This helps prevent unnecessarily long
   rebuilds just because the version number changes; if this file is
   included in a .h file, then any other files which also include that
   .h file will need to be rebuilt when the version number changes. */
#define PANDA_MAJOR_VERSION 1
#define PANDA_MINOR_VERSION 8
#define PANDA_SEQUENCE_VERSION 1
/* Define if this is an "official" version, undefine otherwise. */
#define PANDA_OFFICIAL_VERSION 1
/* This is the panda numeric version as a single number, with three
   digits reserved for each component. */
#define PANDA_NUMERIC_VERSION 1008001
/* This is the panda version expressed as a string.  It ends in the
   letter "c" if this is not an "official" version (e.g. it was checked
   out from CVS by the builder). */
# define PANDA_VERSION_STR "1.8.1"
/* This is the version of the Panda3D ABI expressed as a string.
   This usually means the major and minor version. It should be the
   same for Panda3D versions that are supposed to be backward
   ABI compatible with each other. */
# define PANDA_ABI_VERSION_STR "1.8"
/* This is a string indicating who has provided this distribution. */
# define PANDA_DISTRIBUTOR "homebuilt"
/* The string indicating the version number of the associated Panda3D
   distributable package, or empty string if there is no associated
   package. */
# define PANDA_PACKAGE_VERSION_STR ""
/* The string indicating the URL from which the associated Panda3D
   distributable package may be downloaded, or empty string if there
   is no associated package. */
# define PANDA_PACKAGE_HOST_URL ""
/* Similar definitions for the plugin versioning, if in use. */
#define P3D_PLUGIN_MAJOR_VERSION 1
#define P3D_PLUGIN_MINOR_VERSION 0
#define P3D_PLUGIN_SEQUENCE_VERSION 4
# define P3D_COREAPI_VERSION_STR "1.0.4.1"
