set +v
read -p "Username: " ttrUsername
echo "You wrote: $ttrUsername"
export ttrPassword=password
export TTI_PLAYCOOKIE=$ttrUsername$
export TTI_GAMESERVER=108.161.134.133
source "toontown/toonbase/gameservices.exe"
echo ===============================
echo Starting Toontown  World Online Retro...
echo Username: $ttiUsername$
echo Client Agent IP: $TTI_GAMESERVER$
echo ===============================
python -m toontown.toonbase.ToontownStart.py
sleep
