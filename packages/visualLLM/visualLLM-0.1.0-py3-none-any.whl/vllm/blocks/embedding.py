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

"""
This is a embedding layer for the transformer model.
"""
import math

import torch
import torch.nn as nn


class PositionalEmbeddings(nn.Module):
    """PositionalEmbeddings."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: a context object which holds configuration and general context around
                 the application.
        """

        super().__init__()
        self.embedding_dim = ctx.config.embedding_dim

        pe = torch.zeros(ctx.config.sequence_length, self.embedding_dim)
        for pos in range(ctx.config.sequence_length):
            for i in range(0, self.embedding_dim, 2):
                pe[pos, i] = math.sin(pos / (10000 ** ((2 * i) / self.embedding_dim)))
                pe[pos, i + 1] = math.cos(
                    pos / (10000 ** ((2 * (i + 1)) / self.embedding_dim))
                )
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x * math.sqrt(self.embedding_dim)
        seq_len = x.size(1)
        x = x + torch.autograd.Variable(self.pe[:, :seq_len], requires_grad=False)
        return x
