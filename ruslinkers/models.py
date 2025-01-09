from typing import List, Set

from sqlalchemy import ForeignKey,ForeignKeyConstraint
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# import sqlalchemy as db
# import sqlalchemy_utils as db_utils
# from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

# Database model
class Base(DeclarativeBase):
    pass

# EXAMPLES

# Examples can illustrate units, parameter values of units, and parameter values of forms

examples_to_unit_parametervalues = Table(
    "examples_to_unit_parametervalues",
    Base.metadata,
    Column("example_id", ForeignKey("examples.id"), primary_key=True),
    Column("unit_id", primary_key=True),
    Column("parametervalue_id", primary_key=True),
    ForeignKeyConstraint(
        ["unit_id","parametervalue_id"],
        ["units_to_parametervalues.unit_id", "units_to_parametervalues.parametervalue_id"]
    )
)

examples_to_form_parametervalues = Table(
    "examples_to_form_parametervalues",
    Base.metadata,
    Column("example_id", ForeignKey("examples.id"), primary_key=True),
    Column("form_id", primary_key=True),
    Column("parametervalue_id", primary_key=True),
    ForeignKeyConstraint(
        ["form_id","parametervalue_id"],
        ["forms_to_parametervalues.form_id", "forms_to_parametervalues.parametervalue_id"]
    )
)

examples_to_units = Table(
    "examples_to_units",
    Base.metadata,
    Column("example_id", ForeignKey("examples.id"), primary_key=True),
    Column("unit_id", ForeignKey("units.id"), primary_key=True)
)

examples_to_forms = Table(
    "examples_to_forms",
    Base.metadata,
    Column("example_id", ForeignKey("examples.id"), primary_key=True),
    Column("form_id", ForeignKey("forms.id"), primary_key=True)
)

class Example(Base):
    __tablename__ = 'examples'

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str]

    units: Mapped[List["Unit"]] = relationship(secondary=examples_to_units, back_populates="examples")
    forms: Mapped[List["Form"]] = relationship(secondary=examples_to_forms, back_populates="examples")
    unit_parametervalues: Mapped[List["UnitToParameterValue"]] = relationship(secondary=examples_to_unit_parametervalues, back_populates="examples")
    form_parametervalues: Mapped[List["FormToParameterValue"]] = relationship(secondary=examples_to_form_parametervalues, back_populates="examples")

    def get_related_units(self) -> List["Unit"]:
        return set(self.units + [f.unit for f in self.forms] + [upv.unit for upv in self.unit_parametervalues] + [fpv.form.unit for fpv in self.form_parametervalues])

# SOURCES

# Sources can be related to units and meanings (possibly also examples)

sources_to_units = Table(
    "sources_to_units",
    Base.metadata,
    Column("source_id", ForeignKey("sources.id"), primary_key=True),
    Column("unit_id", ForeignKey("units.id"), primary_key=True)
)

class Source(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(primary_key=True)
    biblio: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)

# SEMANTIC FIELDS

class Semfield(Base):
    __tablename__ = 'semfields'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)

    subfields: Mapped[Set["Subfield"]] = relationship(back_populates="semfield")

class Subfield(Base):
    __tablename__ = 'subfields'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)

    semfield_id: Mapped[int]  = mapped_column(ForeignKey('semfields.id'))
    semfield: Mapped["Semfield"] = relationship(back_populates="subfields")


units_to_semfields = Table(
    "units_to_semfields",
    Base.metadata,
    Column("unit_id", ForeignKey("units.id"), primary_key=True),
    Column("semfield_id", ForeignKey("semfields.id"), primary_key=True)
)

units_to_subfields = Table(
    "units_to_subfields",
    Base.metadata,
    Column("unit_id", ForeignKey("units.id"), primary_key=True),
    Column("subfield_id", ForeignKey("subfields.id"), primary_key=True)
)

# For additional fields associated with specific dictionaries
meanings_to_semfields = Table(
    "meanings_to_semfields",
    Base.metadata,
    Column("meaning_id", ForeignKey("meanings.id"), primary_key=True),
    Column("semfield_id", ForeignKey("semfields.id"), primary_key=True)
)

units_to_subfields = Table(
    "meanings_to_subfields",
    Base.metadata,
    Column("meaning_id", ForeignKey("units.id"), primary_key=True),
    Column("subfield_id", ForeignKey("subfields.id"), primary_key=True)
)

# class UnitToSemfield(Base):
#     __tablename__ = 'units_to_semfields'

