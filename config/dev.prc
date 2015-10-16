# This is the PRC configuration file for developer servers and clients.
# If making a change here, please remember to add it to public_client.prc
# as well as deployment/server.prc if necessary.

# Client settings
window-title Toontown World Online [Pre-Alpha]
server-version ttw-pre-alpha-2.5.2
audio-library-name p3fmod_audio
sync-video #f
want-dev #f
preload-avatars #t
want-keep-alive #f
texture-anisotropic-degree 16
cursor-filename resources/phase_3/etc/toonmono.cur
icon-filename resources/phase_3/etc/icon.ico

# Audio...
audio-library-name p3fmod_audio
#audio-library-name p3openal_audio

# Extra debug tools/variables
show-frame-rate-meter #f
cursor-hidden #f
undecorated #f

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

# Debug mode and sensitivity level
default-directnotify-level info

# Server settings
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/
# rpc-server-secret 0123456789abcdef
eventlog-host 127.0.0.1
want-cheesy-expirations #t
show-total-population #t

# DC Files
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toontown.dc

# Systems and Beta Modifications
# Temporary modifications for unimplemented features go here.
want-pets #t
want-news-tab #f
want-news-page #f
want-accessories #t
want-parties #t
want-gardening #f
want-gifting #t
want-picnic-games #f
want-chinese-table #f
want-fishing #t
want-checkers-table #f
want-findfour-table #f
want-keep-alive #f
want-speedhack-fix #t
want-cogdominiums #f
want-game-tables #f

# A few fun things.
estate-day-night #t
want-instant-parties #f
want-toontorial #f
want-doomsday #f

# Chat filter
want-whitelist #t
want-blacklist-sequence #f
force-avatar-understandable #t
force-player-understandable #t

# Holidays and Events
want-arg-manager #f
want-mega-invasions #t
mega-invasion-cog-type bw
want-hourly-fireworks #t
# want-flippy-pet-intro #f
want-hourly-fireworks-type summer

# Cog battling and multipliers
base-xp-multiplier 4
want-suit-planners #t
want-cogbuildings #t
want-speedhack-fix #f 

# group merges
boarding-group-merges #t

# Misc
# force-skip-tutorial #f