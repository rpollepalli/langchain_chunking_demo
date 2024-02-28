import pandas as pd

class ChunkingUtils():
    
    def data_frame_utils(raw_text, embeddings):
        merged_list = [(raw_text[i], embeddings[i]) for i in range(0, len(raw_text))]
        df = pd.DataFrame([merged_list])
        df.columns =["content" , "embedding"]
        return df