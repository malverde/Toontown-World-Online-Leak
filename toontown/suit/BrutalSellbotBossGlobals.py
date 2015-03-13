from toontown.toonbase import ToontownGlobals


PieCount = (
    70,
    60,
    55,
    50,
    45,
    40,
    35,
    30,
)


DamageLevels = {
    ToontownGlobals.BossCogElectricFence: 30,
    ToontownGlobals.BossCogRecoverDizzyAttack: 40,
    ToontownGlobals.BossCogAreaAttack: 50,
    ToontownGlobals.BossCogDirectedAttack: 40,
    ToontownGlobals.BossCogFrontAttack: 40
}


def getDamageFromAttackCode(attackCode):
    return DamageLevels.get(attackCode) or 40
