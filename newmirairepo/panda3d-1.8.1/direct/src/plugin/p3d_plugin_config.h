/* p3d_plugin_config.h.  Generated automatically by ppremake 1.22 from p3d_plugin_config.h.pp. */
/********************************** DO NOT EDIT ****************************/
/* The URL that is the root of the download server that this plugin
   should contact.  The contents.xml file that defines this particular
   "coreapi" package should be found at this location. */
#define PANDA_PACKAGE_HOST_URL ""
/* The Core API version number.  This one also appears in
   pandaVersion.h. */
#define P3D_COREAPI_VERSION_STR "1.0.4.1"
/* As does the plugin version number. */
#define P3D_PLUGIN_VERSION_STR "1.0.4"
/* The filename(s) to generate output to when the plugin is running.
   For debugging purposes only. */
#define P3D_PLUGIN_LOG_DIRECTORY ""
#define P3D_PLUGIN_LOG_BASENAME1 ""
#define P3D_PLUGIN_LOG_BASENAME2 ""
#define P3D_PLUGIN_LOG_BASENAME3 ""
/* For development only: the location at which p3dpython.exe can be
   found.  Empty string for the default. */
#define P3D_PLUGIN_P3DPYTHON ""
/* For development only: the location at which p3d_plugin.dll/.so can
   be found.  Empty string for the default. */
#define P3D_PLUGIN_P3D_PLUGIN ""
/* We need to know whether GTK is enabled for XEmbed. */
#undef HAVE_GTK
