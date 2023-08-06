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
from .multihead import MaskedMultiHeadAttention


class InputDecoderBlock(nn.Module):
    """InputDecoderBlock."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()

        embedding_dim = ctx.config.embedding_dim

        self.attention = MaskedMultiHeadAttention(ctx)

        self.layer_normalization = nn.LayerNorm(embedding_dim)

        self.dropout = nn.Dropout(0.2)

    def forward(self, key, query, value, mask):
        attention_out = self.attention(key, query, value, mask)
        attention_residual_out = attention_out + value
        normalized_output = self.dropout(
            self.layer_normalization(attention_residual_out)
        )
        return normalized_output


class EncoderDecoderBlock(CommonTransformerUnit):
    """EncoderDecoderBlock."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__(ctx)


class DecoderBlock(nn.Module):
    """DecoderBlock."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()
        self.input_block = InputDecoderBlock(ctx)
        self.encoder_decoder_block = EncoderDecoderBlock(ctx)

    def forward(self, x, encoder_out, mask):
        x = self.input_block(x, x, x, mask)
        return self.encoder_decoder_block(x, encoder_out, encoder_out)


class VLLMDecoder(nn.Module):
    """VLLMDecoder."""

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
        self.decoder_blocks = nn.ModuleList(
            [DecoderBlock(ctx) for _ in range(num_encoder_blocks)]
        )

    def forward(self, x, encoder_out, mask):
        embed_out = self.embedding_layer(x)
        input_vector = self.positional_encoder(embed_out)
        for block in self.decoder_blocks:
            input_vector = block(input_vector, encoder_out, mask)

        return input_vector
