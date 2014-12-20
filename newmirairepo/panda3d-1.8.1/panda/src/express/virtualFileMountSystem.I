// Filename: virtualFileMountSystem.I
// Created by:  drose (03Aug02)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: VirtualFileMountSystem::Constructor
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
INLINE VirtualFileMountSystem::
VirtualFileMountSystem(const Filename &physical_filename) :
  _physical_filename(physical_filename)
{
}

////////////////////////////////////////////////////////////////////
//     Function: VirtualFileMountSystem::get_physical_filename
//       Access: Public
//  Description: Returns the name of the source file on the OS
//               filesystem of the directory or file that is mounted.
////////////////////////////////////////////////////////////////////
INLINE const Filename &VirtualFileMountSystem::
get_physical_filename() const {
  return _physical_filename;
}
