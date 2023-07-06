import unittest
import os
from Voice_Onset import onset

def run_tests():
    # Create a test suite
    suite = unittest.TestSuite()

    # Add the test cases to the suite
    suite.addTest(TestBinarySearch('test_binary_search'))
    suite.addTest(TestBinarySearch('test_cosine_similarity'))

    # Run the test suite
    unittest.TextTestRunner().run(suite)

class TestBinarySearch(unittest.TestCase):
    def setUp(self):
        self.audio_files = self.find_audio_files()

    def test_binary_search(self):
        # Test with English audio file and target word "hello"
        audio_input = self.get_audio_path("001_1.wav")
        language_used = "en-US"
        target_word = "hello"
        self.assertTrue(os.path.isfile(audio_input), f"File '{audio_input}' not found.")
        found_word, onset_value_found = onset.binary_search(audio_input, language_used, target_word, decision_value=0)
        self.assertAlmostEqual(float(onset_value_found), 0.6498, places=2)
        print("Test English Audio File passed")

    def test_cosine_similarity(self):
        # Compare similar words
        cosine_value = onset.word_distance_caluclated("Bird", "Bird", "all-mpnet-base-v2")
        self.assertAlmostEqual(cosine_value, 1, places=2)
        print("Test Similar Words Passed")

    def find_audio_files(self):
        audio_files = []
        for root, dirs, files in os.walk("/"):
            for filename in files:
                if filename.endswith(".wav"):
                    audio_files.append(os.path.join(root, filename))
        return audio_files

    def get_audio_path(self, filename):
        for audio_file in self.audio_files:
            if os.path.basename(audio_file) == filename:
                return audio_file
        raise FileNotFoundError(f"File '{filename}' not found.")

if __name__ == '__main__':
    run_tests()



