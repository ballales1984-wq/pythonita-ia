"""
Modulo per l'addestramento di modelli di classificazione
per riconoscere comandi Python da frasi in italiano.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense


def addestra_modello_classificazione(csv_path="frasi.csv"):
    """
    Addestra un modello di classificazione multi-classe per riconoscere comandi.
    
    Args:
        csv_path: percorso al file CSV con colonne 'frase' e 'etichetta'
    
    Returns:
        tuple: (model, tokenizer, label_index)
    """
    df = pd.read_csv(csv_path)
    frasi = df["frase"].values
    etichette = df["etichetta"].values

    # Tokenizzazione
    tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
    tokenizer.fit_on_texts(frasi)
    sequenze = tokenizer.texts_to_sequences(frasi)
    sequenze_padded = pad_sequences(sequenze, maxlen=10)

    # Encoding delle etichette
    label_index = {label: i for i, label in enumerate(set(etichette))}
    etichette_num = [label_index[label] for label in etichette]

    # Split dei dati
    X_train, X_test, y_train, y_test = train_test_split(
        sequenze_padded, etichette_num, test_size=0.2, random_state=42
    )

    # Creazione modello
    model = Sequential([
        Embedding(1000, 16, input_length=10),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(len(label_index), activation='softmax')
    ])

    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    
    # Addestramento
    model.fit(X_train, y_train, epochs=30, verbose=1, validation_data=(X_test, y_test))

    return model, tokenizer, label_index


def addestra_modello_generico(X_train, y_train):
    """
    Addestra un modello generico per classificazione binaria.
    
    Args:
        X_train: features di training
        y_train: labels di training
    
    Returns:
        model: modello addestrato
    """
    X_train = np.array(X_train, dtype=np.float32)
    y_train = np.array(y_train, dtype=np.float32)

    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.fit(X_train, y_train, epochs=30, verbose=1)

    return model
