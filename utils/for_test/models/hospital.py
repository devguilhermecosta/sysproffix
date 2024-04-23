from hospital.models import Hospital


def create_hospital(name: str = 'Hospital',
                    city: str = 'São Paulo',
                    state: str = 'SP') -> Hospital:
    """
        Create a new instance of Hospital model.
    """
    new_hospital = Hospital.objects.create(
        name=name,
        city=city,
        state=state,
    )
    new_hospital.save()

    return new_hospital
