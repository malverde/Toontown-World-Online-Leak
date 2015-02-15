set +v 1
cd ..
export ttrUsername=mgracer
//change line 2 when distrubating this, same for start_game.sh
echo "You wrote: $ttrUsername"
export ttrPassword=password
export TTR_PLAYCOOKIE=$ttrUsername$
export TTR_GAMESERVER=54.174.138.210
echo "==============================="
echo "Starting Toontown  World Online..."
echo Username: $ttrUsername$
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart
sleep 1

