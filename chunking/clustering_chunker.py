from chunking.chunker import Chunker
import numpy as np
import spacy

class ClusteringChunker(Chunker):
    
    def chunk_text(self,text)-> list[str]:
        
        # Initialize the clusters lengths list and final texts list
        clusters_lens = []
        final_texts = []
        

        # Process the chunk
        threshold = 0.3
        sents, vecs = process(text)

        # Cluster the sentences
        clusters = cluster_text(sents, vecs, threshold)

        for cluster in clusters:
            cluster_txt = clean_text(' '.join([sents[i].text for i in cluster]))
            cluster_len = len(cluster_txt)
        
            # Check if the cluster is too short
            if cluster_len < 60:
                continue
            
            # Check if the cluster is too long
            elif cluster_len > 3000:
                threshold = 0.6
                sents_div, vecs_div = process(cluster_txt)
                reclusters = cluster_text(sents_div, vecs_div, threshold)
                #reclustering processing starts here 
                for subcluster in reclusters:
                    div_txt = clean_text(' '.join([sents_div[i].text for i in subcluster]))
                    div_len = len(div_txt)
                    
                    if div_len < 60 or div_len > 3000:
                        continue
                    
                    clusters_lens.append(div_len)
                    final_texts.append(div_txt)
                    #doc = Document(page_content=final_texts, metadata={"source": file_path})
                    
            else:
                clusters_lens.append(cluster_len)
                final_texts.append(cluster_txt)
                
        return final_texts


def process(text):
    # Load the Spacy model
    # This line loads the English language model (en_core_web_sm) provided by spaCy.
    #  The model is responsible for tokenizing, parsing, and tagging text.
    nlp = spacy.load('en_core_web_sm')
    # It processes the input text (text) using the spaCy pipeline and creates a Doc object, 
    # which contains information about the processed text, including tokens, 
    # part-of-speech tags, and other linguistic features.
    doc = nlp(text)
    # It extracts a list of sentences from the processed document (doc). 
    # The sents variable will contain individual spaCy Span objects, each representing a sentence in the text.
    sents = list(doc.sents)
    #This line creates a NumPy array (vecs) by stacking the vectors of each sentence in the sents list. 
    # Each sentence vector is normalized by dividing it by its vector norm.
    #sent.vector: Retrieves the vector representation of a sentence.
    #sent.vector_norm: Retrieves the L2 norm (Euclidean norm) of the sentence vector.
    #The list comprehension iterates over each sentence in sents, divides its vector by its norm, 
    # and then the resulting vectors are stacked using np.stack() to create a 2D NumPy array.
    vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])

    return sents, vecs

def cluster_text(sents, vecs, threshold):
    clusters = [[0]]
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i-1]) < threshold:
            clusters.append([])
        clusters[-1].append(i)
    
    return clusters

def clean_text(text):
    # Add your text cleaning process here
    return text