#     unit_to_semfield_id: Mapped[int] = mapped_column(primary_key=True)
    
#     semfield_id = db.Column(db.Integer, db.ForeignKey('semfields.semfield_id'), nullable=False)
#     subfield_id = db.Column(db.Integer, db.ForeignKey('subfields.subfield_id')) # Only if there's a subfield

# COMMENTS

class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str]
    hidden: Mapped[bool] = mapped_column(default=True)

    # unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    # unit: Mapped["Unit"] = relationship(back_populates='comments')

comments_to_units = Table(
    "comments_to_units",
    Base.metadata,
    Column("comment_id", ForeignKey("comments.id"), primary_key=True),
    Column("unit_id", ForeignKey("units.id"), primary_key=True)
)

comments_to_unit_parametervalues = Table(
    "comments_to_unit_parametervalues",
    Base.metadata,
    Column("comment_id", ForeignKey("comments.id"), primary_key=True),
    Column("unit_id", primary_key=True),
    Column("parametervalue_id", primary_key=True),
    ForeignKeyConstraint(
        ["unit_id","parametervalue_id"],
        ["units_to_parametervalues.unit_id", "units_to_parametervalues.parametervalue_id"]
    )
)

comments_to_form_parametervalues = Table(
    "comments_to_form_parametervalues",
    Base.metadata,
    Column("comment_id", ForeignKey("comments.id"), primary_key=True),
    Column("form_id", primary_key=True),
    Column("parametervalue_id", primary_key=True),
    ForeignKeyConstraint(
        ["form_id","parametervalue_id"],
        ["forms_to_parametervalues.form_id", "forms_to_parametervalues.parametervalue_id"]
    )
)

# PARAMETERS

class Parameter(Base):
    __tablename__ = "parameters"

    Unit = 1
    Form = 2
    
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default = "INSERT TEXT HERE")

    hidden: Mapped[bool] = mapped_column(default=False)
    singleval: Mapped[bool] = mapped_column(default=True) # If parameter can have only one value
    semantic: Mapped[bool] = mapped_column(default=False) # If semantic, otherwise syntactic
    target: Mapped[str] = mapped_column(CheckConstraint("target = 1 OR target = 2"), default=1) # 1 = Unit, 2 = Form

    values: Mapped[Set["ParameterValue"]] = relationship(back_populates='parameter',
                                                         cascade='all,delete-orphan')

class ParameterValue(Base): # Individual values a parameter can take
    __tablename__ = "parametervalues"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    keyword: Mapped[str]
    description: Mapped[str] = mapped_column(default = "INSERT TEXT HERE")    

    parameter_id: Mapped[int] = mapped_column(ForeignKey("parameters.id"))
    parameter: Mapped["Parameter"] = relationship(back_populates='values')

    __table_args__ = (UniqueConstraint('keyword', 'parameter_id'),
                     ) # Ensure that each parameter value is unique within the scope of one parameter

class TextParameter(Base): # Parameters whose values are free-form text
    __tablename__ = 'textparameters'

    Unit = 1
    Form = 2

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default = "INSERT TEXT HERE")

    hidden: Mapped[bool] = mapped_column(default=False)
    target: Mapped[str] = mapped_column(CheckConstraint("target = 1 OR target = 2"), default=1)

# Parameter mappings

class UnitToParameterValue(Base):
    __tablename__ = 'units_to_parametervalues' # Units are mapped to parameter values

    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'), primary_key=True)
    unit: Mapped["Unit"] = relationship(back_populates="parametervalue_mappings")

    parametervalue_id: Mapped[int] = mapped_column(ForeignKey('parametervalues.id'), primary_key=True)
    parametervalue: Mapped["ParameterValue"] = relationship()
    
    parameter: AssociationProxy["Parameter"] = association_proxy("parametervalue", "parameter")
    # parameter_kw: AssociationProxy["ParameterValue"] = association_proxy("parametervalue", "parameter_kw")

    examples: Mapped[Set["Example"]] = relationship(secondary=examples_to_unit_parametervalues, back_populates="unit_parametervalues")
    comments: Mapped[Set["Comment"]] = relationship(secondary=comments_to_unit_parametervalues)
    # examples = relationship('Example', backref='param') Make a separate linking table

