# coding=utf-8
import random
from otlmow_model.BaseClasses.KeuzelijstField import KeuzelijstField
from otlmow_model.BaseClasses.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlCameraModelnaam(KeuzelijstField):
    """De modelnaam van de camera."""
    naam = 'KlCameraModelnaam'
    label = 'Camera modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlCameraModelnaam'
    definition = 'De modelnaam van de camera.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlCameraModelnaam'
    options = {
        'dinion-ip-starlight-8000-m': KeuzelijstWaarde(invulwaarde='dinion-ip-starlight-8000-m',
                                                       label='Dinion IP Starlight 8000 M',
                                                       status='ingebruik',
                                                       definitie='Dinion IP Starlight 8000 M',
                                                       objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlCameraModelnaam/dinion-ip-starlight-8000-m'),
        'mic-ip-7100i': KeuzelijstWaarde(invulwaarde='mic-ip-7100i',
                                         label='MIC IP 7100i',
                                         status='ingebruik',
                                         definitie='MIC IP 7100i',
                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlCameraModelnaam/mic-ip-7100i'),
        'ulisse-hd': KeuzelijstWaarde(invulwaarde='ulisse-hd',
                                      label='Ulisse HD',
                                      status='ingebruik',
                                      definitie='Ulisse HD',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlCameraModelnaam/ulisse-hd')
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

