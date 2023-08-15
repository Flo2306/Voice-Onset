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
    print("\nAll Tests Passed")

class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        self.audio_files = self.find_audio_files()

    def test_binary_search(self):
        # Test with English audio file and target word "hello"
        audio_path = self.get_audio_directory("001_1.wav")
        audio_file = '001_1.wav'
        os.chdir(audio_path)
        language_used = "en-US"
        target_word = "hello"
        found_word, onset_value_found = onset.binary_search(audio_file, language_used, target_word, decision_value=0)
        self.assertAlmostEqual(float(onset_value_found), 0.6498, places=2)
        print("Test English Audio File passed")

        
        audio_path = self.get_audio_directory("002_1.wav")
        audio_input = "002_1.wav"
        os.chdir(audio_path)
        language_used = "de-DE"
        target_word = "hallo"
        found_word, onset_value_found = onset.binary_search(audio_input, language_used, target_word, decision_value= 0)
        self.assertAlmostEqual(float(onset_value_found), 1.021, places=2)
        print("Test German Audio File passed")

    def test_cosine_similarity(self):
        #Compare similar words
        cosine_value = onset.word_distance_caluclated("Bird", "Bird", "all-mpnet-base-v2")
        self.assertAlmostEqual(cosine_value, 1, places=2)
        print("Test Similar Words Passed")

        #Compare different words
        cosine_value = onset.word_distance_caluclated("Bird", "House", "all-mpnet-base-v2")
        self.assertAlmostEqual(cosine_value, 0.279, places=2)
        print("Test Different Words Passed")

        #Compare German Words 
        cosine_value = onset.word_distance_caluclated("Vogel", "Fisch", "distiluse-base-multilingual-cased-v2")
        self.assertAlmostEqual(cosine_value, 0.560, places=2)
        print("Test German Words Passed")

    def find_audio_files(self):
        audio_files = []
        for root, dirs, files in os.walk("/"):
            for filename in files:
                if filename.endswith(".wav"):
                    audio_files.append((root, filename))
        return audio_files

    def get_audio_directory(self, filename):
        for audio_directory, audio_filename in self.audio_files:
            if audio_filename == filename:
                return audio_directory
        raise FileNotFoundError(f"File '{filename}' not found.")

if __name__ == '__main__':
    run_tests()
