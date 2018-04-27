"""
    config_loader.schema.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement base marshmallow schema to deserialize configuration data

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from config_loader.interpolator import SubstitutionTemplate, Interpolator
from marshmallow import Schema, post_load


class InterpolatingSchema(Schema):
    """Base schema class that interpolate environ variables in input data

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
        if self.substitution_mapping:
            # substitute environment variables
            data = self.interpolator.interpolate_recursive(data)

        return super().load(data, many, partial)


class ExtraFieldsSchema(Schema):
    """Base schema class that preserves fields in input data that were listed as a schema fields"""

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


class ConfigSchema(InterpolatingSchema, ExtraFieldsSchema):
    """Base configuration schema"""
