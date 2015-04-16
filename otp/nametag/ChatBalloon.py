# Embedded file name: otp\nametag\ChatBalloon.py
from pandac.PandaModules import *

class ChatBalloon:
    TEXT_SHIFT = (0.1, -0.05, 1.1)
    TEXT_SHIFT_REVERSED = -0.05
    TEXT_SHIFT_PROP = 0.08
    NATIVE_WIDTH = 10.0
    MIN_WIDTH = 2.5
    MIN_HEIGHT = 1
    BUBBLE_PADDING = 0.3
    BUBBLE_PADDING_PROP = 0.05
    BUTTON_SCALE = 6
    BUTTON_SHIFT = (-0.2, 0, 0.6)
    FRAME_SHIFT = (0.2, 1.4)

    def __init__(self, model):
        self.model = model

    def generate(self, text, font, textColor = (0, 0, 0, 1), balloonColor = (1, 1, 1, 1), wordWrap = 10.0, button = None, reversed = False):
        root = NodePath('balloon')
        balloon = self.model.copyTo(root)
        top = balloon.find('**/top')
        middle = balloon.find('**/middle')
        bottom = balloon.find('**/bottom')
        balloon.setColor(balloonColor)
        if balloonColor[3] < 1.0:
            balloon.setTransparency(1)
        t = root.attachNewNode(TextNode('text'))
        t.node().setFont(font)
        t.node().setWordwrap(wordWrap)
        t.node().setText(text)
        t.node().setTextColor(textColor)
        width, height = t.node().getWidth(), t.node().getHeight()
        t.setAttrib(DepthWriteAttrib.make(0))
        t.setPos(self.TEXT_SHIFT)
        t.setX(t, self.TEXT_SHIFT_PROP * width)
        t.setZ(t, height)
        if reversed:
            t.setX(self.TEXT_SHIFT_REVERSED - self.TEXT_SHIFT_PROP * width - width)
        if button:
            np = button.copyTo(root)
            np.setPos(t, width, 0, -height)
            np.setPos(np, self.BUTTON_SHIFT)
            np.setScale(self.BUTTON_SCALE)
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
            if reversed:
                t.setX(t, -width / 2.0)
            else:
                t.setX(t, width / 2.0)
            t.node().setAlign(TextNode.ACenter)
        if height < self.MIN_HEIGHT:
            height = self.MIN_HEIGHT
            t.setX(t, height / 2.0)
            t.node().setAlign(TextNode.ACenter)
        width *= 1 + self.BUBBLE_PADDING_PROP
        width += self.BUBBLE_PADDING
        balloon.setSx(width / self.NATIVE_WIDTH)
        if reversed:
            balloon.setSx(-balloon.getSx())
            balloon.setTwoSided(True)
        middle.setSz(height)
        top.setZ(top, height - 1)
        left, bottom = self.FRAME_SHIFT
        if reversed:
            left = -left - width
        frame = (left,
         left + width,
         bottom,
         bottom + height + 1)
        return (root, frame)