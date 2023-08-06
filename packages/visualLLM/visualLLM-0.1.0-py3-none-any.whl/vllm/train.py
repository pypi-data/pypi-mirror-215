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

import sys

sys.path.append("./")

import torch
from torch import nn

from vllm.data import VLLMDataset
from vllm.transformer import VLLMTransformer


class VLLMContext:
    def __init__(self):
        from vllm.config import Settings

        self.config = Settings()

    def override(self, name, value):
        self.config = self.config.copy(update={name: value})

    def override_config(self, config_dict: dict):
        self.config = self.config.copy(update=config_dict)


class VLLMTrainer:
    def __init__(self, ctx=VLLMContext()):
        self.ctx = VLLMContext()
        self.epochs = ctx.config.epochs
        self.log_every = ctx.config.log_every
        # load trainer
        self.load()

    def load(self):
        self.dataset = VLLMDataset(self.ctx, filepath="./dailogs.txt")
        self.dataset.set_language_index()
        self.ctx.override("vocab_size", self.dataset.vocab_size)

        self.transformer = VLLMTransformer(self.ctx)

        self.criterian = nn.CrossEntropyLoss(reduction="none")
        self.optim = torch.optim.Adam(self.transformer.parameters(), lr=1e-4)

    def train(self):
        dataset = self.dataset.load()
        for epoch in range(self.epochs):

            for batch_ix, batch_data in enumerate(dataset):
                self.optim.zero_grad()
                self.transformer.train()
                encoder_x, decoder_x, ground_truth = batch_data
                logits = self.transformer(encoder_x, decoder_x)

                # get loss
                loss = self.criterian(
                    logits.view(-1, self.dataset.vocab_size), ground_truth.view(-1)
                )

                valid_indices = torch.where(
                    ground_truth.view(-1)
                    == self.dataset.language_to_index[self.dataset.PADDING_TOKEN],
                    False,
                    True,
                )

                loss = loss.sum() / valid_indices.sum()

                # backprapogate
                loss.backward()

                self.optim.step()

                if batch_ix % self.log_every == 0:
                    print(
                        f"Iteration: {batch_ix} Epoch: {epoch} Loss is",
                        loss.detach().numpy(),
                    )
        return self.transformer


if __name__ == "__main__":
    trainer = VLLMTrainer()
    model = trainer.train()
