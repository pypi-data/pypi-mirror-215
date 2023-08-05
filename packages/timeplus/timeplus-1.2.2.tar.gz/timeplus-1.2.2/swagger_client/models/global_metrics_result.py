# coding: utf-8

"""
    Timeplus

    Welcome to the Timeplus HTTP REST API specification.  # noqa: E501

    OpenAPI spec version: v1
    Contact: support@timeplus.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class GlobalMetricsResult(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'sink_throughput': 'float',
        'source_throughput': 'float',
        'storage': 'int'
    }

    attribute_map = {
        'sink_throughput': 'sink_throughput',
        'source_throughput': 'source_throughput',
        'storage': 'storage'
    }

    def __init__(self, sink_throughput=None, source_throughput=None, storage=None):  # noqa: E501
        """GlobalMetricsResult - a model defined in Swagger"""  # noqa: E501
        self._sink_throughput = None
        self._source_throughput = None
        self._storage = None
        self.discriminator = None
        self.sink_throughput = sink_throughput
        self.source_throughput = source_throughput
        self.storage = storage

    @property
    def sink_throughput(self):
        """Gets the sink_throughput of this GlobalMetricsResult.  # noqa: E501


        :return: The sink_throughput of this GlobalMetricsResult.  # noqa: E501
        :rtype: float
        """
        return self._sink_throughput

    @sink_throughput.setter
    def sink_throughput(self, sink_throughput):
        """Sets the sink_throughput of this GlobalMetricsResult.


        :param sink_throughput: The sink_throughput of this GlobalMetricsResult.  # noqa: E501
        :type: float
        """
        if sink_throughput is None:
            raise ValueError("Invalid value for `sink_throughput`, must not be `None`")  # noqa: E501

        self._sink_throughput = sink_throughput

    @property
    def source_throughput(self):
        """Gets the source_throughput of this GlobalMetricsResult.  # noqa: E501


        :return: The source_throughput of this GlobalMetricsResult.  # noqa: E501
        :rtype: float
        """
        return self._source_throughput

    @source_throughput.setter
    def source_throughput(self, source_throughput):
        """Sets the source_throughput of this GlobalMetricsResult.


        :param source_throughput: The source_throughput of this GlobalMetricsResult.  # noqa: E501
        :type: float
        """
        if source_throughput is None:
            raise ValueError("Invalid value for `source_throughput`, must not be `None`")  # noqa: E501

        self._source_throughput = source_throughput

    @property
    def storage(self):
        """Gets the storage of this GlobalMetricsResult.  # noqa: E501


        :return: The storage of this GlobalMetricsResult.  # noqa: E501
        :rtype: int
        """
        return self._storage

    @storage.setter
    def storage(self, storage):
        """Sets the storage of this GlobalMetricsResult.


        :param storage: The storage of this GlobalMetricsResult.  # noqa: E501
        :type: int
        """
        if storage is None:
            raise ValueError("Invalid value for `storage`, must not be `None`")  # noqa: E501

        self._storage = storage

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GlobalMetricsResult, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GlobalMetricsResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
