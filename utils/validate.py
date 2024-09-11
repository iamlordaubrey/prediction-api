def validate_parameters_with_weights(parameters, weights):
    """
    Validate that all parameters have corresponding weights.

    :param parameters: Dictionary containing input parameters. Each key is a parameter name.
    :param weights: Dictionary containing weights for each parameter. Each key should match a parameter name from `parameters`.
    :raises ValueError: If any parameter in `parameters` does not have a corresponding weight in `weights`.
    """
    if not all(param in weights for param in parameters):
        raise ValueError("All parameters must have corresponding weights")
