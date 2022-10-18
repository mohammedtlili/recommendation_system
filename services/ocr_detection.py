from PIL import Image
import requests
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from fastapi import UploadFile

model = 'microsoft/trocr-small-printed'


class OCRModel:
    __instance = dict()

    def __init__(self):
        self.__dict__ = self.__instance
        self.model = VisionEncoderDecoderModel.from_pretrained(model)
        self.processor = TrOCRProcessor.from_pretrained(model)

    def predict_from_url(self, image_url: str) -> str:
        image = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text

    def predict_from_file(self, file: UploadFile) -> str:
        image = Image.open(file.file).convert("RGB")
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text


lm = OCRModel()
