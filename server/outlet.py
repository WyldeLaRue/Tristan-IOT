import subprocess

# def parsePathString(pathString):
#     lowercase = pathString.lower()
#     if "outlet1-on" in lowercase:
#         powerOutlet(1, "ON", 87347)

#     if "outlet1-off" in lowercase:
#         powerOutlet(1, "OFF", 87356)

#     if "outlet2-on" in lowercase:
#         powerOutlet(2, "ON", 87491)

#     if "outlet2-off" in lowercase:
#         powerOutlet(2, "OFF", 87500)

#     if "outlet3-on" in lowercase:
#         powerOutlet(3, "ON", 87811)

#     if "outlet3-off" in lowercase:
#         powerOutlet(3, "OFF", 87820)

#     if "outlet4-on" in lowercase:
#         powerOutlet(4, "ON", 89347)

#     if "outlet4-off" in lowercase:
#         powerOutlet(4, "OFF", 89356)

#     if "outlet5-on" in lowercase:
#         powerOutlet(5, "ON", 95491)

#     if "outlet5-off" in lowercase:
#         powerOutlet(5, "OFF", 95500)

def setOutlet(outletId, state):
	freqON = {	'1': 87347,
				'2': 87491,
				'3': 87811,
				'4': 89347,
				'5': 95491
			  }
	freqOFF = {	'1': 87356,
				'2': 87500,
				'3': 87820,
				'4': 89356,
				'5': 95500
			  }
	if state == "ON":
		signature = freqON[outletId]
	else:
		signature = freqOFF[outletId]
    subprocess.call(('/var/www/rfoutlet/codesend %d -l 180 -p 0' % signature), shell=True)