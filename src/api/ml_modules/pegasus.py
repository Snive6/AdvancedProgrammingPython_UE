from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch


def pegasus_summarizer(text, max_length):
    model_name = 'google/pegasus-xsum'
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
    batch = tokenizer.prepare_seq2seq_batch(text, truncation=True, padding='longest', return_tensors='pt',
                                            max_length=100)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text


if __name__ == "__main__":
    text_example = open("example/text_example.txt", "r").read()
    summary_text = pegasus_summarizer(text_example, max_length=100)
    print(summary_text)
