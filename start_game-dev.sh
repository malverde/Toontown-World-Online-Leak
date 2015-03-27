set +v
read -p "Username: " ttrUsername
read -p "Password: " ttrPassword
export TTR_PLAYCOOKIE=$ttrUsername:$ttrPassword
export TTR_GAMESERVER=54.172.56.119

echo ===============================
echo Starting Toontown  World Online...
echo Username: $ttrUsername
echo Client Agent IP: $TTR_GAMESERVER$
echo ===============================
ppython -m toontown.toonbase.ToontownStart
sleep 1
