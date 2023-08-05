# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class PatientRelationshipToInsuredCodeAll(str, enum.Enum):
    SPOUSE = "01"
    GRANDPARENT = "04"
    GRANDCHILD = "05"
    NIECE_NEPHEW = "07"
    FOSTER_CHILD = "10"
    WARD_OF_THE_COURT = "15"
    STEPCHILD = "17"
    SELF = "18"
    CHILD = "19"
    EMPLOYEE = "20"
    UNKNOWN = "21"
    HANDICAPPED_DEPENDENT = "22"
    SPONSORED_DEPENDENT = "23"
    DEPENDENT_OF_MINOR_DEPENDENT = "24"
    SIGNIFICANT_OTHER = "29"
    MOTHER = "32"
    FATHER = "33"
    EMANCIPATED_MINOR = "36"
    ORGAN_DONOR = "39"
    CADAVER_DONOR = "40"
    INJURED_PLAINTIFF = "41"
    CHILD_NO_FINANCIAL_RESPONSIBILITY = "43"
    LIFE_PARTNER = "53"
    OTHER_RELATIONSHIP = "G8"

    def visit(
        self,
        spouse: typing.Callable[[], T_Result],
        grandparent: typing.Callable[[], T_Result],
        grandchild: typing.Callable[[], T_Result],
        niece_nephew: typing.Callable[[], T_Result],
        foster_child: typing.Callable[[], T_Result],
        ward_of_the_court: typing.Callable[[], T_Result],
        stepchild: typing.Callable[[], T_Result],
        self_: typing.Callable[[], T_Result],
        child: typing.Callable[[], T_Result],
        employee: typing.Callable[[], T_Result],
        unknown: typing.Callable[[], T_Result],
        handicapped_dependent: typing.Callable[[], T_Result],
        sponsored_dependent: typing.Callable[[], T_Result],
        dependent_of_minor_dependent: typing.Callable[[], T_Result],
        significant_other: typing.Callable[[], T_Result],
        mother: typing.Callable[[], T_Result],
        father: typing.Callable[[], T_Result],
        emancipated_minor: typing.Callable[[], T_Result],
        organ_donor: typing.Callable[[], T_Result],
        cadaver_donor: typing.Callable[[], T_Result],
        injured_plaintiff: typing.Callable[[], T_Result],
        child_no_financial_responsibility: typing.Callable[[], T_Result],
        life_partner: typing.Callable[[], T_Result],
        other_relationship: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is PatientRelationshipToInsuredCodeAll.SPOUSE:
            return spouse()
        if self is PatientRelationshipToInsuredCodeAll.GRANDPARENT:
            return grandparent()
        if self is PatientRelationshipToInsuredCodeAll.GRANDCHILD:
            return grandchild()
        if self is PatientRelationshipToInsuredCodeAll.NIECE_NEPHEW:
            return niece_nephew()
        if self is PatientRelationshipToInsuredCodeAll.FOSTER_CHILD:
            return foster_child()
        if self is PatientRelationshipToInsuredCodeAll.WARD_OF_THE_COURT:
            return ward_of_the_court()
        if self is PatientRelationshipToInsuredCodeAll.STEPCHILD:
            return stepchild()
        if self is PatientRelationshipToInsuredCodeAll.SELF:
            return self_()
        if self is PatientRelationshipToInsuredCodeAll.CHILD:
            return child()
        if self is PatientRelationshipToInsuredCodeAll.EMPLOYEE:
            return employee()
        if self is PatientRelationshipToInsuredCodeAll.UNKNOWN:
            return unknown()
        if self is PatientRelationshipToInsuredCodeAll.HANDICAPPED_DEPENDENT:
            return handicapped_dependent()
        if self is PatientRelationshipToInsuredCodeAll.SPONSORED_DEPENDENT:
            return sponsored_dependent()
        if self is PatientRelationshipToInsuredCodeAll.DEPENDENT_OF_MINOR_DEPENDENT:
            return dependent_of_minor_dependent()
        if self is PatientRelationshipToInsuredCodeAll.SIGNIFICANT_OTHER:
            return significant_other()
        if self is PatientRelationshipToInsuredCodeAll.MOTHER:
            return mother()
        if self is PatientRelationshipToInsuredCodeAll.FATHER:
            return father()
        if self is PatientRelationshipToInsuredCodeAll.EMANCIPATED_MINOR:
            return emancipated_minor()
        if self is PatientRelationshipToInsuredCodeAll.ORGAN_DONOR:
            return organ_donor()
        if self is PatientRelationshipToInsuredCodeAll.CADAVER_DONOR:
            return cadaver_donor()
        if self is PatientRelationshipToInsuredCodeAll.INJURED_PLAINTIFF:
            return injured_plaintiff()
        if self is PatientRelationshipToInsuredCodeAll.CHILD_NO_FINANCIAL_RESPONSIBILITY:
            return child_no_financial_responsibility()
        if self is PatientRelationshipToInsuredCodeAll.LIFE_PARTNER:
            return life_partner()
        if self is PatientRelationshipToInsuredCodeAll.OTHER_RELATIONSHIP:
            return other_relationship()
