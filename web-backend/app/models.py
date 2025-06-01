from . import db


class Herb(db.Model):
    """
    Use flask SQLAlchemy to interact with table herb. It has three columns: herb_id, name, and description.
    """
    __tablename__ = 'herb_jointed'
    herb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80))
    # description = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))

# Herb_pinyin_name	Herb_en_name	Herb_latin_name	Properties	Meridians	UsePart	Function	Indication	Toxicity	Clinical_manifestations	Therapeutic_en_class	Therapeutic_cn_class	TCMID_id	TCM_ID_id	SymMap_id	TCMSP_id
    herb_pinyin_name = db.Column(db.String(80))
    herb_en_name = db.Column(db.String(80))
    herb_latin_name = db.Column(db.String(80))
    properties = db.Column(db.String(200))
    meridians = db.Column(db.String(200))
    UsePart = db.Column(db.String(200))
    function = db.Column(db.String(200))
    indication = db.Column(db.String(200))
    toxicity = db.Column(db.String(200))
    clinical_manifestations = db.Column(db.String(200))
    therapeutic_en_class = db.Column(db.String(200))
    therapeutic_cn_class = db.Column(db.String(200))
    tcmid_id = db.Column(db.String(80))
    tcm_id_id = db.Column(db.String(80))
    symmap_id = db.Column(db.String(80))
    tcmsp_id = db.Column(db.String(80))
class Treatment(db.Model):
    """
    Use flask SQLAlchemy to interact with table treatment. It has seven columns: treatment_id, ref_id, disease, symptoms, prescription_name, herbs, and notes.
    """
    __tablename__ = 'treatment'
    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_id = db.Column(db.Integer)
    disease = db.Column(db.String(200))
    symptoms = db.Column(db.String(200))
    prescription_name = db.Column(db.String(80), unique=True, nullable=False)
    herbs = db.Column(db.String(200))
    notes = db.Column(db.String(200), nullable=False)


class HerbRef(db.Model):
    """
    Use flask SQLAlchemy to interact with table herb_ref. It has five columns: herb_id, treatment_id, ref_id, dosage, and preparation.
    """
    __tablename__ = 'herb_ref'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    herb_id = db.Column(db.Integer, db.ForeignKey('herb_jointed.herb_id'))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.treatment_id'))
    ref_id = db.Column(db.Integer)
    dosage = db.Column(db.String(50))
    preparation = db.Column(db.String(100))

    herb = db.relationship('Herb', backref=db.backref('herb_refs', lazy=True))
    treatment = db.relationship('Treatment', backref=db.backref('treatment_refs', lazy=True))
