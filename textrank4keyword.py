from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

def extract_keyword(text_strg, num_keyword=5):
    nlp = spacy.load('en_core_web_sm')

    class TextRank4Keyword():
        """Extract keywords from text"""

        def __init__(self):
            self.d = 0.85 # damping coefficient, usually is .85
            self.min_diff = 1e-5 # convergence threshold
            self.steps = 10 # iteration steps
            self.node_weight = None # save keywords and its weight


        def set_stopwords(self, stopwords):  
            """Set stop words"""
            for word in STOP_WORDS.union(set(stopwords)):
                lexeme = nlp.vocab[word]
                lexeme.is_stop = True

        def sentence_segment(self, doc, candidate_pos, lower):
            """Store those words only in cadidate_pos"""
            sentences = []
            for sent in doc.sents:
                selected_words = []
                for token in sent:
                    # Store words only with cadidate POS tag
                    if token.pos_ in candidate_pos and token.is_stop is False:
                        if lower is True:
                            selected_words.append(token.text.lower())
                        else:
                            selected_words.append(token.text)
                sentences.append(selected_words)
            return sentences

        def get_vocab(self, sentences):
            """Get all tokens"""
            vocab = OrderedDict()
            i = 0
            for sentence in sentences:
                for word in sentence:
                    if word not in vocab:
                        vocab[word] = i
                        i += 1
            return vocab

        def get_token_pairs(self, window_size, sentences):
            """Build token_pairs from windows in sentences"""
            token_pairs = list()
            for sentence in sentences:
                for i, word in enumerate(sentence):
                    for j in range(i+1, i+window_size):
                        if j >= len(sentence):
                            break
                        pair = (word, sentence[j])
                        if pair not in token_pairs:
                            token_pairs.append(pair)
            return token_pairs

        def symmetrize(self, a):
            return a + a.T - np.diag(a.diagonal())

        def get_matrix(self, vocab, token_pairs):
            """Get normalized matrix"""
            # Build matrix
            vocab_size = len(vocab)
            g = np.zeros((vocab_size, vocab_size), dtype='float')
            for word1, word2 in token_pairs:
                i, j = vocab[word1], vocab[word2]
                g[i][j] = 1

            # Get Symmeric matrix
            g = self.symmetrize(g)

            # Normalize matrix by column
            norm = np.sum(g, axis=0)
            g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm

            return g_norm


        # def get_keywords(self, number=10):
        #     """Print top number keywords"""
        #     node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        #     for i, (key, value) in enumerate(node_weight.items()):
        #         #print(key + ' - ' + str(value))
        #         print(key)
        #         if i > number:
        #             break
        def get_keywords(self, number=10):
            """Return top number keywords"""
            node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
            keywords = []
            for i, (key, value) in enumerate(node_weight.items()):
                if i >= number:
                    break
                keywords.append(key)
            return keywords

                
        def analyze(self, text, 
                    candidate_pos=['NOUN', 'PROPN'], 
                    window_size=4, lower=False, stopwords=list()):
            """Main function to analyze text"""

            # Set stop words
            self.set_stopwords(stopwords)

            # Pare text by spaCy
            doc = nlp(text)

            # Filter sentences
            sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words

            # Build vocabulary
            vocab = self.get_vocab(sentences)

            # Get token_pairs from windows
            token_pairs = self.get_token_pairs(window_size, sentences)

            # Get normalized matrix
            g = self.get_matrix(vocab, token_pairs)

            # Initionlization for weight(pagerank value)
            pr = np.array([1] * len(vocab))

            # Iteration
            previous_pr = 0
            for epoch in range(self.steps):
                pr = (1-self.d) + self.d * np.dot(g, pr)
                if abs(previous_pr - sum(pr))  < self.min_diff:
                    break
                else:
                    previous_pr = sum(pr)

            # Get weight for each node
            node_weight = dict()
            for word, index in vocab.items():
                node_weight[word] = pr[index]

            self.node_weight = node_weight


    # with open("content0.txt", "r") as f:
    #     text_strg = f.read()

    clean_data = text_strg
    #clean_data = re.sub('[^a-zA-Z\s]', '', text_strg)
    clean_data = ' '.join(clean_data.split())
    clean_data = clean_data.lower()

    tr4w = TextRank4Keyword()
    tr4w.analyze(clean_data, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
    return(tr4w.get_keywords(num_keyword))

    #DOCUMENTATION: remember to use python3 -m space download en to install the model first.
#extract_keyword("""Tesla says it has no plans to stabilise the prices of its popular electric vehicles, despite repeated price cuts denting its profits.The car company led by billionaire Elon Musk is grappling with the impact of increased competition and higher borrowing costs on buyers. It has responded to the pressures by slashing prices repeatedly this year.It warned investors on Wednesday that product pricing would continue to "evolve, upwards or downwards"."We're not 'starting a price war', we're just lowering prices to enable affordability at scale," Mr Musk wrote on his social media platform, Twitter, earlier this month. Tesla said overall revenue in the first three months of the year rose to $23.3bn (Â£18.4bn), up 24% from a year ago, as car sales increased. But profit in the same period dropped 24% from a year earlier, to $2.5bn (Â£2bn).Tesla, which stands out among electric carmakers for its profitability, told investors that over the long term profits would remain strong, noting that the "lifetime value" of its cars could be boosted by ongoing payments for service, super charging and other features."We continue to believe that our operating margin will remain among the highest in the industry," it said in a quarterly financial update.Tesla bucked a wider decline in car sales last year, helped by booming interest in electric vehicles. But its market share has shown signs of eroding, as rivals launch electric vehicles of their own. Meanwhile Tesla deliveries have lagged the firm's output, which has increased dramatically since last year, stoking speculation that demand may be weaker than it had hoped. The company blamed the mismatch on slower deliveries of vehicles.But the company said that price cuts will help keep customers coming - though the sudden decreases in price led to outcry from some customers earlier this year who had paid more.The firm delivered nearly 423,000 cars in the three months to March. That was up 36% from last year but only 4% more than in the prior quarter.""", 10)