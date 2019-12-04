import rospy
from qt_nuitrack_app.msg import Hands
from std_msgs.msg import Int8
class handsTracking:

	hands = None
	rightHandPosition = None
	
	def __init__(self):

		self.handsSub = rospy.Subscriber("qt_nuitrack_app/hands", Hands, self.handsCallback)

	def handsCallback(self, data):

		self.hands = data.hands[0]

		self.rightHandPosition = self.hands.right_projection #Only one element in list

	def getHandPosition(self):
	
		return self.rightHandPosition

class getInterval:

	interval = None
	hands = handsTracking()
	intervalList = [0,0.083,0.166,0.25,0.332,0.415,0.5,0.581,0.664,0.747,0.85,0.913,1]

	def __init__(self):

		self.intervalPub = rospy.Publisher('/QTInstrument/interval', Int8, queue_size = 1)		
	def findInterval(self):
		if self.hands.rightHandPosition == None or self.hands.rightHandPosition[0] == -1:
			return
		for i in range(12):
			if self.intervalList[i] < self.hands.rightHandPosition[0] and self.hands.rightHandPosition[0] < self.intervalList[i+1]: #Compare the position of hand to the bonds of 12 equal zones
				self.interval = i+1 #Registers the zone where hand is detected
				print(self.interval)
				self.intervalPub.publish(self.interval)
				break
			
def main():
	
	interval = getInterval()

	rospy.init_node("intervalNode", anonymous = True)
	
	rate = rospy.Rate(2.5)

	try:
		while not rospy.is_shutdown():
			interval.findInterval()
			rate.sleep()
	except KeyboardInterrupt:
		print("Shutting down")



main()

