set +v
export TTWUsername=
echo "You wrote: $TTWUsername"
export TTWPassword=password
export TTW_PLAYCOOKIE=$TTWUsername$
export TTW_GAMESERVER=108.161.134.133

echo ===============================
echo Starting Toontown  World Online...
echo Username: $TTWUsername$
echo Client Agent IP: $TTW_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart.py
sleep 1
