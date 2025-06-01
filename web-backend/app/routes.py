from flask import Blueprint, jsonify, request
from .models import db, Herb, Treatment, HerbRef
import logging
import zhconv

# set logging level to info
logging.basicConfig(level=logging.INFO)

bp = Blueprint('main', __name__)


@bp.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Convert query to simplified Chinese
    query = zhconv.convert(query, 'zh-cn')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    herbs = Herb.query.filter(Herb.name.contains(query)).all()
    treatments = Treatment.query.filter(Treatment.prescription_name.contains(query)).all()

    herbs_result = [
        {
            'id': herb.herb_id,
            'name': herb.name,
            'description': herb.description,
            'link': f'/ref/herb/?herb={herb.name}'
        } for herb in herbs
    ]
    treatments_result = [
        {
            'id': treatment.treatment_id,
            'name': treatment.prescription_name,
            'description': treatment.notes,
            'link': f'/ref/treatment/?treatment={treatment.prescription_name}'
        } for treatment in treatments
    ]

    return jsonify({'herbs': herbs_result, 'treatments': treatments_result})


@bp.route('/api/herb', methods=['GET'])
def get_herb_info():
    query = request.args.get('herb')
    # Convert query to simplified Chinese
    query = zhconv.convert(query, 'zh-cn')

    if not query:
        return jsonify({'error': 'No herb query provided'}), 400

    herb = Herb.query.filter_by(name=query).first()
    if not herb:
        return jsonify({'error': 'Herb not found'}), 404

    treatments = db.session.query(
        Treatment.prescription_name,
        HerbRef.dosage,
        HerbRef.preparation
    ).join(HerbRef, HerbRef.treatment_id == Treatment.treatment_id).filter(HerbRef.herb_id == herb.herb_id).all()

    treatment_list = [{'name': t[0], 'dosage': t[1], 'preparation': t[2]} for t in treatments]

    return jsonify({'name': herb.name,
                    'description': herb.description,
                    'treatments': treatment_list,
                    'herb_pinyin_name': herb.herb_pinyin_name,
                    'herb_en_name': herb.herb_en_name,
                    'herb_latin_name': herb.herb_latin_name,
                    'properties': herb.properties,
                    'meridians': herb.meridians,
                    'UsePart': herb.UsePart,
                    'function': herb.function,
                    'indication': herb.indication,
                    'toxicity': herb.toxicity,
                    'clinical_manifestations': herb.clinical_manifestations,
                    'therapeutic_en_class': herb.therapeutic_en_class,
                    'therapeutic_cn_class': herb.therapeutic_cn_class,
                    'tcmid_id': herb.tcmid_id,
                    'tcm_id_id': herb.tcm_id_id,
                    'symmap_id': herb.symmap_id,
                    'tcmsp_id': herb.tcmsp_id
                    })


@bp.route('/api/treatment', methods=['GET'])
def get_treatment_info():
    query = request.args.get('treatment')
    # Convert query to simplified Chinese
    query = zhconv.convert(query, 'zh-cn')

    if not query:
        return jsonify({'error': 'No treatment query provided'}), 400

    treatment = Treatment.query.filter_by(prescription_name=query).first()
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404

    herbs = db.session.query(
        Herb.name,
        HerbRef.dosage,
        HerbRef.preparation
    ).join(HerbRef, HerbRef.herb_id == Herb.herb_id).filter(HerbRef.treatment_id == treatment.treatment_id).all()

    herb_list = [{'name': h[0], 'dosage': h[1], 'preparation': h[2]} for h in herbs]

    return jsonify({'name': treatment.prescription_name, 'notes': treatment.notes, 'herbs': herb_list})



@bp.route('/api/suggestions', methods=['GET'])
def suggestions():
    """
    Search suggestions
    :return:
    """
    query = request.args.get('query')
    # Convert query to simplified Chinese
    query = zhconv.convert(query, 'zh-cn')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    herb_suggestions = Herb.query.filter(Herb.name.contains(query)).all()
    treatment_suggestions = Treatment.query.filter(Treatment.prescription_name.contains(query)).all()

    herb_suggestions_result = [{'id': herb.herb_id, 'name': herb.name, 'type': 'herb'} for herb in herb_suggestions]
    treatment_suggestions_result = [
        {'id': treatment.treatment_id, 'name': treatment.prescription_name, 'type': 'treatment'} for treatment in
        treatment_suggestions]

    return jsonify({'herbs': herb_suggestions_result, 'treatments': treatment_suggestions_result})
