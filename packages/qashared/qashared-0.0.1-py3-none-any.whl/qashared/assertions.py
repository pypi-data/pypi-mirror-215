from deepdiff import DeepDiff
from qashared.helpers import * 

def assert_are_equivalent(actual: DividoSimpleNamespace, expected: DividoSimpleNamespace, exclude_paths=[]) -> None:
    """Assert that two objects have deep equivalency, i.e. they share the same attributes and corresponding values

    Args:
        actual (DividoSimpleNamespace): The actual object involved in the comparison
        expected (DividoSimpleNamespace): The expected object involved in the comparison
        exclude_paths (list, optional): A list of attribute paths using dot notation to exclude when making the comparison. Defaults to [].
    """    
    differences = DeepDiff(actual, expected, exclude_paths=[f'root.{path}' for path in exclude_paths])

    values_changed_errors = [f'Attribute "{key.replace("root.", "")}" had value "{val["new_value"]}", expecting "{val["old_value"]}"' for key, val in differences.get('values_changed', {}).items()]
    attributes_added_errors = [f'Attribute was missing: "{attribute.replace("root.", "")}"' for attribute in differences.get('attribute_added', [])]
    attributes_removed_errors = [f'Unexpected attribute was present: "{attribute.replace("root.", "")}"' for attribute in differences.get('attribute_removed', [])]

    errors_string = '\n❌ '.join(values_changed_errors + attributes_added_errors + attributes_removed_errors)
    assert not differences, f'"{get_variable_name(actual)}" was different to the expected "{get_variable_name(expected)}":\n❌ {errors_string}'

def assert_matching_attributes(actual: DividoSimpleNamespace, expected: DividoSimpleNamespace, include_paths: list) -> None:
    """Assert that two objects have the same values for a given list of attributes 

    Args:
        actual (DividoSimpleNamespace): The actual object involved in the comparison
        expected (DividoSimpleNamespace): The expected object involved in the comparison
        include_paths (list): A list of attribute paths using dot notation to include when making the comparison
    """    
    errors = []

    for attribute in include_paths:
        actual_value, expected_value = actual.get_attribute_or_none(attribute), expected.get_attribute_or_none(attribute)

        if actual_value is None:
            errors.append(f'"{get_variable_name(actual)}" did not have attribute "{attribute}"')
        if expected_value is None:
            errors.append(f'"{get_variable_name(expected)}" did not have attribute "{attribute}"')
        if (not actual_value is None and not expected_value is None) and actual_value != expected_value:
            errors.append(f'Attribute "{attribute}" had value "{actual_value}", expected "{expected_value}"')

    errors_string = '\n❌ '.join(errors)
    assert not errors, f'"{get_variable_name(actual)}" had attributes that did not match the expected "{get_variable_name(expected)}":\n❌ {errors_string}'
