import pandas as pd, numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
#from sklearn.model_selection import StratifiedKFold
from transformers import *
import tokenizers
#print('TF version', tf.__version__)


class SentimentModel:
    def __init__(self, vocap_pth, merges_pth, model_path, max_len=96):
        self.max_len = max_len
        self.tokenizer = tokenizers.ByteLevelBPETokenizer(
            vocab=vocap_pth,
            merges=merges_pth,
            lowercase=True,
            add_prefix_space=True
        )
        text = "This is Donald Trump"
        encoding = self.tokenizer.encode(text)
        #print(f"Encoded text IDs: {encoding.ids}")
       
        self.sentiment_id = {'positive': 1313, 'negative': 2430, 'neutral': 7974}
        self.model = self.build_model(path=model_path)
        
    
    def build_model(self, path):
        ids = tf.keras.layers.Input((self.max_len,), dtype=tf.int32, name="Input_Tokens")
        att = tf.keras.layers.Input((self.max_len,), dtype=tf.int32, name="Attention_Mask")
        tok = tf.keras.layers.Input((self.max_len,), dtype=tf.int32, name="Token_Types")

        config = RobertaConfig.from_pretrained(path+'config-roberta-base.json')
        bert_model = TFRobertaModel.from_pretrained(path+'pretrained-roberta-base.h5', config=config)
        x = bert_model(ids, attention_mask=att, token_type_ids=tok)

        x1 = tf.keras.layers.Dropout(0.1)(x[0]) 
        x1 = tf.keras.layers.Conv1D(1,1)(x1)
        x1 = tf.keras.layers.Flatten()(x1)
        x1 = tf.keras.layers.Activation('softmax')(x1)

        x2 = tf.keras.layers.Dropout(0.1)(x[0]) 
        x2 = tf.keras.layers.Conv1D(1,1)(x2)
        x2 = tf.keras.layers.Flatten()(x2)
        x2 = tf.keras.layers.Activation('softmax')(x2)

        model = tf.keras.models.Model(inputs=[ids, att, tok], outputs=[x1,x2])
        model.load_weights(path + "weights_final.h5")

        return model
    
    def predict(self, input_text, sentiment):
        if sentiment not in self.sentiment_id:
            return "Sentiment error"
        if len(input_text) == 0:
            return "Empty input text"
        
        # transform input for roberta model
        text = " " + " ".join(input_text.split())
        enc = self.tokenizer.encode(text)                
        s_tok = self.sentiment_id[sentiment]
        
        input_ids = [0] + enc.ids + [2,2] + [s_tok] + [2]
        attention_mask = [1] * len(input_ids)
        token_type_ids = [0] * self.max_len
        
        pad_length = self.max_len - len(input_ids)
        # check if input fits into max_len
        if pad_length > 0:
            input_ids = input_ids + ([1] * pad_length)
            attention_mask = attention_mask + ([0] * pad_length)
        else:
            input_ids = input_ids[:self.max_len]
            attention_mask = attention_mask[:self.max_len]
        
        model_input = {
            "Input_Tokens": np.array([input_ids]),
            "Attention_Mask": np.array([attention_mask]),
            "Token_Types": np.array([token_type_ids])
        }
        
        # Model prediction
        start_pred, end_pred = self.model.predict(model_input)
        start_index = max(1, np.argmax(start_pred[0]))
        end_index = np.argmax(end_pred[0])
        # print(start_index)
        # print(end_index)
        
        # Check if predicted Indices make sense
        if end_index < start_index:
            return input_text
        else:
            filtered_tokens = enc.ids[start_index-1:end_index]
            filtered_text = self.tokenizer.decode(filtered_tokens)
            return filtered_text
            

if __name__ == "__main__":
    path = './config/'
    vocap_pth = path+'vocab-roberta-base.json'
    merges_pth = path+'merges-roberta-base.txt'
    
    input_text = "Das Wetter ist heute super schön."
    #input_text = "I really really like the song Love Story by Taylor Swift"
    #input_text = " a celtics-lakers rematch sounds better don`t you think? lol"
    sentiment = "positive"
    
    model = SentimentModel(vocap_pth=vocap_pth, merges_pth=merges_pth, model_path=path)
    output = model.predict(input_text, sentiment)
    print("Predicted Subtext: ", output)

