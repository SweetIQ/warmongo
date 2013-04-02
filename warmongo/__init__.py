# Copyright 2013 Rob Britton
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

from model import Model as WarmongoModel
from database import connect

import warlock


def model_factory(schema, base_class=WarmongoModel):
    # All models have an _id field
    if not "_id" in schema["properties"]:
        schema["properties"]["_id"] = { "type": "object_id" }

    class Model(base_class):
        _schema = schema

    return warlock.model_factory(schema, Model)
