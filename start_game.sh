set +v
export ttrUsername=mgracer
echo "You wrote: $ttrUsername"
export ttrPassword=password
export TTR_PLAYCOOKIE=$ttrUsername$
export TTR_GAMESERVER=108.161.134.133

echo ===============================
echo Starting Toontown  World Online...
echo Username: $ttrUsername$
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart.py
sleep 1