class FormToParameterValue(Base):
    __tablename__ = 'forms_to_parametervalues' # mainly for correlatives, but perhaps also for others

    form_id: Mapped[int] = mapped_column(ForeignKey('forms.id'), primary_key=True)
    form: Mapped["Form"] = relationship(back_populates='parametervalue_mappings')

    parametervalue_id: Mapped[int] = mapped_column(ForeignKey('parametervalues.id'), primary_key=True) # Maybe add constraints that ensure that correct parameters are chosen
    parametervalue: Mapped["ParameterValue"] = relationship()

    parameter: AssociationProxy["Parameter"] = association_proxy("parametervalue", "parameter")

    examples: Mapped[Set["Example"]] = relationship(secondary=examples_to_form_parametervalues, back_populates="form_parametervalues")
    comments: Mapped[Set["Comment"]] = relationship(secondary=comments_to_form_parametervalues)

class UnitToTextParameter(Base):
    __tablename__ = 'units_to_textparametervalues' # For text parameters, you just map parameters to text values

    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'), primary_key=True)
    unit: Mapped["Unit"] = relationship(back_populates="textparametervalues")

    parameter_id: Mapped[int] = mapped_column(ForeignKey('textparameters.id'), primary_key=True)
    parameter: Mapped["TextParameter"] = relationship()

    value: Mapped[str]

class FormToTextParameter(Base):
    __tablename__ = 'forms_to_textparametervalues' # For text parameters, you just map parameters to text values

    form_id: Mapped[int] = mapped_column(ForeignKey('forms.id'), primary_key=True)
    form: Mapped["Form"] = relationship(back_populates="textparametervalues")

    parameter_id: Mapped[int] = mapped_column(ForeignKey('textparameters.id'), primary_key=True)
    parameter: Mapped["TextParameter"] = relationship()

    value: Mapped[str]    

# UNITS

class Unit(Base):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(primary_key=True)
    linker: Mapped[str] # Head word (not treated as Form)

    #internal_id = db.Column(db.Integer)
    status: Mapped[bool] = mapped_column(default=True)  # will be found in dictionary search (1) or not (?)

    # Hardcoded parameters
    style: Mapped[str] = mapped_column(nullable=True)
    sem_comment: Mapped[str] = mapped_column(nullable=True)

    # Connections between units
    links: Mapped[Set["UnitToUnit"]] = relationship(back_populates="source", foreign_keys='UnitToUnit.source_id')

    # Semantic fields
    semfield_id: Mapped[int] = mapped_column(ForeignKey("semfields.id"))
    semfield: Mapped['Semfield'] = relationship()
    extra_semfields: Mapped[Set["Semfield"]] = relationship(secondary=units_to_semfields)
    subfields: Mapped[Set["Subfield"]] = relationship(secondary=units_to_subfields) # Maybe somehow check that subfields belong to the semfields (main and extra)?

    forms: Mapped[Set["Form"]] = relationship(back_populates='unit',cascade='all,delete-orphan')
    meanings: Mapped[Set["Meaning"]] = relationship(back_populates='unit',cascade='all,delete-orphan')
    # log = relationship('Entry_logs', backref='unit', lazy=True)
    # comments = db.relationship('Unit_comments', backref='unit', lazy=True)
    # pictures = db.relationship('Unit_pictures', backref='unit', lazy=True)
    parametervalue_mappings: Mapped[Set["UnitToParameterValue"]] = relationship(back_populates='unit',
                                                                                cascade='all,delete-orphan')
    parametervalues: AssociationProxy[Set["ParameterValue"]] = association_proxy(
        "parametervalue_mappings",
        "parametervalue",
        creator=lambda param: UnitToParameterValue(parametervalue = param)
        )
    parameters: AssociationProxy[Set["Parameter"]] = association_proxy("parametervalue_mappings", "parameter")

    textparametervalues: Mapped[Set["UnitToTextParameter"]] = relationship(back_populates='unit',
                                                                           cascade='all,delete-orphan')
    textparameters: AssociationProxy[Set["TextParameter"]] = association_proxy("textparametervalues", "parameter")

    def get_values_for_parameter(self, param: Parameter) -> List[ParameterValue]:
        if param.target is not Parameter.Unit:
            raise ValueError("Parameter %s does not classify units" % param.keyword)
        return [x for x in param.values if x in self.parametervalues]    

    comments: Mapped[Set["Comment"]] = relationship(secondary=comments_to_units)
    examples: Mapped[Set["Example"]] = relationship(secondary=examples_to_units, back_populates="units")
    sources: Mapped[Set["Source"]] = relationship(secondary=sources_to_units)

    # __table_args__ = (UniqueConstraint('linker', 'semfield_id'),
    #                  ) # Ensures that the combination of linker and semantic field is unique

