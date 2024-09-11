from utils.validate import validate_parameters_with_weights


def weighted_sum_model(parameters, weights):
    """
    Calculate the weighted sum of input parameters.

    The function multiplies each parameter by its corresponding weight and sums the results.

    :param parameters: Dictionary containing input parameters as keys and their values as floats.
    :param weights: Dictionary containing input parameters as keys and their corresponding weights as floats.
    :return: The weighted sum as a float.
    :raises ValueError: If any parameter in `parameters` is not in `weights`, or if `weights` is missing for any parameter in `parameters`.
    """
    validate_parameters_with_weights(parameters, weights)

    weighted_sum = sum(parameters[param] * weights[param] for param in parameters)
    return weighted_sum


def weighted_average_model(parameters, weights):
    """
    Calculate the weighted average of input parameters.

    The function multiplies each parameter by its corresponding weight, sums the results, and divides by the sum of the weights.

    :param parameters: Dictionary containing input parameters as keys and their values as floats.
    :param weights: Dictionary containing input parameters as keys and their corresponding weights as floats.
    :return: The weighted average as a float.
    :raises ValueError: If any parameter in `parameters` is not in `weights`, or if `weights` is missing for any parameter in `parameters`.
    :raises ValueError: If the sum of weights is zero, to prevent division by zero.
    """
    validate_parameters_with_weights(parameters, weights)

    # Calculate the weighted sum and sum of the weights
    weighted_sum = sum(parameters[param] * weights[param] for param in parameters)
    sum_of_weights = sum(weights.values())

    # Prevent division by zero
    if sum_of_weights == 0:
        raise ValueError("Sum of weights must not be zero")

    # Calculate and return the weighted average
    return weighted_sum / sum_of_weights
