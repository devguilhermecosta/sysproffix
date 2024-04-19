from django.core.exceptions import ValidationError


def required_field(data: str | int | float,
                   message: str = 'campo obrigatório',
                   code: str = 'required',
                   ) -> str | int | float:
    """
        Creates an instance of ValidationError if the field is empty.
    """
    if not data:
        raise ValidationError(
            message,
            code=code,
        )

    return data
