from chunking.chunker import Chunker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

class KmeansChunker(Chunker):
    """
    Implimentation of the interface Chunker
    """
    

    def chunk_text(self,text)-> list[str]:
        text_chunks = text.split('\n')
        print(len(text_chunks))
        num_clusters = 3
        
        # Perform K-means clustering on the text chunks
        # Create TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(text_chunks)

        # Apply TruncatedSVD for dimensionality reduction (optional)
        svd = TruncatedSVD(n_components=100)
        tfidf_matrix_svd = svd.fit_transform(tfidf_matrix)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(tfidf_matrix_svd)

        # Assign cluster labels to each document
        cluster_labels = kmeans.labels_

        return cluster_labels

        

    #print(len(sentences))

    #print(sentences)
    
    
    