// Filename: vorbisAudioCursor.cxx
// Created by: rdb (23Aug13)
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

#include "vorbisAudioCursor.h"
#include "virtualFileSystem.h"

#ifdef HAVE_VORBIS

TypeHandle VorbisAudioCursor::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::Constructor
//       Access: Protected
//  Description: Reads the .wav header from the indicated stream.
//               This leaves the read pointer positioned at the
//               start of the data.
////////////////////////////////////////////////////////////////////
VorbisAudioCursor::
VorbisAudioCursor(VorbisAudio *src, Filename filename) :
  MovieAudioCursor(src),
  _is_valid(false),
  _bitstream(0)
{
  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  _vfile = vfs->get_file(filename);
  if(!_vfile)
  {
	return;
  }
  _stream = _vfile->open_read_file(true);

  if (_stream == NULL) {
    return;
  }

  _stream->seekg(0, ios::end);
  vorbis_cat.debug() << "StreamSize: " << _stream->tellg() << "\n";
  vorbis_cat.debug() << "fail(): " << _stream->fail() << "\n";
  _stream->seekg(0, ios::beg);
  // Set up the callbacks to read via the VFS.
  ov_callbacks callbacks;
  callbacks.read_func = &cb_read_func;
  callbacks.seek_func = &cb_seek_func;
  callbacks.close_func = &cb_close_func;
  callbacks.tell_func = &cb_tell_func;

  if (ov_open_callbacks((void*)this, &_ov, NULL, 0, callbacks) != 0) {
    vorbis_cat.error()
      << "Failed to read Ogg Vorbis file.\n";
    return;
  }

  _length = ov_time_total(&_ov, -1);

  vorbis_info *vi = ov_info(&_ov, -1);
  _audio_channels = vi->channels;
  _audio_rate = vi->rate;

  _can_seek = (ov_seekable(&_ov) != 0);
  _can_seek_fast = _can_seek;

  _is_valid = true;
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::Destructor
//       Access: Protected, Virtual
//  Description: xxx
////////////////////////////////////////////////////////////////////
VorbisAudioCursor::
~VorbisAudioCursor() {
  if(_is_valid)
	ov_clear(&_ov);
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::seek
//       Access: Protected
//  Description: Seeks to a target location.  Afterward, the
//               packet_time is guaranteed to be less than or
//               equal to the specified time.
////////////////////////////////////////////////////////////////////
void VorbisAudioCursor::
seek(double t) {
  if(t > ov_time_total(&_ov, -1))
  {
    t = ov_time_total(&_ov, -1);
  }

  // Use ov_time_seek_lap if cross-lapping is enabled.
  if (vorbis_seek_lap) {
    int code = ov_time_seek_lap(&_ov, t);
    if(code == OV_EOF) //Can't crosslap on EOF
    {
        code = ov_time_seek(&_ov, t);
    }
    if (code != 0) {
      vorbis_cat.error()
        << "Seek failed.  Ogg Vorbis stream may not be lap-seekable. t = " << t
		<< " code = " << code << "\n";
      return;
    }
  } else {
    int code = ov_time_seek(&_ov, t);
    if (code != 0) {
      vorbis_cat.error()
        << "Seek failed.  Ogg Vorbis stream may not be seekable. t = " << t
		<< " code = " << code << "\n";
      return;
    }
  }

  _last_seek = ov_time_tell(&_ov);
  _samples_read = 0;
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::read_samples
//       Access: Public, Virtual
//  Description: Read audio samples from the stream.  N is the
//               number of samples you wish to read.  Your buffer
//               must be equal in size to N * channels.
//               Multiple-channel audio will be interleaved.
////////////////////////////////////////////////////////////////////
void VorbisAudioCursor::
read_samples(int n, PN_int16 *data) {
  int desired = n * _audio_channels;

  char *buffer = (char*) data;
  int length = desired * 2;

  // Call ov_read repeatedly until the buffer is full.
  while (length > 0) {
    int bitstream;

    // ov_read can give it to us in the exact format we need.  Nifty!
    long read_bytes = ov_read(&_ov, buffer, length, 0, 2, 1, &bitstream);
    if (read_bytes > 0) {
      buffer += read_bytes;
      length -= read_bytes;
    } else {
      break;
    }

    if (_bitstream != bitstream) {
      // It is technically possible for it to change parameters from one
      // bitstream to the next.  However, we don't offer this flexibility.
      vorbis_info *vi = ov_info(&_ov, -1);
      if (vi->channels != _audio_channels || vi->rate != _audio_rate) {
        vorbis_cat.error()
          << "Ogg Vorbis file has non-matching bitstreams!\n";

        // We'll change it anyway.  Not sure what happens next.
        _audio_channels = vi->channels;
        _audio_rate = vi->rate;
        break;
      }

      _bitstream = bitstream;
    }
  }

  // Fill the rest of the buffer with silence.
  if (length > 0) {
    memset(buffer, 0, length);
    n -= length / 2 / _audio_channels;
  }

  _samples_read += n;
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::cb_read_func
//       Access: Private, Static
//  Description: Callback passed to libvorbisfile to implement
//               file I/O via the VirtualFileSystem.
////////////////////////////////////////////////////////////////////
size_t VorbisAudioCursor::
cb_read_func(void *ptr, size_t size, size_t nmemb, void *datasource) {
  VorbisAudioCursor *me = (VorbisAudioCursor*) datasource;

  me->_stream->read((char *)ptr, size * nmemb);
  vorbis_cat.debug() << "cb_read_func size: " << size << " nmemb: " << nmemb << "\n";
  vorbis_cat.debug() << "cb_read_func: " << me->_stream->gcount() << "\n";
  return me->_stream->gcount();
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::cb_seek_func
//       Access: Private, Static
//  Description: Callback passed to libvorbisfile to implement
//               file I/O via the VirtualFileSystem.
////////////////////////////////////////////////////////////////////
int VorbisAudioCursor::
cb_seek_func(void *datasource, ogg_int64_t offset, int whence) {
  VorbisAudioCursor *me = (VorbisAudioCursor*) datasource;
  vorbis_cat.debug() << "cb_seek_func offset: " << offset << " whence: " << whence << "\n";
  switch (whence) {
  case SEEK_SET:
    me->_stream->seekg(offset, ios::beg);
    break;

  case SEEK_CUR:
    me->_stream->seekg(offset, ios::cur);
    break;

  case SEEK_END:
    me->_stream->seekg(offset, ios::end);
    break;

  default:
    vorbis_cat.error()
      << "Illegal parameter to seek in VorbisAudioCursor::cb_seek_func\n";
    return -1;
  }
  static bool fail_recurse = false;
  if(me->_stream->fail() && !fail_recurse)
  {
    if(me->_stream->bad())
	{
	  vorbis_cat.debug() << "cb_seek_func badbit\n";
	}
	else
	{
	  vorbis_cat.debug() << "cb_seek_func failbit\n";
	}
	me->_vfile->close_read_file(me->_stream);
	me->_stream = me->_vfile->open_read_file(true);
	fail_recurse = true;
	cb_seek_func((void*)me, offset, whence);
	fail_recurse = false;
  }
  me->_stream->clear();
  return 0;
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::cb_close_func
//       Access: Private, Static
//  Description: Callback passed to libvorbisfile to implement
//               file I/O via the VirtualFileSystem.
////////////////////////////////////////////////////////////////////
int VorbisAudioCursor::
cb_close_func(void *datasource) {
  VorbisAudioCursor *me = (VorbisAudioCursor*) datasource;
  vorbis_cat.debug() << "cb_close_func\n";
  me->_vfile->close_read_file(me->_stream);

  // Return value isn't checked, but let's be predictable
  return 0;
}

////////////////////////////////////////////////////////////////////
//     Function: VorbisAudioCursor::cb_tell_func
//       Access: Private, Static
//  Description: Callback passed to libvorbisfile to implement
//               file I/O via the VirtualFileSystem.
////////////////////////////////////////////////////////////////////
long VorbisAudioCursor::
cb_tell_func(void *datasource) {
  VorbisAudioCursor *me = (VorbisAudioCursor*) datasource;
  vorbis_cat.debug() << "cb_tell_func: " << me->_stream->tellg() << "\n";
  return me->_stream->tellg();
}

#endif // HAVE_VORBIS
