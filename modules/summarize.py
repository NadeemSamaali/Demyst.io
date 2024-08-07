from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # You can use other summarizers like LuhnSummarizer, LexRankSummarizer, etc.

# Function extracting summary of a large body of text using sumy's LSA summarizer
def get_summary(text : str) -> str :
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    num_sentences = 5
    
    summary_output = []

    # Generate the summary
    summary = summarizer(parser.document, num_sentences)

    for sentence in summary:
        summary_output.append(str(sentence))

    return "".join(summary_output)