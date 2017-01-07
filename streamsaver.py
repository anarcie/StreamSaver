	
import requests, os ,subprocess

#Stream
#streamer = 'nl_kripp'
streamer = 'sodapoppin'
stream_quality = 'high' 

#Save Options
save_location = '/media/quanternary/streams/'

def CheckStream():
	client_id = 'yryp0trc799327bj62kfrhnf04x8x7'
	url = "https://api.twitch.tv/kraken/streams/%s?client_id=%s" % (streamer, client_id)
	r = requests.get(url)
	stream = r.json()
	return stream

def RecordStream(filename, status): 
        print "New Stream, Recording as " + str(filename)
        command = "/usr/local/bin/streamlink http://www.twitch.tv/"+ streamer + " " + stream_quality +  " -o " + filename + " -f "
        create_file = 'touch ' + filename + ' ;  setfattr -n user.title -v "' + status + '" ' + filename
        print command
        subprocess.check_call(create_file , shell = True)
        subprocess.check_call(command, shell = True)

data = CheckStream()
if data['stream'] is not None:
	stream  = data['stream'] 
	id      = stream['_id'] 
	created = stream['created_at'].replace(":", "")
	status  = stream['channel']['status']

	print "---------------------------"
	print "Status: Online!"
	print "ID: " + str(id)
	print "Streamer:" + streamer.encode('utf-8').strip()
	print "Created: " + created.encode('utf-8').strip()
	print "Title: " + status.encode('utf-8').strip()

	filename = save_location + str(streamer) + "_" + str(id) + "_" + str(created) + ".mp4"
	if os.path.isfile(filename) == False:
		RecordStream(filename, status)
	else:
		print "File Already exists. Checking Size."		
		statinfo = os.stat(filename)
		if (statinfo.st_size == 0): 
			print "Empty File Found, Cleaning up and Recording"
			os.remove(filename)
			RecordStream(filename, status)
		else:
			print "Non Empty File, Exiting"
		print "---------------------------"

else:
	print "---------------------------"
	print "Offline" 

