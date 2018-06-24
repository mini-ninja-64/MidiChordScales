from midiutil.MidiFile import MIDIFile
import os

track = 0
time = 0
channel = 0
volume = 100
duration = 4
A=45

#minor(0),major(1),augmented(2),diminished(3)
triadDisplacement = [[3, 7], [4, 7], [4, 8], [3, 6]]
triadNames = ["Minor","Major","Augmented","Diminished"]
#minor7(0),major7(1),minor major7(2),1/2Diminished7(3),Diminished7(4),augmented7(5),Dominant7(6)
#Minor(0),Major(1),Minor Major(2),Half Diminished(3),Diminished(4),Augmented(5),Augmented Major(6),Dominant(7)
seventhDisplacement = [[3, 7, 10], [4, 7, 11], [3, 7, 11], [3, 6, 10], [3, 6, 9], [4, 8, 10], [4, 8, 11], [4, 7, 10]]
seventhNames = ["Minor","Major","Minor Major","Half Diminished","Diminished","Augmented","Augmented Major","Dominant"]
#notes
notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
majorScaleDisplacement = [0,2,4,5,7,9,11,12]
minorScaleDisplacement = [0,2,3,5,7,8,10,12]
#chord types for different scales
majorTriad = [1,0,0,1,1,0,3]
major7th = [1,0,0,1,7,0,3]
minorTriad = [0,3,1,0,0,1,1]
minor7th = [0,3,1,0,0,1,7]

#How to calculate scales
#Major Scale: Root, Root+2, Root+4, Root+5, Root+7, Root+9, Root+11, Root+12
#Minor Scale: Root, Root+2, Root+3, Root+5, Root+7, Root+8, Root+10, Root+12

def saveTriad(chordName, root, _type, key):
	name = chordName + " " + triadNames[_type] + " Triad"
	mf = MIDIFile(1)
	mf.addTrackName(track, time, name)
	mf.addTempo(track, time, 120)

	mf.addNote(track, channel, root, time, duration, volume)
	mf.addNote(track, channel, root+triadDisplacement[_type][0], time, duration, volume)
	mf.addNote(track, channel, root+triadDisplacement[_type][1], time, duration, volume)

	filename = key+"/"+name+".mid"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'wb') as outf:
		mf.writeFile(outf)

def save7th(chordName, root, _type, key):
	name = chordName + " " + seventhNames[_type] + " 7th"
	mf = MIDIFile(1)
	mf.addTrackName(track, time, name)
	mf.addTempo(track, time, 120)

	mf.addNote(track, channel, root, time, duration, volume)
	mf.addNote(track, channel, root+seventhDisplacement[_type][0], time, duration, volume)
	mf.addNote(track, channel, root+seventhDisplacement[_type][1], time, duration, volume)
	mf.addNote(track, channel, root+seventhDisplacement[_type][2], time, duration, volume)

	filename = key+"/"+name+".mid"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'wb') as outf:
		mf.writeFile(outf)

def saveScale(scaleNoteArrays, key):
	mf = MIDIFile(1)
	mf.addTrackName(track, time, key)
	mf.addTempo(track, time, 120)

	for i in range(0, 8): #7 notes in a scale as supertonic will be repeated
		for r in range(0, 9): #8 octave repeats
			mf.addNote(track, channel, 9+(r*12)+scaleNoteArrays[i], time, duration, volume) #9 is first A

	filename = "Scales/"+key+".mid"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'wb') as outf:
		mf.writeFile(outf)

for i in range(0, 12):
	#save major
	tempNotesForKey = [i]
	print("Key: "+notes[i]+" Major")
	for n in range(0,7):
		noteIndex = i+majorScaleDisplacement[n]
		noteIndexPrint = noteIndex
		if (noteIndexPrint>11):
			noteIndexPrint-=12
		tempNotesForKey.append(noteIndex) #append note for scale
		saveTriad(notes[noteIndexPrint], A+noteIndex, majorTriad[n], notes[i]+" Major")
		save7th(notes[noteIndexPrint], A+noteIndex, major7th[n], notes[i]+" Major")
		print("\t"+notes[noteIndexPrint])


	#save major scale
	saveScale(tempNotesForKey, notes[i]+" Major")

	#save minor
	tempNotesForKey = [i]
	print("Key: "+notes[i]+" Minor")
	for n in range(0, 7):
		noteIndex = i+minorScaleDisplacement[n]
		noteIndexPrint = noteIndex
		if (noteIndexPrint>11):
			noteIndexPrint-=12
		tempNotesForKey.append(noteIndex) #append note for scale
		saveTriad(notes[noteIndexPrint], A+noteIndex, minorTriad[n], notes[i]+" Minor")
		save7th(notes[noteIndexPrint], A+noteIndex, minor7th[n], notes[i]+" Minor")
		print("\t"+notes[noteIndexPrint])

	#save minor scale
	saveScale(tempNotesForKey, notes[i]+" Minor")



