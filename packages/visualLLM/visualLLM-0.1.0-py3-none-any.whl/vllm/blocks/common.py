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

from .multihead import MultiHeadAttention


class CommonTransformerUnit(nn.Module):
    """CommonTransformerUnit."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()
        embedding_dim = ctx.config.embedding_dim
        expansion_factor = ctx.config.expansion_factor

        self.attention = MultiHeadAttention(ctx)

        self.layer_normalization1 = nn.LayerNorm(embedding_dim)
        self.layer_normalization2 = nn.LayerNorm(embedding_dim)

        self.ffl = nn.Sequential(
            nn.Linear(embedding_dim, expansion_factor * embedding_dim),
            nn.ReLU(),
            nn.Linear(expansion_factor * embedding_dim, embedding_dim),
        )

        self.dropout1 = nn.Dropout(0.2)
        self.dropout2 = nn.Dropout(0.2)

    def forward(self, key, query, value):

        attention_out = self.attention(key, query, value)
        attention_residual_out = attention_out + value
        norm1_out = self.dropout1(self.layer_normalization1(attention_residual_out))

        ffl = self.ffl(norm1_out)
        ffl_residual = ffl + norm1_out
        return self.dropout2(self.layer_normalization2(ffl_residual))
