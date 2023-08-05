"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.3.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from delphix.api.gateway.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from delphix.api.gateway.exceptions import ApiAttributeError



class DSourceSnapshotParameters(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('sync_strategy',): {
            'LATEST_BACKUP': "latest_backup",
            'NEW_BACKUP': "new_backup",
            'SPECIFIC_BACKUP': "specific_backup",
        },
        ('availability_group_backup_policy',): {
            'PRIMARY': "primary",
            'SECONDARY_ONLY': "secondary_only",
            'PREFER_SECONDARY': "prefer_secondary",
        },
    }

    validations = {
        ('mssql_backup_uuid',): {
            'max_length': 4096,
            'min_length': 1,
        },
        ('files_for_partial_full_backup',): {
            'max_items': 10000,
            'min_items': 1,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'drop_and_recreate_devices': (bool,),  # noqa: E501
            'sync_strategy': (str,),  # noqa: E501
            'ase_backup_files': ([str],),  # noqa: E501
            'mssql_backup_uuid': (str,),  # noqa: E501
            'compression_enabled': (bool,),  # noqa: E501
            'availability_group_backup_policy': (str,),  # noqa: E501
            'do_not_resume': (bool,),  # noqa: E501
            'double_sync': (bool,),  # noqa: E501
            'force_full_backup': (bool,),  # noqa: E501
            'skip_space_check': (bool,),  # noqa: E501
            'files_for_partial_full_backup': ([int],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'drop_and_recreate_devices': 'drop_and_recreate_devices',  # noqa: E501
        'sync_strategy': 'sync_strategy',  # noqa: E501
        'ase_backup_files': 'ase_backup_files',  # noqa: E501
        'mssql_backup_uuid': 'mssql_backup_uuid',  # noqa: E501
        'compression_enabled': 'compression_enabled',  # noqa: E501
        'availability_group_backup_policy': 'availability_group_backup_policy',  # noqa: E501
        'do_not_resume': 'do_not_resume',  # noqa: E501
        'double_sync': 'double_sync',  # noqa: E501
        'force_full_backup': 'force_full_backup',  # noqa: E501
        'skip_space_check': 'skip_space_check',  # noqa: E501
        'files_for_partial_full_backup': 'files_for_partial_full_backup',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """DSourceSnapshotParameters - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            drop_and_recreate_devices (bool): If this parameter is set to true, older devices will be dropped and new devices created instead of trying to remap the devices. This might increase the space utilization on Delphix Engine. (ASE only) . [optional]  # noqa: E501
            sync_strategy (str): Determines how the Delphix Engine will take a backup: * `latest_backup` - Use the most recent backup. * `new_backup` - Delphix will take a new backup of your source database. * `specific_backup` - Use a specific backup. Using this option requires setting   `ase_backup_files` for ASE dSources or `mssql_backup_uuid` for MSSql dSources. Default is `new_backup`. (ASE, MSSql only) . [optional]  # noqa: E501
            ase_backup_files ([str]): When using the `specific_backup` sync_strategy, determines the backup files. (ASE Only). [optional]  # noqa: E501
            mssql_backup_uuid (str): When using the `specific_backup` sync_strategy, determines the Backup Set UUID. (MSSql only). [optional]  # noqa: E501
            compression_enabled (bool): When using the `new_backup` sync_strategy, determines if compression must be enabled. Defaults to the configuration of the ingestion strategy configured on the Delphix Engine for this dSource. (MSSql only). [optional]  # noqa: E501
            availability_group_backup_policy (str): When using the `new_backup` sync_strategy for an MSSql Availability Group, determines the backup policy: * `primary` - Backups only go to the primary node. * `secondary_only` - Backups only go to secondary nodes. If secondary nodes are down, backups will fail. * `prefer_secondary` - Backups go to secondary nodes, but if secondary nodes are down, backups will go to the primary node. (MSSql only) . [optional]  # noqa: E501
            do_not_resume (bool): Indicates whether a fresh SnapSync must be started regardless if it was possible to resume the current SnapSync. If true, we will not resume but instead ignore previous progress and backup all datafiles even if already completed from previous failed SnapSync. This does not force a full backup, if an incremental was in progress this will start a new incremental snapshot. (Oracle only) . [optional]  # noqa: E501
            double_sync (bool): Indicates whether two SnapSyncs should be performed in immediate succession to reduce the number of logs required to provision the snapshot. This may significantly reduce the time necessary to provision from a snapshot. (Oracle only). . [optional]  # noqa: E501
            force_full_backup (bool): Whether or not to take another full backup of the source database. (Oracle only). [optional]  # noqa: E501
            skip_space_check (bool): Skip check that tests if there is enough space available to store the database in the Delphix Engine. The Delphix Engine estimates how much space a database will occupy after compression and prevents SnapSync if insufficient space is available. This safeguard can be overridden using this option. This may be useful when linking highly compressible databases. (Oracle only) . [optional]  # noqa: E501
            files_for_partial_full_backup ([int]): List of datafiles to take a full backup of. This would be useful in situations where certain datafiles could not be backed up during previous SnapSync due to corruption or because they went offline. (Oracle only) . [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """DSourceSnapshotParameters - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            drop_and_recreate_devices (bool): If this parameter is set to true, older devices will be dropped and new devices created instead of trying to remap the devices. This might increase the space utilization on Delphix Engine. (ASE only) . [optional]  # noqa: E501
            sync_strategy (str): Determines how the Delphix Engine will take a backup: * `latest_backup` - Use the most recent backup. * `new_backup` - Delphix will take a new backup of your source database. * `specific_backup` - Use a specific backup. Using this option requires setting   `ase_backup_files` for ASE dSources or `mssql_backup_uuid` for MSSql dSources. Default is `new_backup`. (ASE, MSSql only) . [optional]  # noqa: E501
            ase_backup_files ([str]): When using the `specific_backup` sync_strategy, determines the backup files. (ASE Only). [optional]  # noqa: E501
            mssql_backup_uuid (str): When using the `specific_backup` sync_strategy, determines the Backup Set UUID. (MSSql only). [optional]  # noqa: E501
            compression_enabled (bool): When using the `new_backup` sync_strategy, determines if compression must be enabled. Defaults to the configuration of the ingestion strategy configured on the Delphix Engine for this dSource. (MSSql only). [optional]  # noqa: E501
            availability_group_backup_policy (str): When using the `new_backup` sync_strategy for an MSSql Availability Group, determines the backup policy: * `primary` - Backups only go to the primary node. * `secondary_only` - Backups only go to secondary nodes. If secondary nodes are down, backups will fail. * `prefer_secondary` - Backups go to secondary nodes, but if secondary nodes are down, backups will go to the primary node. (MSSql only) . [optional]  # noqa: E501
            do_not_resume (bool): Indicates whether a fresh SnapSync must be started regardless if it was possible to resume the current SnapSync. If true, we will not resume but instead ignore previous progress and backup all datafiles even if already completed from previous failed SnapSync. This does not force a full backup, if an incremental was in progress this will start a new incremental snapshot. (Oracle only) . [optional]  # noqa: E501
            double_sync (bool): Indicates whether two SnapSyncs should be performed in immediate succession to reduce the number of logs required to provision the snapshot. This may significantly reduce the time necessary to provision from a snapshot. (Oracle only). . [optional]  # noqa: E501
            force_full_backup (bool): Whether or not to take another full backup of the source database. (Oracle only). [optional]  # noqa: E501
            skip_space_check (bool): Skip check that tests if there is enough space available to store the database in the Delphix Engine. The Delphix Engine estimates how much space a database will occupy after compression and prevents SnapSync if insufficient space is available. This safeguard can be overridden using this option. This may be useful when linking highly compressible databases. (Oracle only) . [optional]  # noqa: E501
            files_for_partial_full_backup ([int]): List of datafiles to take a full backup of. This would be useful in situations where certain datafiles could not be backed up during previous SnapSync due to corruption or because they went offline. (Oracle only) . [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
