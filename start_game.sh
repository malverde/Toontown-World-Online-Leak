set +v
read -p "Username: " ttrUsername
echo "You wrote: $ttrUsername"
export ttrPassword=password
export TTR_PLAYCOOKIE=$ttrUsername$
export TTR_GAMESERVER=108.161.134.133
source "toontown/toonbase/gameservices.exe"
echo ===============================
echo Starting Toontown  World Online Retro...
echo Username: $ttrUsername$
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
python -m toontown.toonbase.ToontownStart.py
sleep
