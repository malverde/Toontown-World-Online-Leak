# This is the PRC configuration file for a published TTW client. Note that only
# this file and Panda3D's Confauto.prc are included. Any relevant directives in
# Config.prc should be reproduced here.

# Client settings
window-title Toontown World Online [Pre-Alpha]
server-version ttw-pre-alpha-2.5.2
texture-anisotropic-degree 16
preload-avatars #f


# Graphics:
aux-display pandagl
aux-display pandadx9
aux-display p3tinydisplay


# Performance
sync-video #f
smooth-lag 0.4
texture-power-2 none
gl-check-errors #f
garbage-collect-states #f


# Debug settings
# Codebase
default-directnotify-level info
default-directnotify-level warning
# Panda
notify-level warning
want-dev #f
want-keep-alive #f


# Game server address and authentication address
game-server 158.69.210.54
server-port 7198
# account-server localhost


# Audio
audio-library-name p3fmod_audio
# audio-library-name p3openal_audio


# Cursor and Icon
# cursor-filename resources/phase_3/etc/toonmono.cur
# icon-filename resources/phase_3/etc/icon.ico


# Useless Variables
show-frame-rate-meter #f
cursor-hidden #f
undecorated #f


# Resources settings
model-path /
model-cache-models #f
model-cache-textures #f
vfs-mount phase_3.mf /
vfs-mount phase_3.5.mf /
vfs-mount phase_4.mf /
vfs-mount phase_5.mf /
vfs-mount phase_5.5.mf /
vfs-mount phase_6.mf /
vfs-mount phase_7.mf /
vfs-mount phase_8.mf /
vfs-mount phase_9.mf /
vfs-mount phase_10.mf /
vfs-mount phase_11.mf /
vfs-mount phase_12.mf /
vfs-mount phase_13.mf /
default-model-extension .bam


# Now that we've loaded the phase files, tell panda to trust the TTRCA
# ssl-certificates /phase_3/etc/TTRCA.crt
#<dev>
# ssl-certificates /phase_3/etc/TTRDev.crt
# want-dev-certificate-trust #t
#</dev>
# server-force-ssl #f


# DC files are NOT configured.
# They're wrapped up into the code automatically.


# Systems and Beta Modifications
# Modifications/temporary for unimplemented features go here.
want-accessories #f
# Newsmanager
want-news-tab #f
want-news-page #f
want-fishing #t
want-parties #f
# Estates
want-pets #f
want-gardening #f
want-gifting #f
# Table games
want-game-tables #f
want-checkers-table #f
want-findfour-table #f
want-keep-alive #f
want-picnic-games #f
want-chinese-table #f
# Security
want-speedhack-fix #t
# A few fun things for unfinished events and settings
estate-day-night #t
want-instant-parties #f
want-toontorial #f
want-doomsday #f
want-cogdominiums #t


# Chat system (server-sided/client-sided)
want-whitelist #t
want-blacklist-sequence #f
force-avatar-understandable #t
force-player-understandable #t


# Holidays and Events (server-sided/client-sided)
want-arg-manager #f
want-mega-invasions #f
mega-invasion-cog-type bw
want-hourly-fireworks #t
# want-flippy-pet-intro #f
want-hourly-fireworks-type victoryreleasefireworks
# Alternative than nerfing VP?
easy-vp #f
# force-holiday-decorations 0
want-blueprint4-ARG #f
want-april-toons #f


# Cog battling and multipliers
base-xp-multiplier 4
want-suit-planners #t
want-cogbuildings #t


# Group merges
boarding-group-merges #t


# Misc
# force-skip-tutorial #f


# Server:
server-timezone BST/EDT/-5
server-port 7198
account-server-endpoint https://toontownworldonline.com/api/
csmud-secret Yvv4Jr5TUDkX5M8gh64Z9Q4AUAQYdFNecyGgl2I5GOQf8CBh7LUZWpzKB9FBF