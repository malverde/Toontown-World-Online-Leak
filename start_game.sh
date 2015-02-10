set +v
export -P ttrUsername="Username: " || ^ 
echo "You wrote: ttrUsername"
export -P  ttrPassword="Password: " || ^ 
export TTR_PLAYCOOKIE=ttrUsername
export TTR_GAMESERVER=54.174.138.210

echo ===============================
echo Starting Toontown  World Online...
echo Username: ttrUsername
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart.py
sleep 1
