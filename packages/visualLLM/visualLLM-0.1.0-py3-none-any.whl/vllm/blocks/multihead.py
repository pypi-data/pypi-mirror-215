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
This is a multi-head layer of self attention as per `Attention is all your need paper`
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiHeadAttention(nn.Module):
    """MultiHeadAttention."""

    def __init__(self, ctx):
        """__init__.

        Args:
            ctx: A context object which holds configuration
                 and other context arount the execution
        """
        super().__init__()
        self.ctx = ctx
        embedding_dim = ctx.config.embedding_dim
        num_heads = ctx.config.num_heads

        single_head_dims = int(embedding_dim / num_heads)

        self.query_weights = nn.Linear(single_head_dims, single_head_dims, bias=False)
        self.key_weights = nn.Linear(single_head_dims, single_head_dims, bias=False)
        self.value_weights = nn.Linear(single_head_dims, single_head_dims, bias=False)

        self.ffl = nn.Linear(single_head_dims * num_heads, embedding_dim)
        self.num_heads = num_heads
        self.single_head_dims = single_head_dims

    def _attention_matrix_transpose(
        self, K, Q, V, batch_size, sequence_length=0, query_sequence_length=None
    ):
        """_attention_matrix_transpose.

        Args:
            K: Key
            Q: Query
            V: Value
            batch_size: batch size
            sequence_length: sequence length
            query_sequence_length: query sequence length
        """
        if query_sequence_length is None:
            query_sequence_length = sequence_length

        K = K.view(batch_size, sequence_length, self.num_heads, self.single_head_dims)
        Q = Q.view(
            batch_size, query_sequence_length, self.num_heads, self.single_head_dims
        )
        V = V.view(K.shape)
        return K, Q, V

    def forward(self, query, key, value):
        # x shape -> B, S, E
        # B: Batch
        # S: Sequence Length
        # E: Embedding Dimension

        # transpose x for query multiplication
        batch_size, sequence_length, embedding_dim = query.shape

        # Query and Key transpose
        # BxSxE -> BxSxnum_headsxsingle_head_dims

        key, query, value = self._attention_matrix_transpose(
            key, query, value, batch_size, sequence_length=sequence_length
        )

        query = self.query_weights(query)
        key = self.key_weights(key)
        value = self.value_weights(value)

        # (Bxsingle_head_dimsxSxnum_heads) x (Bxsingle_head_dimsxnum_headsxS)
        # (Bxsingle_head_dimsxSxS)
        transposed_query = query.view(
            batch_size, self.num_heads, sequence_length, self.single_head_dims
        )
        transposed_key = key.view(
            batch_size, self.num_heads, self.single_head_dims, sequence_length
        )

        # QxK
        intermediate_attention = torch.matmul(transposed_query, transposed_key)

        # divide with sqrt of dimension

        intermediate_attention = intermediate_attention / math.sqrt(
            self.single_head_dims
        )

        scores = F.softmax(intermediate_attention, dim=-1)

        # multiply with value weights

        attention = torch.matmul(
            scores,
            value.view(
                batch_size, self.num_heads, sequence_length, self.single_head_dims
            ),
        )

        attention = self.ffl(attention.view(batch_size, sequence_length, embedding_dim))

        return attention


class MaskedMultiHeadAttention(MultiHeadAttention):
    def __init__(self, ctx):
        super().__init__(ctx)

    def forward(self, query, key, value, mask):
        # x shape -> B, S, E
        # B: Batch
        # S: Sequence Length
        # E: Embedding Dimension

        # transpose x for query multiplication
        batch_size, sequence_length, embedding_dim = key.shape

        # Query and Key transpose
        # BxSxE -> BxSxnum_headsxsingle_head_dims

        key, query, value = self._attention_matrix_transpose(
            key, query, value, batch_size, sequence_length=sequence_length
        )

        query = self.query_weights(query)
        key = self.key_weights(key)
        value = self.value_weights(value)

        # (Bxsingle_head_dimsxSxnum_heads) x (Bxsingle_head_dimsxnum_headsxS)
        # (Bxsingle_head_dimsxSxS)
        transposed_query = query.view(
            batch_size, self.num_heads, sequence_length, self.single_head_dims
        )
        transposed_key = key.view(
            batch_size, self.num_heads, self.single_head_dims, sequence_length
        )

        # QxK
        intermediate_attention = torch.matmul(transposed_query, transposed_key)

        # mask it with lookahead masking
        intermediate_attention = intermediate_attention.masked_fill(
            mask == 0, float("-1e20")
        )

        # divide with sqrt of dimension

        intermediate_attention = intermediate_attention / math.sqrt(
            self.single_head_dims
        )

        scores = F.softmax(intermediate_attention, dim=-1)

        # multiply with value weights

        attention = torch.matmul(
            scores,
            value.view(
                batch_size, self.num_heads, sequence_length, self.single_head_dims
            ),
        )

        attention = self.ffl(attention.view(batch_size, sequence_length, embedding_dim))

        return attention
