set +v 1
read -p "Username: " ttrUsername
read -p "Password: " ttrPassword
//change line 2 when distrubating this, same for start_game.sh


export TTR_PLAYCOOKIE=$ttrUsername:$ttrPassword
export TTR_GAMESERVER=54.174.138.210

echo "==============================="
echo "Starting Toontown  World Online..."
echo Username: $ttrUsername$
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart.py
sleep 1
