from hospital.models import Hospital


def create_hospital(name: str = 'Hospital') -> Hospital:
    """
        Create a new instance of Hospital model.
    """
    new_hospital = Hospital.objects.create(name=name)
    new_hospital.save()

    return new_hospital
