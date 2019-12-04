import rospy
from std_msgs.msg import String, Int8

class intervalToNote:

	d = None
	path = "Octaves/Octave4/"

	def __init__(self):

		self.intervalSub = rospy.Subscriber('/QTInstrument/interval', Int8, self.noteSendCallback)
		self.notePub = rospy.Publisher('/qt_robot/audio/play', String, queue_size = 1)

	def noteSendCallback(self, data):
		self.d = str(data.data)
		self.d = self.d + '.wav'
		print(self.d)
		self.notePub.publish(self.path + self.d)

def main():
	
	note = intervalToNote()
	
	rospy.init_node("IntervalToNoteNode", anonymous = True)

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

main()