class UnitLinkType(Base):
    __tablename__ = 'unitlinktypes'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)

class UnitToUnit(Base): #connections between units
    __tablename__ = 'units_to_units'

    # id: Mapped[int] = mapped_column(primary_key=True)

    # rank = db.Column(db.Integer, nullable=True)

    source_id: Mapped[int] = mapped_column(ForeignKey('units.id'), primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey('units.id'), primary_key=True)
    unitlinktype_id: Mapped[int] = mapped_column(ForeignKey('unitlinktypes.id'), primary_key=True)

    source: Mapped["Unit"] = relationship(foreign_keys=[source_id], back_populates="links")
    target: Mapped["Unit"] = relationship(foreign_keys=[target_id])
    unitlinktype: Mapped["UnitLinkType"] = relationship()

# class Label(Base):
#     __tablename__ = 'labels' # Assign a parameter value to a Unit

#     label_id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.Text, unique=True)
    # decode = db.Column(db.Text)
    # rank = db.Column(db.Integer, unique=True)
    # label_type = db.Column(db.Integer, unique=False) # what column is this label from? 1 -- number of components, 2 -- position, 3 -- ...        

# FORMS

class Form(Base):
    __tablename__ = 'forms'

    id: Mapped[int] = mapped_column(primary_key=True)

    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'))
    unit: Mapped["Unit"] = relationship(back_populates="forms")

    formtype_id: Mapped[int] = mapped_column(ForeignKey('formtypes.id'))
    formtype: Mapped["FormType"] = relationship(back_populates="forms")

    # gloss_id = db.Column(db.Integer, db.ForeignKey('glosses.gloss_id'), nullable=False)
    text: Mapped[str]

    parametervalue_mappings: Mapped[Set["FormToParameterValue"]] = relationship(back_populates='form',
                                                                                cascade='all,delete-orphan')
    parametervalues: AssociationProxy[Set["ParameterValue"]] = association_proxy(
        "parametervalue_mappings", 
        "parametervalue", 
        creator = lambda param: FormToParameterValue(parametervalue = param)
        )
    parameters: AssociationProxy[Set["Parameter"]] = association_proxy("parametervalue_mappings", "parameter")

    textparametervalues: Mapped[Set["FormToTextParameter"]] = relationship(back_populates='form',
                                                                           cascade='all,delete-orphan')
    textparameters: AssociationProxy[Set["TextParameter"]] = association_proxy("textparametervalues", "parameter")

    examples: Mapped[Set["Example"]] = relationship(secondary=examples_to_forms, back_populates="forms")

    # __table_args__ = (UniqueConstraint('unit_id', 'formtype_id', "text"),
    #                  ) # Only one unit-type mapping for a given text value

    def get_values_for_parameter(self, param: Parameter) -> List[ParameterValue]:
        if param.target is not Parameter.Form:
            raise ValueError("Parameter %s does not classify forms" % param.keyword)
        return [x for x in param.values if x in self.parametervalues]

parameters_to_formtypes = Table(
    "parameters_to_formtypes",
    Base.metadata,
    Column("parameter_id", ForeignKey("parameters.id")),
    Column("formtype_id", ForeignKey("formtypes.id"))
)

textparameters_to_formtypes = Table(
    "textparameters_to_formtypes",
    Base.metadata,
    Column("textparameter_id", ForeignKey("parameters.id")),
    Column("formtype_id", ForeignKey("formtypes.id"))
)

class FormType(Base):
    __tablename__ = 'formtypes' # linker, correl, phonvar, mainpart

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str]
    keyword: Mapped[str] = mapped_column(unique=True)

    forms: Mapped[Set["Form"]] = relationship(back_populates="formtype")
    parameters: Mapped[Set["Parameter"]] = relationship(secondary=parameters_to_formtypes)

# MEANINGS

class Meaning(Base):
    __tablename__ = 'meanings'

    id: Mapped[int] = mapped_column(primary_key=True)

    meaning: Mapped[str]
    pos: Mapped[str]
    pos_type: Mapped[str]
    other_senses: Mapped[str]
    other_pos: Mapped[str]

    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'))
    unit: Mapped["Unit"] = relationship()

    source_id: Mapped[int] = mapped_column(ForeignKey('sources.id'))
    source: Mapped["Source"] = relationship()