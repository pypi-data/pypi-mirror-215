# coding: utf-8

"""
    FINBOURNE Insights API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.681
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_insights.configuration import Configuration


class VendorRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'id': 'str',
        'request': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'request': 'request',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'request': 'required',
        'links': 'optional'
    }

    def __init__(self, id=None, request=None, links=None, local_vars_configuration=None):  # noqa: E501
        """VendorRequest - a model defined in OpenAPI"
        
        :param id:  The ID of the log. (required)
        :type id: str
        :param request:  The body of the request. (required)
        :type request: str
        :param links: 
        :type links: list[finbourne_insights.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._request = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.request = request
        self.links = links

    @property
    def id(self):
        """Gets the id of this VendorRequest.  # noqa: E501

        The ID of the log.  # noqa: E501

        :return: The id of this VendorRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this VendorRequest.

        The ID of the log.  # noqa: E501

        :param id: The id of this VendorRequest.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and len(id) < 1):
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def request(self):
        """Gets the request of this VendorRequest.  # noqa: E501

        The body of the request.  # noqa: E501

        :return: The request of this VendorRequest.  # noqa: E501
        :rtype: str
        """
        return self._request

    @request.setter
    def request(self, request):
        """Sets the request of this VendorRequest.

        The body of the request.  # noqa: E501

        :param request: The request of this VendorRequest.  # noqa: E501
        :type request: str
        """
        if self.local_vars_configuration.client_side_validation and request is None:  # noqa: E501
            raise ValueError("Invalid value for `request`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                request is not None and len(request) < 1):
            raise ValueError("Invalid value for `request`, length must be greater than or equal to `1`")  # noqa: E501

        self._request = request

    @property
    def links(self):
        """Gets the links of this VendorRequest.  # noqa: E501


        :return: The links of this VendorRequest.  # noqa: E501
        :rtype: list[finbourne_insights.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this VendorRequest.


        :param links: The links of this VendorRequest.  # noqa: E501
        :type links: list[finbourne_insights.Link]
        """

        self._links = links

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, VendorRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VendorRequest):
            return True

        return self.to_dict() != other.to_dict()
