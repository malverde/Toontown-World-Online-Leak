set +v
export ttrUsername=mgracer
//change line 2 when distrubating this, same for start_game.sh
echo "You wrote: $ttrUsername"
export ttrPassword=password
export TTR_PLAYCOOKIE=$ttrUsername$
export TTR_GAMESERVER=54.84.246.211

echo ===============================
echo Starting Toontown  World Online...
echo Username: $ttrUsername$
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart.py
sleep 1
