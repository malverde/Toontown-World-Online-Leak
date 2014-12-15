set +v
read -p "Username: " ttiUsername
echo "You wrote: $ttiUsername"
export TTI_PLAYCOOKIE=$ttiUsername$
export TTI_GAMESERVER=108.161.134.133
echo ===============================
echo Starting Toontown Online Retro...
echo Username: $ttiUsername$
echo Client Agent IP: $TTI_GAMESERVER$
echo ===============================
python -m toontown.toonbase.ToontownStart.py
sleep
