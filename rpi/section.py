print("init")
import time
import logging

from gpiozero import Motor

DIRECTIONS = ("forward", "backward", None)

logging.basicConfig()
LOGGER = logging.getLogger(name="PyTrain")
LOGGER.setLevel(logging.INFO)
#LOGGER.setLevel(logging.DEBUG)

class Section(Motor):

	def __init__(self, id_, gpio1, gpio2, length, name=None):
		super(Section, self).__init__(gpio1, gpio2, True)
		self.id_ = id_
		self.name = name if name else id_
		self.length = length
		self._logger = LOGGER.getChild("section.{}".format(self.id_))
		self._logger.info("init")

		self._speed = 0
		self._direction = None

	def forward(self, speed=1):
		"""Going forward"""
		self._logger.info("Going forward with speed: %s", speed)
		self._accelerate("forward", speed)

	def backward(self, speed=1):
		"""Going backward"""
		self._logger.info("Going backward with speed: %s", speed)
		self._accelerate("backward", speed)

	def stop(self):
		"""Stop section"""
		self._logger.info("Stopping section")
		self._accelerate(self._direction, 0)

	def _accelerate(self, new_direction, new_speed):
		"""Accelerate or deccelerate or stopping"""
		# Check direction
		if new_direction not in DIRECTIONS:
			raise ValueError("Bad direction: {}".format(new_direction))
		# If direction is None, we assume this means stop
		elif new_direction is None:
			self._logger.debug("Direction is None, assuming stopping te section")
			new_speed = 0

		# Check spees
		if new_speed < 0 or new_speed > 1:
			raise ValueError("Bad speed: {}".format(new_speed))

		if self._direction is not None and new_direction != self._direction:
			# change direction
			self._logger.debug("Changing direction from %s to %s", self._direction, new_direction)
			self.stop()
			time.sleep(1)

		if new_speed == self._speed:
			# nothing to do
			self._logger.debug("No speed changes")
			return

		elif new_speed > self._speed:
			# Acceleration
			self._logger.info("Accelerate from %0.2f to %0.2f", self._speed, new_speed)
			speed_list = range(int(self._speed * 100),
							   int(new_speed * 100),
							   5)
			sleep_time = 0.2 
		else:
			# Decceleration
			self._logger.info("Deccelerate from %0.2f to %0.2f", self._speed, new_speed)
			speed_list = range(int(new_speed * 100),
							   int(self._speed * 100),
							   5)
			speed_list = reversed(speed_list)
			sleep_time = 0.1
		# Send quick impulsion to start engine
		if self._speed == 0:
			self._logger.info("Starting section impulsion")
			getattr(super(Section, self), new_direction)(1)
			time.sleep(0.01)

		# increase/decrease speed
		for speed in speed_list:
			# Elimate low speeds which making some electric noise to train engines
			if speed < 25:
				continue
			# Get speed between 0 and 1
			raw_speed = speed / 100
			self._logger.debug("Speed: {}".format(raw_speed))
			# Setting speed
			getattr(super(Section, self), new_direction)(raw_speed)
			# Saving speed
			self._speed = raw_speed
			# Saving direction
			self._direction = new_direction
			# Waiting for next acceleration
			time.sleep(sleep_time)

		if new_speed == 0:
			# Stop engine if new speed is 0
			self._direction = None
			super(Section, self).stop()
			self._logger.debug("Section stopped")
		else:
			# Last speed change
			getattr(super(Section, self), new_direction)(new_speed)
			self._logger.info("Wanted speed reached: %s", new_speed)


mysection = Section(1, 17, 18, 120, "first")
mysection.forward(0.6)
time.sleep(2)
#mysection.forward(0.4)
#time.sleep(2)

mysection.backward(0.6)
time.sleep(2)
#mysection.backward(0.4)
#time.sleep(2)


#for x in range(2):
#	mysection.forward(0.6)
#	time.sleep(3)
#	mysection.stop()
#	time.sleep(1)
#	mysection.backward(0.6)
#	time.sleep(3)
#	mysection.stop()
#	time.sleep(1)

mysection.stop()
