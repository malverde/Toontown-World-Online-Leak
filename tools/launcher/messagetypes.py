# Defines types of 'messages' that might get sent to the GUI
# Each object sent to the GUI via queue should be a tuple of at least 1 object, the first object being a message type

# Ex: output.put((LAUNCHER_ERROR, "Things broke"), block=False)
# Ex: output.put((LAUNCHER_VERSION_UPDATE, "1.2.3", "Fixed nothing", "google.com"), block=False)

# LAUNCHER_ERROR(message)
# Implies that the GUI should display the error and then reset the state of the GUI
LAUNCHER_ERROR = 0

# LAUNCHER_VERSION_UPDATE(version, changelog, url)
# The user should be given a modal saying there's a new version of the launcher.
# After the user acks the modal, the URL should be opened.
LAUNCHER_VERSION_UPDATE = 1

# LAUNCHER_REQUEST_TFA(message)
# Request a two-factor token from the user
LAUNCHER_REQUEST_TFA = 2

# LAUNCHER_STATUS(message)
# Update the status text that informs the user what's being worked on right now
LAUNCHER_STATUS = 3

# LAUNCHER_PROGRESS(percent)
# Set the progress bar percentage, an int out of 100
LAUNCHER_PROGRESS = 4

# LAUNCHER_PLAY_RETRY()
# Ask the user if they want to retry launching/playing the game
# If we do want to retry, send a True down the pipe
LAUNCHER_PLAY_RETRY = 5

# LAUNCHER_ENABLE_CONTROLS()
# Reenable the login controls
LAUNCHER_ENABLE_CONTROLS = 6

# LAUNCHER_CLEAR_PASSWORD
# Clear out the password field
LAUNCHER_CLEAR_PASSWORD = 7

# LAUNCHER_HIDE()
# Hide the launcher window in the task bar
LAUNCHER_HIDE = 997

# LAUNCHER_SHOW()
# Show the launcher window from the task bar
LAUNCHER_SHOW = 998

# LAUNCHER_EXIT()
# The launcher should immediately close
LAUNCHER_EXIT = 999