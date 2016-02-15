import hashlib
import json

def generateHash(filename):
	sha = hashlib.md5()
	try:
		file = open(filename, "rb")
	except IOError:
		return None
	try:
		sha.update(file.read())
	finally:
		file.close()
	return sha.hexdigest()
	
p3 = generateHash("build/resources/phase_3.mf")
p35 = generateHash("build/resources/phase_3.5.mf")
p4 = generateHash("build/resources/phase_4.mf")
p5 = generateHash("build/resources/phase_5.mf")
p55 = generateHash("build/resources/phase_5.5.mf")
p6 = generateHash("build/resources/phase_6.mf")
p7 = generateHash("build/resources/phase_7.mf")
p8 = generateHash("build/resources/phase_8.mf")
p9 = generateHash("build/resources/phase_9.mf")
p10 = generateHash("build/resources/phase_10.mf")
p11 = generateHash("build/resources/phase_11.mf")
p12 = generateHash("build/resources/phase_12.mf")
p13 = generateHash("build/resources/phase_13.mf")
gd = generateHash("build/GameData.pyd")

out = {}
out['phase_3.mf'] = {'hash':	str(p3)}
out['phase_3.5.mf'] = {'hash':	str(p35)}
out['phase_4.mf'] = {'hash':	str(p4)}
out['phase_5.mf'] = {'hash':	str(p5)}
out['phase_5.5.mf'] = {'hash':	str(p55)}
out['phase_6.mf'] = {'hash':	str(p6)}
out['phase_7.mf'] = {'hash':	str(p7)}
out['phase_8.mf'] = {'hash':	str(p8)}
out['phase_9.mf'] = {'hash':	str(p9)}
out['phase_10.mf'] = {'hash':	str(p10)}
out['phase_11.mf'] = {'hash':	str(p11)}
out['phase_12.mf'] = {'hash':	str(p12)}
out['phase_13.mf'] = {'hash':	str(p13)}
out['GameData.pyd'] = {'hash':	str(gd)}

with open('patcher.json', 'w') as patcher:
	patcher.write(json.dumps(out))
	print json.dumps(out)
