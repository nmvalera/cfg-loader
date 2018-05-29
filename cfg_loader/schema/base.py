"""
    cfg_loader.schema.base
    ~~~~~~~~~~~~~~~~~~~~~~

    Implement base marshmallow schema to deserialize configuration data

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import marshmallow
from marshmallow import Schema, post_load

from ..exceptions import ValidationError
from ..fields import UnwrapNested
from ..interpolator import SubstitutionTemplate, Interpolator
from ..utils import add_prefix


class InterpolatingSchema(Schema):
    """Schema class that interpolate environ variables from input data

    It implements environment variable substitution following specification from docker-compose
    (c.f. https://docs.docker.com/compose/compose-file/#variable-substitution)

    :param substitution_mapping: Mapping containing values to substitute
    :type substitution: dict
    """

    _interpolator_class = Interpolator
    _substitution_template = SubstitutionTemplate

    def __init__(self, *args, substitution_mapping=None, **kwargs):
        self.substitution_mapping = substitution_mapping or {}
        self.interpolator = self._interpolator_class(substitution_mapping=self.substitution_mapping,
                                                     substitution_template=self._substitution_template)
        super().__init__(*args, **kwargs)

    def load(self, data, many=None, partial=None):
        """Deserialize a data structure to an object defined by this Schema’s fields

        :param data: Data object to load from
        :type data: dict
        :param many: Whether to deserialize ``data`` as a collection
        :type many: bool
        :param partial: whether to ignore missing fields
        :type partial: bool | tuple
        :returns: Deserialized data
        :type return: dict
        """
        if self.substitution_mapping:
            # substitute environment variables
            data = self.interpolator.interpolate_recursive(data)

        try:
            return super().load(data, many, partial)
        except marshmallow.exceptions.ValidationError as e:
            raise ValidationError(e.normalized_messages())


class ExtraFieldsSchema(Schema):
    """Schema class that preserves fields provided in input data but that were omitted in schema fields"""

    @post_load(pass_original=True)
    def add_extra_fields(self, data, original_data):
        """Add field from input data that were not listed as a schema fields

        :param data: Data to complete
        :type data: dict
        :param extra_data: Extra data to insert
        :type extra_data: dict
        """
        extra_fields = set(original_data) - set(self.fields)
        for field in extra_fields:
            data[field] = original_data[field]

        return data


class UnwrapNestedSchema(Schema):
    """Schema class that can unwrap nested fields"""

    @post_load
    def unwrap_nested_fields(self, data):
        unwrap_nested = {}
        for field, value in self.fields.items():
            if isinstance(value, UnwrapNested):
                unwrap_nested.update(add_prefix(data.pop(field), value.prefix))
        data.update(unwrap_nested)

        return data


class ConfigSchema(InterpolatingSchema, ExtraFieldsSchema, UnwrapNestedSchema):
    """Main schema class for declaring a configuration schema

    It inherits every feature from

    - :class:`InterpolatingSchema`
    - :class:`ExtraFieldsSchema`
    - :class:`UnwrapNestedSchema`

    Example

    >>> from cfg_loader import ConfigSchema, BaseConfigLoader
    >>> from marshmallow import fields

    >>> class MyConfigSchema(ConfigSchema):
    ...     setting1 = fields.Str()
    ...     setting2 = fields.Int(required=True)
    ...     setting3 = fields.Float(missing=13.2)

    >>> substitution_mapping = {'VARIABLE': 'substitution'}
    >>> my_config_loader = BaseConfigLoader(MyConfigSchema,
    ...                                     substitution_mapping)

    >>> schema = MyConfigSchema(substitution_mapping=substitution_mapping)
    >>> config = schema.load({
    ...    'setting1': '${VARIABLE}',
    ...    'setting2': '${UNSET_VARIABLE:-1}',
    ... })

    >>> config == {
    ...     'setting1': 'substitution',
    ...     'setting2': 1,
    ...     'setting3': 13.2,
    ... }
    True
    """
