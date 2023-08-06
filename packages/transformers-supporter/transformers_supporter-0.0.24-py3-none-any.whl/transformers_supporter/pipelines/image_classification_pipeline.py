#https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.ImageClassificationPipeline
#https://github.com/huggingface/transformers/blob/v4.30.0/src/transformers/pipelines/image_classification.py#L32
from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class ImageClassificationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        postprocess_kwargs = {}
        if "top_k" in kwargs:
            preprocess_kwargs["top_k"] = kwargs["top_k"]
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs):
        return self.image_processor(inputs, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, top_k=5):
        logits = model_outputs['logits']
        probabilities = F.softmax(logits, dim=-1)
        results = []
        for i, probability in enumerate(probabilities[0]):
            label = self.model.config.id2label[i]
            results.append({'label': label, 'score': probability.item()})   
        results.sort(key=lambda x: x['score'], reverse=True)
        if top_k != None:
            results = results[:top_k]            
        return results

def register_pipeline():
    PIPELINE_REGISTRY.register_pipeline('image-classification', 
                                    #pt_model=AutoModelForImageClassification,
                                    pipeline_class=ImageClassificationPipeline)
