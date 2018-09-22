import sys
from datetime import datetime
import random
import bisect
import time
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS

argv = sys.argv
if len(argv) < 0:
	print("Usage: python exif.py [filename]")
path = argv[1]

programs = {}
with zipfile.ZipFile(path) as zipObj:
	zipObj.extractall("./")
	for filename in zipObj.namelist():
		if filename[-1] == "/":
			continue
		img = Image.open(filename)
		exif = img._getexif()
		DateTimeOriginal = ""
		DateTime = ""
		MeteringMode = 0
		command = ""
		lat = 0.0
		lng = 0.0
		height = 0
		width = 0
		for key, val in exif.items():
			if TAGS.get(key, key) == "DateTimeOriginal":
				DateTimeOriginal = datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
			elif TAGS.get(key, key) == "DateTime":
				DateTime = datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
			elif TAGS.get(key, key) == "MeteringMode":
				MeteringMode = val
			elif TAGS.get(key, key) == "ISOSpeedRatings":
				if val < 100:
					command = "substitution"
				elif val < 200:
					command = "input"
				elif val < 300:
					command = "output"
				elif val < 400:
					command = "addition"
				elif val < 500:
					command = "substraction"
				elif val < 600:
					command = "multiplication"
				elif val < 700:
					command = "division"
				elif val < 800:
					command = "remainder"
			elif TAGS.get(key, key) == "ExifImageHeight":
				height = val
			elif TAGS.get(key, key) == "ExifImageWidth":
				width = val
			elif TAGS.get(key, key) == "GPSInfo":
				lat = (1 if val[1] == "N" else - 1) * (1.0 * val[2][0][0] /
														val[2][0][1] + 1.0 / 60 * val[2][1][0] / val[2][1][1])
				lng = (1 if val[3] == "E" else - 1) * (1.0 * val[4][0][0] /
														val[4][0][1] + 1.0 / 60 * val[4][1][0] / val[4][1][1])
		if DateTimeOriginal in programs:
			programs[DateTimeOriginal].append({"DateTimeOriginal": DateTimeOriginal,
												"DateTime": DateTime,
												"MeteringMode": MeteringMode,
												"command": command,
												"height": height,
												"width": width,
												"latitude": lat,
												"longitude": lng
												})
		else:
			programs[DateTimeOriginal] = [{"DateTimeOriginal": DateTimeOriginal,
											"DateTime": DateTime,
											"MeteringMode": MeteringMode,
											"command": command,
											"height": height,
											"width": width,
											"latitude": lat,
											"longitude": lng
											}]

curTime = min(programs.keys())
times = sorted(list(programs.keys()))


def getNextTime(curTime):
	if curTime >= max(programs.keys()):
		return None
	return times[bisect.bisect_right(times, curTime)]


data = {}

while True:
	target = programs[curTime][0]
	if target["DateTime"] != target["DateTimeOriginal"]:
		addrfrom = target["longitude"]
		if target["MeteringMode"] & 1:
			addrfrom = data[target["longitude"]]
		if data[addrfrom] >= 0:
			curTime = target["DateTime"]
			time.sleep(abs((curTime - target["DateTimeOriginal"]).total_seconds()) / 20)
	else:
		addrfrom = target["longitude"]
		if target["MeteringMode"] & 1:
			addrfrom = data[target["longitude"]]
		addrto = target["latitude"]
		if target["MeteringMode"] & 2:
			addrto = data[target["latitude"]]

		if target["command"] == "substitution":
			data[addrto] = target["width"] * target["height"]
		elif target["command"] == "input":
			data[addrto] = ord(sys.stdin.buffer.read(1))
		elif target["command"] == "output":
			sys.stdout.buffer.write(chr(data[addrfrom]).encode("ascii"))
		elif target["command"] == "addition":
			data[addrto] += data[addrfrom]
		elif target["command"] == "substraction":
			data[addrto] -= data[addrfrom]
		elif target["command"] == "multiplicatoin":
			data[addrto] *= data[addrfrom]
		elif target["command"] == "division":
			data[addrto] //= data[addrfrom]
		elif target["command"] == "remainder":
			data[addrto] %= data[addrfrom]
	curTime = getNextTime(curTime)
	if curTime is None:
		break
