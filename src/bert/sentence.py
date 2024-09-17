from keybert import KeyBERT

class SentenceBert:
    def __init__(self, sentence: str):
        """
        Initialize the SentenceBert class.

        Args:
            sentence (str): The sentence from which to extract keywords.
        """
        
        self.sentence = sentence
        self.kw_model = KeyBERT()

    def extract_keywords(self, top_n: int = 5) -> list:
        
        """
        Extract keywords from the given sentence.

        Args:
            top_n (int, optional): The number of keywords to return. Defaults to 5.

        Returns:
            list: A list of the top_n keywords extracted from the sentence.
        """

        keywords = self.kw_model.extract_keywords(
            self.sentence,
            keyphrase_ngram_range=(1, 1),
            stop_words='english',
            top_n=top_n,
            use_mmr=True,
            diversity=0.7
        )
        return keywords
