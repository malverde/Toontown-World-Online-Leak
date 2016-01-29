# Basic FSM module, based on Panda3D's direct.fsm.FSM module.
# This was intented for use by toontown world's launcher.
# Created by Harv on 6/6/2014 @ 4:12am UTC

import string
import sys

class FSM:
    """
    A very basic FSM module that gets the job done. This module does NOT enforce
    FSM locking, and should not be used to do so. It is simply a class that keeps
    track of the current state and allows switching of states.

    To create a new State, you define it as a method:
        def enterState(self, ...):
            foo.bar()

    You can also define the method to be called when the FSM exits this state:
        def exitState(self):
            foo.bar()
    However, you cannot pass any parameters in the exit method. Alternatively, you
    can store attributes you want to pass in to the FSM class itself, and exit can
    use them when executed.

    To switch to a new state, call the following method:
        self.request('State', ...)
    If you call the method directly, the FSM will likely break, so I recommend that
    you don't do so.

    To create an FSM, you simply create a new class and inherit from FSM.
    Note that you also have to call FSM.__init__(self) in order for the FSM class
    to properly work.
    """

    def __init__(self):
        self.state = "Off"
        self.valid_state_characters = string.ascii_letters + '_'
        self.transitions = None

    def request(self, state, *args, **kwargs):
        if not state == 'Off' and self.transitions is None:
            print "Error: No transitions defined!"
            self.request('Off')
        if not isinstance(state, basestring):
            print "Error: State %s is not a string!" % str(state)
            self.request('Off')
        for character in state:
            if character not in self.valid_state_characters:
                print "Error: State %s has invalid characters." % state
                self.request('Off')
        if not hasattr(self, 'enter'+state):
            print "Error: State %s does not exist." % state
            self.request('Off')
        if self.state == state:
            print "Error: Already in State %s." % state
            return
        possible_transitions = self.transitions.get(self.state, [])
        if not state == 'Off' and state not in possible_transitions:
            print "Error: Cannot transition from %s to %s." % (self.state, state)
            self.request('Off')
        if hasattr(self, 'exit'+self.state):
            getattr(self, 'exit'+self.state)()
        self.state = state
        getattr(self, 'enter'+state)(*args, **kwargs)

    def enterOff(self):
        # Over-ridable by child class.
        sys.exit(1)
