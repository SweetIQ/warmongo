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

class InvalidSchemaException(Exception):
    ''' Thrown when we have discovered an invalid schema. '''
    pass

class ValidationError(Exception):
    ''' Thrown when a field does not match the schema. '''
    pass

class InvalidReloadException(Exception):
    ''' Thrown when we attempt to call reload() on a model that is not in the
    database. '''
