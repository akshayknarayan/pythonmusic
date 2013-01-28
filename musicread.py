import wave,numpy,struct
import matplotlib.pyplot as plot

def getPCMData(name):
	song = wave.open(name,'r')
	(nchannels, sampwidth, framerate, nframes, comptype, compname) = song.getparams()
	bytestring = song.readframes(nframes)
	song.close()
	num_samples = nframes * nchannels
	if sampwidth == 1: 
		fmt = "%iB" % num_samples # read unsigned chars
	elif sampwidth == 2:
		fmt = "%ih" % num_samples # read signed 2 byte shorts
	else:
		raise ValueError("Only supports 8 and 16 bit audio formats.")
	integer_data = struct.unpack(fmt, bytestring)
	del bytestring
	channels = [[] for _ in range(nchannels)]
	counter = 0
	for i in integer_data:
		if (counter % 2 == 0):
			channels[0].append(i)
		else:
			channels[1].append(i)
		counter += 1
	return (channels, framerate)
	
def magnitudinize(complex_list):
	return [abs(i) for i in complex_list]
	
def normalize(int_list, total, framesize=10):
	shortlist = []
	counter = 0
	for i in range(int(len(int_list)/framesize)):
		shortlist.append(numpy.mean(int_list[counter:counter+framesize])/total)
		counter+=framesize
	return shortlist

def graph(freqs, space, name):
	fig = plot.figure()
	ax = fig.add_subplot(111)
	xaxis = [int(i*space) for i in range(len(freqs))]
	ax.bar(xaxis, freqs, width=0.1)
	ax.grid(True)
	plot.savefig(name)

(channels, framerate) = getPCMData('tone2.wav')
print(len(channels))
freqs = [magnitudinize(numpy.fft.fft(a)) for a in channels]
del channels
high = [max(a) for a in freqs]
print(high)
#frequency spacing = framerate/num.of.frames * framerate (b/c of averaging in normalize)
freq_space = [(framerate/len(i))*framerate for i in freqs]
short_freqs = [normalize(a,t,framesize=framerate) for (a,t) in zip(freqs,high)]
print(len(freqs[0]), len(short_freqs[0]))
del freqs
graph(short_freqs[0],freq_space[0],'2toneleft')
graph(short_freqs[1],freq_space[1],'2toneright')
