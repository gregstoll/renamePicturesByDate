import sys, os, re, datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exifpy'))
import exifread

def renamePhotos(path, splitByYear):
	dirs = []
	if splitByYear:
		for name in os.listdir(path):
			# only include years
			if (re.match(r'^\d{4}$', name) and os.path.isdir(os.path.join(name, path))):
				dirs.append(os.path.join(path, name))
	else:
		dirs = [path]

	#print(dirs)
	for yearDir in dirs:
		for root, dir, files in os.walk(yearDir):
			for filename in files:
				if not (filename.endswith('.JPG') or filename.endswith('.jpg')):
					continue
				startsWithImg = filename.startswith('IMG_')
				pathname = os.path.join(root, filename)
				#print(filename)
				f = open(pathname, 'rb')
				tags = exifread.process_file(f, details=False)
				if 'EXIF DateTimeOriginal' not in tags:
					print ("No DateTimeOriginal for %s!" % pathname)
					continue
				dtString = str(tags['EXIF DateTimeOriginal'])
				#print('original ' + str(tags['EXIF DateTimeOriginal']))
				dt = datetime.datetime.strptime(dtString, '%Y:%m:%d %H:%M:%S')
				def makeFilename(localDt):
					format = '%Y%m%d_%H%M%S.jpg'
					if startsWithImg:
						format = 'IMG_' + format
					return localDt.strftime(format)
				newFilename = makeFilename(dt)
				#print('dig ' + str(tags['EXIF DateTimeDigitized']))
				#for tag in tags.keys():
				#	print(tag)

				f.close()
				while (os.path.isfile(os.path.join(root, newFilename))):
					dt = dt + datetime.timedelta(seconds=1)
					newFilename = makeFilename(dt)
				print('%s -> %s' % (filename, newFilename))
				os.rename(os.path.join(root, filename), os.path.join(root, newFilename))


if (__name__ == '__main__'):
	if (len(sys.argv) > 1):
		renamePhotos(sys.argv[1], False)
	else:
		print("Usage: renamePicturesByDate.py <directory>")
		sys.exit(1)
