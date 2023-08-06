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

from pydantic import BaseModel, BaseSettings


class MultiHeadSetting(BaseModel):
    num_heads = 4


class Settings(BaseSettings):
    epochs: int = 2
    log_every: int = 200
    auth_key: str = ""
    embedding_dim: int = 512
    sequence_length: int = 120
    vocab_size: int = 72
    encoder_blocks: int = 4
    expansion_factor: int = 4
    batch_size: int = 8
    num_heads: int = 4

    multi_head_settings: MultiHeadSetting = MultiHeadSetting()

    class Config:
        env_prefix = "llm_"  # defaults to no prefix, i.e. ""
        fields = {"auth_key": {"env": "my_auth_key"}}
