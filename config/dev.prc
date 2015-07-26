# This is the PRC configuration file for developer servers and clients.
# If making a change here, please remember to add it to public_client.prc
# as well as deployment/server.prc if necessary.

# Client settings
window-title Toontown World [Pre-Alpha]
server-version ttw-pre-alpha-2.5.2
audio-library-name p3openal_audio
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

# Useless Variables
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


# Server settings
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/
rpc-server-secret 0123456789abcdef
eventlog-host 127.0.0.1
want-cheesy-expirations #t


# DC Files
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toontown.dc


# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-pets #f
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


# Developer Modifications
# A few fun things for our developer build. These shouldn't go in public_client.
estate-day-night #t
want-instant-parties #f
show-total-population #t
want-toontorial #t
want-doomsday #f

# Chat stuff
want-whitelist #t
want-blacklist-sequence #f
force-avatar-understandable #t
force-player-understandable #t

want-suit-planners #t
want-cogbuildings #t
# Holidays and Events
want-arg-manager #f
want-mega-invasions #f
mega-invasion-cog-type dt
want-speedhack-fix #f 


# Cog battles :
#gag-bonus 2
base-xp-multiplier 1
#group merges
boarding-group-merges #t
#other

want-speedhack-fix #t
want-cogdominiums #f
want-game-tables #f
force-skip-tutorial #t
