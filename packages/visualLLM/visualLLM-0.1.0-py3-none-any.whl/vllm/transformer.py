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

import torch
import torch.nn as nn
import torch.nn.functional as F

from vllm.blocks import VLLMDecoder, VLLMEncoder
from vllm.mask import lookahead_mask


class VLLMTransformer(nn.Module):
    """VLLMTransformer.
    VLLMTransformer is a encoder decoder transformer model with
    visual context input support.
    """

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()
        self.vllm_encoder = VLLMEncoder(ctx)
        self.vllm_decoder = VLLMDecoder(ctx)
        self.ffl = nn.Sequential(
            nn.Linear(ctx.config.embedding_dim, ctx.config.embedding_dim),
            nn.ReLU(),
            nn.Linear(ctx.config.embedding_dim, ctx.config.vocab_size),
        )

    def inference(self, input_x, seed_target):
        """inference.
        inference function is a helper function to execute
        inference of input sequence to output sequence.

        Args:
            input_x: input sequence
            seed_target: output sequence with previous output added.
        """
        target_mask = lookahead_mask(seed_target)
        encoder_out = self.vllm_encoder(input_x)
        target_x = seed_target
        predicted_labels = []
        for word_counter in range(self.ctx.config.sequence_length):
            target_x = self.vllm_decoder(target_x, encoder_out, target_mask)
            target_x = target_x[:, word_counter, :]
            target_x = target_x.argmax(-1)
            predicted_labels.append(target_x.item())
            target_x = torch.unsqueeze(target_x, axis=0)
        return predicted_labels

    def forward(self, input_x, target_x):
        target_mask = lookahead_mask(target_x)
        encoder_out = self.vllm_encoder(input_x)
        outputs = self.vllm_decoder(target_x, encoder_out, target_mask)
        outputs = self.ffl(outputs)
        outputs = F.softmax(outputs, dim=-1)
        return outputs
