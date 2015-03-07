set +v
read -p "Username: " ttrUsername
read -p "Password: " ttrPassword
export TTR_PLAYCOOKIE=$ttrUsername:$ttrPassword
export TTR_GAMESERVER=52.0.191.143

echo ===============================
echo Starting Toontown  World Online...
echo Username: $ttrUsername
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart
sleep 1
