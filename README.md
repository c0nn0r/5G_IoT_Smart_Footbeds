Video of project in action: https://www.youtube.com/watch?v=HDl0rbA_3ew

What:
A Prototype set of Smart Footbeds including software, hardware, and experimental 5G M1/NB1 IoT connections for each independent footbed.

About:
I was hired as a consultant by the “Luminary” of Seattle-based startup JumpstartCSR (http://jumpstartcsr.com/) to develop a fully functioning prototype of their vision of 5G M1/NB1 IoT smart footbeds. The footbed concept is to connect with a cloud-based "state of the art cognitive expert ecosystem" called Holmz which "creates an integrated and connected health/wellness fitness experience aimed at optimizing physical performance while predicting and preventing the risk of muscular skeletal injury."

Each footbed incorporates a 10-point Force Strain Resistor (FSR) array to measure pressure across the foot in motion and at rest. The footbed also includes a 9-DOF IMU for dead-reckoning foot orientation. Data from the FSR and IMU are fused and formatted by a Python script running on a Raspberry PI before being sent to a central server over 5G IoT data connection.

This was a 6 week project, with final prototype being successfully demonstrated, and selected for advancement at “Hubraum” a 5G Internet of Things incubator that is part of Deutsch Telekom’s initiative to pipeline 5G IoT demonstrators (https://twitter.com/WTOllson/status/1056938337515106304).

With very limited technical specification from JumpstartCSR I was responsible for the entirety of design/build/test cycle on a very short timeline. Deliverables included:

(1) Hardware

	•	20x FSR array in shape of foot. 10x per footbed.
	•	20x resistor. 10x per footbed.
	•	4x ADC. 2x per footbed.
	•	2x 9dof IMU. 1x per footbed
	•	2x Raspberry Pi 3. 1x per footbed.
	•	2x Quectel BG96 5G M1/NB1 IoT radio development kit. 1x per footbed.

(2) Mechanical Design

	•	1x Right footbed
	•	1x Left footbed

(3) Software

	•	Linux Environment Preparation
	•	Python script

(4) 5G Network (Quectel LTE BG96 M1/NB1 IoT modem)

	•	M1/NB1 IoT Modem configuration for BELL, ROGERS, TELUS, T-Mobile USA (EDGE), & T-Mobile Netherlands.
	•	AT commands to send data from footbeds to JumpstartCSR server.
	•	5G IoT account management via Cisco Jasper tools.
