from app_types import GenderEnum, SpeciesEnum, StatusEnum

def convert_age_to_display(age_months: float) -> str:
    """
    Converte idade em meses para formato de exibição
    """
    if age_months < 12:
        return f"{int(age_months)} meses"
    else:
        years = int(age_months // 12)
        remaining_months = int(age_months % 12)
        if remaining_months == 0:
            return f"{years} ano{'s' if years > 1 else ''}"
        else:
            return f"{years} ano{'s' if years > 1 else ''} e {remaining_months} meses"

def get_pet_type_display(species: SpeciesEnum) -> str:
    """
    Retorna o tipo do pet em português
    """
    return {
        SpeciesEnum.DOG: "Cachorro",
        SpeciesEnum.CAT: "Gato"
    }.get(species, species.value)

def get_gender_display(gender: GenderEnum) -> str:
    """
    Retorna o gênero em português
    """
    return {
        GenderEnum.MALE: "Macho",
        GenderEnum.FEMALE: "Fêmea"
    }.get(gender, gender.value)

def get_species_label(species: SpeciesEnum) -> str:
    """
    Retorna o label da espécie em português
    """
    return {
        SpeciesEnum.DOG: "Cachorro",
        SpeciesEnum.CAT: "Gato"
    }.get(species, species.value)

def get_gender_label(gender: GenderEnum) -> str:
    """
    Retorna o label do gênero em português
    """
    return {
        GenderEnum.MALE: "Macho",
        GenderEnum.FEMALE: "Fêmea"
    }.get(gender, gender.value)

def get_status_label(status) -> str:
    """
    Retorna o label do status em português
    """
    return {
        StatusEnum.AVAILABLE: "Disponível",
        StatusEnum.ADOPTED: "Adotado",
        StatusEnum.PENDING: "Pendente"
    }.get(status, str(status))
