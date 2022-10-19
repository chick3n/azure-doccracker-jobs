import os
from pydoc import doc
from typing import List, Tuple
from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction
from azure.core.credentials import AzureKeyCredential
import unicodedata
import re
import stanza

class ExtractiveSummary:
    def __init__(self,  texts:List[str], max_document_length:int=40000, summary_sentence_length=4):
        self.texts = texts
        self.max_document_length = max_document_length
        self.summary_sentence_length = summary_sentence_length
        self.endpoint = os.environ['Cognitive_Endpoint']
        self.key = os.environ['Cognitive_Key']
        self.documents:List[str] = []
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize', download_method=None, model_dir='./models')
        self.__process_texts()

    def get_documents(self) -> List[str]:
        return self.documents

    def __client(self) -> TextAnalyticsClient:
        ta_credential = AzureKeyCredential(self.key)
        return TextAnalyticsClient(endpoint=self.endpoint,
                                    credential=ta_credential)
    
    def summarize(self) -> Tuple[str, List[str]]:
        client = self.__client()
        poller = client.begin_analyze_actions(
            self.documents,
            actions=[
                ExtractSummaryAction(max_sentence_count=self.summary_sentence_length)
            ]
        )

        summary_results = poller.result()
        summaries = []
        errors = []

        for result in summary_results:
            extract_summary_result = result[0]
            if(extract_summary_result.is_error):
                errors.append("... Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
            else:
                summaries.append(" ".join([sentence.text for sentence in extract_summary_result.sentences]))
        
        return summaries, errors

    def __process_texts(self):
        for text in self.texts:
            sentences = self.__sentence_extraction(text)
            if len(sentences) > 0:
                self.documents = [*self.documents, *self.__pack_document(sentences)]

    def __sentence_extraction(self, text):
        if text is None:
            return []
        doc = self.nlp(text)
        sentences = []
        for sentence in doc.sentences:
            clean_sentence = self.sentence_cleaning(sentence.text)
            sentences.append(clean_sentence)

        return sentences

    def __pack_document(self, sentences):
        document = ''
        appended = False
        documents = []

        for sentence in sentences:
            pre_document = f'{document} {sentence}'
            if len(pre_document) > self.max_document_length:
                documents.append(document)
                document = sentence
                appended = True
            else:
                appended = False
                document = pre_document

        if not appended and len(document) > 0:
            documents.append(document)

        return documents

    def sentence_cleaning(self, text):
        return text.replace('\t', '').replace('\n', '')

    

