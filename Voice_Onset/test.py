import unittest
import os
from Voice_Onset import onset

class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        current_directory = os.getcwd()
        if "Sample_Data" not in current_directory:
            os.chdir(current_directory + os.sep + "Sample_Data")
       
        # Test with English audio file and target word "hello"
        audio_input = "001_1.wav"
        language_used = "en-US"
        target_word = "hello"
        found_word, onset_value_found = onset.binary_search(audio_input, language_used, target_word, decision_value=0)
        self.assertAlmostEqual(float(onset_value_found), 0.6498, places=2)
        print("Test English Audio File passed")
        
        # Test with German audio file and target word "hallo"
        audio_input = "002_1.wav"
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

    def test_adjusting_audio(self):
        #Testing whether the files are changed to the right type
        current_directory = os.getcwd()
        if "Sample_Data" not in current_directory:
            os.chdir(current_directory + os.sep + "Sample_Data")
        audio_input = "003_3.wav"
        audio_name = onset.adjust_audio_input(audio_input)
        target_name = "NEW_" + audio_input
        os.remove(target_name)
        self.assertEqual(audio_name, "NEW_" + audio_input)
        print("Audio File Test Passed")

if __name__ == '__main__':
    unittest.main()