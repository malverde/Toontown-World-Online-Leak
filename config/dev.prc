# This is the PRC configuration file for developer servers and clients.
# Please remember to update public_client.prc if necessary.

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
default-directnotify-level spam
# Panda
notify-level warning
want-dev #f
want-keep-alive #f


# Extra debug tools/variables
show-frame-rate-meter #f
cursor-hidden #f
undecorated #f


# Game server address and authentication address
game-server 158.69.210.54
server-port 7198
# account-server localhost


# Cursor and Icon

# cursor-filename resources/phase_3/etc/toonmono.cur
# icon-filename resources/phase_3/etc/icon.ico


# Audio
audio-library-name p3fmod_audio
# audio-library-name p3openal_audio


# Resource settings
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
vfs-mount resources/server /server

model-path /
default-model-extension .bam


# Main Server Settings

# RPC settings - never used
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/
# rpc-server-secret 0123456789abcdef
eventlog-host 127.0.0.1
# Cheesy Effects and POP
want-cheesy-expirations #t
show-total-population #t
shard-low-pop 1
shard-mid-pop 3
csmud-secret Yvv4Jr5TUDkX5M8gh64Z9Q4AUAQYdFNecyGgl2I5GOQf8CBh7LUZWpzKB9FBF

# DC Files (server and client-sided)
dc-file config/toontown.dc


# Systems and Beta Modifications
# Modifications/temporary for unimplemented features go here.
want-accessories #t
# Newsmanager
want-news-tab #f
want-news-page #f
want-fishing #t
want-parties #t
# Estates
want-pets #t
want-gardening #f
want-gifting #t
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
want-cogdominiums #f


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
easy-vp #t
force-holiday-decorations 1, 6
want-blueprint4-ARG #f
want-april-toons #f

# Cog battling and multipliers
base-xp-multiplier 4
want-suit-planners #t
want-cogbuildings #t

# Group merges
boarding-group-merges #t

# Misc
# force-skip-tutorial #t