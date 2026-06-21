doctor_mapping = {
    "flu": {
        "doctor": "General Physician",
        "hospital": "Clinic",
        "urgency": "Normal"
    },
    "covid19": {
        "doctor": "Pulmonologist",
        "hospital": "Multi Specialty Hospital",
        "urgency": "Within 24 Hours"
    },
    "dengue": {
        "doctor": "Infectious Disease Specialist",
        "hospital": "Government Hospital",
        "urgency": "Immediate"
    },
    "malaria": {
        "doctor": "Infectious Disease Specialist",
        "hospital": "General Hospital",
        "urgency": "Immediate"
    },
    "hypertension": {
        "doctor": "Cardiologist",
        "hospital": "Heart Care Center",
        "urgency": "Normal"
    },
    "heart_disease": {
        "doctor": "Cardiologist",
        "hospital": "Cardiac Hospital",
        "urgency": "Emergency"
    },
    "asthma": {
        "doctor": "Pulmonologist",
        "hospital": "Chest Hospital",
        "urgency": "Within 24 Hours"
    },
    "migraine": {
        "doctor": "Neurologist",
        "hospital": "Neurology Center",
        "urgency": "Normal"
    }
}


def get_doctor_info(disease):
    disease_data = {
        "flu": {
            "doctor": "General Physician",
            "severity": "Low",
            "description": "Viral infection affecting the respiratory system.",
            "medicines": ["Paracetamol", "Cetirizine"],
            "precautions": ["Drink warm water", "Take adequate rest", "Avoid cold foods"]
        },
        "covid19": {
            "doctor": "Pulmonologist",
            "severity": "Medium",
            "description": "Contagious respiratory illness caused by SARS-CoV-2.",
            "medicines": ["Paracetamol", "Vitamin C"],
            "precautions": ["Isolate yourself", "Monitor oxygen levels"]
        },
        "dengue": {
            "doctor": "Infectious Disease Specialist",
            "severity": "High",
            "description": "Mosquito-borne viral infection.",
            "medicines": ["Paracetamol", "ORS"],
            "precautions": ["Drink plenty of fluids", "Avoid painkillers like aspirin"]
        },
        "malaria": {
            "doctor": "Infectious Disease Specialist",
            "severity": "High",
            "description": "Parasitic infection transmitted by mosquitoes.",
            "medicines": ["Chloroquine", "Artemisinin"],
            "precautions": ["Use mosquito nets", "Complete medication course"]
        },
        "hypertension": {
            "doctor": "Cardiologist",
            "severity": "Medium",
            "description": "Persistently elevated blood pressure.",
            "medicines": ["Amlodipine"],
            "precautions": ["Reduce salt intake", "Exercise regularly"]
        },
        "diabetes": {
            "doctor": "Endocrinologist",
            "severity": "Medium",
            "description": "Condition affecting blood sugar regulation.",
            "medicines": ["Metformin"],
            "precautions": ["Monitor blood sugar", "Avoid sugary foods"]
        },
        "asthma": {
            "doctor": "Pulmonologist",
            "severity": "Medium",
            "description": "Chronic respiratory disease causing breathing difficulty.",
            "medicines": ["Salbutamol Inhaler", "Budesonide"],
            "precautions": ["Avoid dust and smoke", "Carry inhaler regularly"]
        },
        "bronchitis": {
            "doctor": "Pulmonologist",
            "severity": "Medium",
            "description": "Inflammation of bronchial tubes causing cough.",
            "medicines": ["Cough Syrup", "Bronchodilator"],
            "precautions": ["Avoid smoking", "Drink warm fluids"]
        },
        "heart_disease": {
            "doctor": "Cardiologist",
            "severity": "High",
            "description": "Condition affecting heart function and blood circulation.",
            "medicines": ["Aspirin", "Atorvastatin"],
            "precautions": ["Avoid fatty foods", "Regular heart checkups"]
        },
        "food_poisoning": {
            "doctor": "Gastroenterologist",
            "severity": "Medium",
            "description": "Illness caused by contaminated food or water.",
            "medicines": ["ORS", "Probiotics"],
            "precautions": ["Drink clean water", "Avoid outside food"]
        },
        "stress": {
            "doctor": "Psychologist",
            "severity": "Low",
            "description": "Mental and emotional strain affecting wellbeing.",
            "medicines": ["Relaxation Therapy"],
            "precautions": ["Meditation", "Regular sleep schedule"]
        },
        "common_cold": {
            "doctor": "General Physician",
            "severity": "Low",
            "description": "Viral infection affecting the nose and throat.",
            "medicines": ["Paracetamol", "Cetirizine", "Steam Inhalation"],
            "precautions": [
                "Drink warm fluids",
                "Take adequate rest",
                "Avoid cold exposure",
                "Wash hands frequently"
            ]
        },
        "migraine": {
            "doctor": "Neurologist",
            "severity": "Low",
            "description": "Neurological condition causing severe headaches.",
            "medicines": ["Ibuprofen"],
            "precautions": ["Avoid stress", "Maintain sleep schedule"]
        }
    }

    return disease_data.get(
        disease.lower(),
        {
            "doctor": "General Physician",
            "severity": "Low",
            "description": "Further medical evaluation is recommended.",
            "medicines": ["Consult a healthcare professional"],
            "precautions": [
                "Maintain healthy lifestyle",
                "Drink adequate water",
                "Get sufficient rest"
                ]
                }
                
                )
