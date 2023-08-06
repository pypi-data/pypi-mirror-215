from types import SimpleNamespace
import pprint

def convert_namespace_to_dict(namespace: SimpleNamespace) -> SimpleNamespace:
    if isinstance(namespace, SimpleNamespace):
        namespace_dict = vars(namespace)
        
        for key, value in namespace_dict.items():
            if isinstance(value, SimpleNamespace):
                namespace_dict[key] = convert_namespace_to_dict(value)
            elif isinstance(value, list):
                namespace_dict[key] = [convert_namespace_to_dict(item) if isinstance(item, SimpleNamespace) else item for item in value]

        return namespace_dict
    else:
        return namespace

class DividoSimpleNamespace(SimpleNamespace):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)

    def as_dict(self) -> dict:
        return convert_namespace_to_dict(self)
    
    def get_attribute_or_none(self, attribute: str) -> any:
        """Returns the value for an attribute or None if there is no attribute, using dot syntax, e.g. 'data.parent.child' 

        Args:
            attribute (str): The attribute to return 

        Returns:
            any: The attribute value, or None if no such attribute can be found
        """        
        copy = self
        for layer in attribute.split('.'):
            if hasattr(copy, layer):
                copy = getattr(copy, layer)
            else:
                return None
        return copy

    def _find_missing_attributes(self, attributes: list) -> list:
        return [attribute for attribute in attributes if self.get_attribute_or_none(attribute=attribute) == None]

    def _verify_attributes_list(self, attributes: list, error_preface: str):
        missing_attributes = self._find_missing_attributes(attributes=attributes)
        missing_attributes_string = ", ".join([f'"{attribute}"' for attribute in missing_attributes])

        assert not missing_attributes, f'{error_preface}: {missing_attributes_string}.\nFull data as JSON:\n {pprint.pformat(self.as_dict(), sort_dicts=False)}'
        return self 
    
    def verify_attributes(self, attributes: any, error_preface = None):
        """Assert that each of the provided attributes exists

        Args:
            attributes (any): One or more attributes to check for 
            error_preface (_type_, optional): Optional error preface override to provide additional context in case of error. Defaults to None.

        Raises:
            NotImplementedError: This function only supports list or list parsable arguments

        Returns:
            _type_: The object that is being checked 
        """        
        error_preface = error_preface or 'DividoSimpleNamespace was missing the following attributes'
        
        if isinstance(attributes, list):
            return self._verify_attributes_list(attributes, error_preface)
        elif isinstance(attributes, str):
            return self._verify_attributes_list([attributes], error_preface)
        raise NotImplementedError(f'"DividoSimpleNamespace.verify_attributes" function is not implemented for attributes of type "{type(attributes).__name__}"')
    