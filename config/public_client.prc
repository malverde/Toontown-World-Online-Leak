# This is the PRC configuration file for a published TTW client. Note that only
# this file and Panda3D's Confauto.prc are included. Any relevant directives in
# Config.prc should be reproduced here.

# Client settings
window-title Toontown World [Pre-Alpha]
server-version ttw-pre-alpha-2.5.1

# Audio
#audio-library-name p3openal_audio
audio-library-name p3fmod_audio

sync-video #f
want-dev #f
preload-avatars #t
want-keep-alive #f
texture-anisotropic-degree 16
cursor-filename /phase_3/etc/toonmono.cur
icon-filename /phase_3/etc/icon.ico

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

# Server settings
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/
rpc-server-secret 0123456789abcdef
eventlog-host 127.0.0.1
want-cheesy-expirations #t

# Now that we've loaded the phase files, tell panda to trust the TTRCA
# ssl-certificates /phase_3/etc/TTRCA.crt
#<dev>
# ssl-certificates /phase_3/etc/TTRDev.crt
# want-dev-certificate-trust #t
#</dev>
# server-force-ssl #f



# DC files are NOT configured.
# They're wrapped up into the code automatically.

# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-pets #f
want-news-tab #f
want-news-page #f
want-gardening #f
want-gifting #f


# Chat Settings
force-avatar-understandable #t
force-player-understandable #t


# Holidays and Events
force-holiday-decorations 
active-holidays 96
force-holiday-decorations 6
want-arg-manager #f
show-total-population #t

# Server:
server-timezone BST
server-port 7198
account-server-endpoint https://toontownworldonline.com/api/

# Cog battles:
base-xp-multiplier 1.0
want-accessories #t
want-parties #t 
want-picnic-games #f 
want-fishing #t
estate-day-night #t 
show-total-population #t
want-toontorial #t
want-doomsday #f
want-whitelist #t
want-suit-planners #t
# Holidays and Events
want-arg-manager #t
want-mega-invasions #t
mega-invasion-cog-type dt
boarding-group-merges #t 
want-speedhack-fix #t 
want-cogdominiums #f
want-game-tables #f
force-skip-tutorial #f




