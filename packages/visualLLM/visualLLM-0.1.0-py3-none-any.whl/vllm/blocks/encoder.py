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

from .common import CommonTransformerUnit
from .embedding import PositionalEmbeddings


class VLLMEncoder(nn.Module):
    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()
        vocab_size = ctx.config.vocab_size
        embedding_dim = ctx.config.embedding_dim
        num_encoder_blocks = ctx.config.encoder_blocks

        self.embedding_layer = nn.Embedding(vocab_size, embedding_dim)
        self.positional_encoder = PositionalEmbeddings(ctx)
        self.encoder_blocks = nn.ModuleList(
            [CommonTransformerUnit(ctx) for _ in range(num_encoder_blocks)]
        )

    def forward(self, x):
        embed_out = self.embedding_layer(x)
        input_vector = self.positional_encoder(embed_out)
        for block in self.encoder_blocks:
            input_vector = block(input_vector, input_vector, input_vector)

        return input_vector
