# Copyright 2023 kartik4949. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================

import re

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

START_TOKEN = "<start>"
PADDING_TOKEN = "<pad>"
END_TOKEN = "<end>"

english_vocabulary = [
    START_TOKEN,
    " ",
    ";",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    PADDING_TOKEN,
    END_TOKEN,
]


class TextDataset(Dataset):
    def __init__(self, encoder_x, decoder_x, decoder_y):
        self.encoder_x = encoder_x
        self.decoder_x = decoder_x
        self.decoder_y = decoder_y

    def __len__(self):
        return len(self.decoder_y)

    def __getitem__(self, idx):
        return self.encoder_x[idx], self.decoder_x[idx], self.decoder_y[idx]


class VLLMDataset:
    PADDING_TOKEN = PADDING_TOKEN

    def __init__(self, ctx, filepath=None):
        self.filepath = filepath
        self.df = None
        self.language_to_index = {}
        self.ctx = ctx

    @property
    def vocab_size(self):
        if self.language_to_index:
            return len(self.language_to_index)
        else:
            raise ValueError

    def set_language_index(self):
        self.language_to_index = {v: k for k, v in enumerate(english_vocabulary)}

    def load_file(self):
        df = pd.read_csv(self.filepath, sep="\t", names=["question", "answer"])
        print(f"Dataframe size: {len(df)}")
        df.head()
        return df

    def clean(self, df):
        def clean_text(text):
            text = re.sub("-", " ", text.lower())
            text = re.sub("[.]", " . ", text)
            text = re.sub("[1]", " 1 ", text)
            text = re.sub("[2]", " 2 ", text)
            text = re.sub("[3]", " 3 ", text)
            text = re.sub("[4]", " 4 ", text)
            text = re.sub("[5]", " 5 ", text)
            text = re.sub("[6]", " 6 ", text)
            text = re.sub("[7]", " 7 ", text)
            text = re.sub("[8]", " 8 ", text)
            text = re.sub("[9]", " 9 ", text)
            text = re.sub("[0]", " 0 ", text)
            text = re.sub("[,]", " , ", text)
            text = re.sub("[?]", " ? ", text)
            text = re.sub("[!]", " ! ", text)
            text = re.sub("[$]", " $ ", text)
            text = re.sub("[&]", " & ", text)
            text = re.sub("[/]", " / ", text)
            text = re.sub("[:]", " : ", text)
            text = re.sub("[;]", " ; ", text)
            text = re.sub("[*]", " * ", text)
            text = re.sub("[']", " ' ", text)
            text = re.sub('[\\"]', ' \\" ', text)
            text = re.sub("\t", " ", text)
            return text

        df["encoder_inputs"] = df["question"].apply(clean_text)
        df["decoder_targets"] = df["answer"].apply(clean_text) + f" {END_TOKEN}"
        df["decoder_inputs"] = (
            f"{START_TOKEN} " + df["answer"].apply(clean_text) + f" {END_TOKEN}"
        )
        return df

    def tokenize(self, x):
        tokenized = []
        for sentence in x:
            sentence_word_indicies = []
            for token in list(sentence):
                try:
                    ix = self.language_to_index[token]
                except KeyError:
                    ix = self.language_to_index[" "]
                sentence_word_indicies.append(ix)

            for _ in range(
                len(sentence_word_indicies), self.ctx.config.sequence_length
            ):
                sentence_word_indicies.append(self.language_to_index[PADDING_TOKEN])

            tensor_tokenized_words = torch.tensor(sentence_word_indicies)
            tokenized.append(tensor_tokenized_words)
        tokenized = torch.stack(tokenized)
        return tokenized

    def load(self):
        self.set_language_index()
        df = self.load_file()
        df = self.clean(df)

        # encoder input
        encoder_inputs = df["encoder_inputs"].tolist()
        encoder_inputs = self.tokenize(encoder_inputs)

        decoder_inputs = df["decoder_inputs"].tolist()
        decoder_inputs = self.tokenize(decoder_inputs)

        decoder_targets = df["decoder_targets"].tolist()
        decoder_targets = self.tokenize(decoder_targets)
        text_dataset = TextDataset(encoder_inputs, decoder_inputs, decoder_targets)
        return DataLoader(text_dataset, batch_size=self.ctx.config.batch_size)
