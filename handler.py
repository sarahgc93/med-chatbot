from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
import torch


# Much of this code borrowed from huggingface docs.
# See https://huggingface.co/docs/inference-endpoints/main/en/engines/toolkit#create-a-custom-inference-handler.


class EndpointHandler:
    def __init__(self, path=""):
        """
        path: directory where your adapter is stored
        """
        base_model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(base_model, path)

        # Build text-generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
        self.device = 0 if torch.cuda.is_available() else -1


    def __call__(self, data):
        """
        data: dict from the inference request
        """
        inputs = data.get("inputs", "")
        parameters = data.get("parameters", {}) or {}

        # format input to our expected chat formal
        messages = [
            {"role": "user", "content": inputs}
        ]
        # match the template used in training
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # tokenize prompt
        model_inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # generate output
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=parameters.get("max_new_tokens", 256),
            temperature=parameters.get("temperature", 0.7),
            top_p=parameters.get("top_p", 0.9),
            do_sample=parameters.get("do_sample", True)
        )

        # decode response
        decoded = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        # Strip prompt to leave only assistant answer
        # this is not consistently working for me
        #assistant_response = decoded[len(prompt):].strip()
        assistant_response = decoded.strip()
        return {"generated_text": assistant_response}
