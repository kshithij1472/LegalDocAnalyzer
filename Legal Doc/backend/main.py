from utils.model_loader import load_ner_model, load_tokenizer

# Load models at startup
ner_model = load_ner_model()
tokenizer = load_tokenizer()

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        text = await parse_document(file)
        
        # NER Processing
        inputs = tokenizer(text, return_tensors="tf", truncation=True, max_length=512)
        outputs = ner_model(**inputs)
        
        # Process results
        entities = extract_entities(outputs, text)
        
        return {
            "entities": entities,
            "simplified": simplify_text(text)  # Add your simplification logic
        }
    
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")