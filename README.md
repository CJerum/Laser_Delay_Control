Code in Python written to interface with two delay generators in accordance with a delay line setup in the Extreme State Physics Laboratory (XSPL).

If completed, the code would be able to send commands to 3 pieces of equipment: An SDG2000x Arbitrary Waveform Generator, a DG535 Delay Generator, and a Canon Camera. The code is currently capable of updating the two delay generators simultaneously, but the ability to subsequently trigger the canon camera to capture data
(which in this case is an interferogram of a laser-produced plasma spark) was never finished.

If I ever fix the input port of the DG535, then this code enables fully automatic unsupervised data collection, as opposed to manually adjusting each delay generator, then manually taking a photo on the camera, then repeating (which is a tedious, time consuming process).
