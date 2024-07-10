from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Sample paragraph
# text = "The Industrial Revolution marked a significant turning point in human history, beginning in the 18th century and continuing through the 19th century. It was characterized by rapid industrialization, technological advancements, and social changes that transformed economies and societies across the globe. Key innovations such as the steam engine, textile machinery, and the telegraph revolutionized manufacturing, communication, and transportation. This era saw the rise of factories, urbanization, and mass production, leading to profound shifts in labor patterns and living conditions. The Industrial Revolution also spurred economic growth, trade expansion, and the emergence of new industries such as iron and steel production. However, it was not without its challenges, including harsh working conditions, child labor, and social inequalities. The movement for workers' rights and labor reforms gained momentum in response to these issues. Overall, the Industrial Revolution reshaped the world, laying the groundwork for modern industrial economies and shaping the course of technological progress and social development."

# Function summarizing large bodies of text using sumy library
def get_summary(input_text : str, sentence_amount : int) -> str :
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_amount)  
    return " ".join([str(sentence) for sentence in summary])

# Testing the summarizing function
# text1 = summarize(text, 4)
# print(text1)

