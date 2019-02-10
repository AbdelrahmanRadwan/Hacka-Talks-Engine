# -*- coding: utf-8 -*-
import sys
import os
import dateparser
from pathlib import Path


ROOT_DIR = str(Path(__file__).parents[2])

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath('..'))

from IE.information_extraction_module.helper_functions import process_row_data, clean_date, clean_url
import spacy
from spacy_lookup import Entity

ROOT_DIR = str(Path(__file__).parents[1])
FEATURES_DIR = ROOT_DIR + "/data/extracted_features/reference/"


class InformationExtractor:
    def __init__(self):
        self.extractor = dict()
        self.extractor["career_level"] = self.create_ner_detector(FEATURES_DIR + "career_level_list.txt")
        self.extractor["city"] = self.create_ner_detector(FEATURES_DIR + "city_list.txt")
        self.extractor["company_name"] = self.create_ner_detector(FEATURES_DIR + "company_name_list.txt")
        self.extractor["currency"] = self.create_ner_detector(FEATURES_DIR + "currency_list.txt")
        self.extractor["education"] = self.create_ner_detector(FEATURES_DIR + "education_list.txt")
        self.extractor["job_title"] = self.create_ner_detector(FEATURES_DIR + "job_title_list.txt")
        self.extractor["language"] = self.create_ner_detector(FEATURES_DIR + "languages_list.txt")
        self.extractor["maximum_salary"] = self.create_ner_detector(FEATURES_DIR + "maximum_salary_list.txt")
        self.extractor["minimum_salary"] = self.create_ner_detector(FEATURES_DIR + "minimum_salary_list.txt")
        self.extractor["payment_period"] = self.create_ner_detector(FEATURES_DIR + "payment_period_list.txt")
        self.extractor["skill"] = self.create_ner_detector(FEATURES_DIR + "skills_list.txt")
        self.extractor["work_type"] = self.create_ner_detector(FEATURES_DIR + "work_type_list.txt")
        self.extractor["years_of_experience"] = self.create_ner_detector(FEATURES_DIR + "years_of_experience_list.txt")

    @staticmethod
    def create_ner_detector(file_directory):
        nlp = spacy.blank('en')
        with open(file_directory) as f:
            reference_data = f.read().splitlines()

        entity = Entity(keywords_list=reference_data)
        nlp.add_pipe(entity)
        return nlp

    def generate_response(self, doc, response_index):
        try:
            # return [{"start_token": element[1], "text": element[0]} for element in self.extractor[response_index](doc)._.entities]
            return list(set([element[0].lower() for element in self.extractor[response_index](doc)._.entities])) or []
        except IndexError:
            return []

    def get_named_entities_str(self, doc):
        response = dict()
        response["query"] = doc
        response["career_level"] = self.generate_response(doc, "career_level")
        response["city"] = self.generate_response(doc, "city")
        response["company_name"] = self.generate_response(doc, "company_name")
        response["currency"] = self.generate_response(doc, "currency")
        response["education"] = self.generate_response(doc, "education")
        response["job_title"] = self.generate_response(doc, "job_title")
        response["language"] = self.generate_response(doc, "language")
        response["maximum_salary"] = self.generate_response(doc, "maximum_salary")
        response["minimum_salary"] = self.generate_response(doc, "minimum_salary")
        response["payment_period"] = self.generate_response(doc, "payment_period")
        response["skill"] = self.generate_response(doc, "skill")
        response["work_type"] = self.generate_response(doc, "work_type")
        response["years_of_experience"] = self.generate_response(doc, "years_of_experience")
        return response

    def get_named_entities_json(self, json_doc):
        response = dict()
        doc = process_row_data(json_doc)
        response["original_job"] = json_doc
        response["query"] = doc
        response["career_level"] = self.generate_response(doc, "career_level")
        response["city"] = self.generate_response(doc, "city") + [json_doc["workplace"]]
        response["company_name"] = self.generate_response(doc, "company_name") + [json_doc["company_name"]]
        response["currency"] = self.generate_response(doc, "currency")
        response["education"] = self.generate_response(doc, "education") + [json_doc["education"]]
        response["job_title"] = self.generate_response(doc, "job_title") + [json_doc["position_name"]]
        response["language"] = self.generate_response(doc, "language")
        response["maximum_salary"] = self.generate_response(doc, "maximum_salary") + [json_doc["salary"]]
        response["minimum_salary"] = self.generate_response(doc, "minimum_salary") + [json_doc["salary"]]
        response["payment_period"] = self.generate_response(doc, "payment_period")
        response["skill"] = self.generate_response(doc, "skill")
        response["work_type"] = self.generate_response(doc, "work_type") + [json_doc["employment_type"]]
        response["years_of_experience"] = self.generate_response(doc, "years_of_experience") + [json_doc["experience"]]
        response["company_industry"] = json_doc["company_industry"]
        response["url"] = clean_url(json_doc["url"])
        response["job_id"] = response["url"]
        response["post_date"] = dateparser.parse(clean_date(json_doc["post_date"]))

        return response
