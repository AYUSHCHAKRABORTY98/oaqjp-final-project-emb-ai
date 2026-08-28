from EmotionDetection import emotion_detection as ed
import unittest

class moduletest(unittest.TestCase):
    def test_emotion_detetctor(self):
        self.assertEqual(ed.emotion_detector("I am glad this happened")['dominant_emotion'],'joy')
        self.assertEqual(ed.emotion_detector("I am really mad about this")['dominant_emotion'],'anger')
        self.assertEqual(ed.emotion_detector("I feel disgusted just hearing about this")['dominant_emotion'],'disgust')
        self.assertEqual(ed.emotion_detector("I am so sad about this")['dominant_emotion'],'sadness')
        self.assertEqual(ed.emotion_detector("I am really afraid that this will happen")['dominant_emotion'],'fear')
if __name__ == "__main__":
    unittest.main()