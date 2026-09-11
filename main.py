from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import uvicorn

app = FastAPI(
    title="SIH26105 API", 
    description="Cyber Risk Quantification Engine (Log-Scaled Ensemble)"
)

# Load trained artifacts
model = joblib.load("cyber_loss_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")

class TelemetryInput(BaseModel):
    Company_Size: str = "Medium"
    Patch_Age_Days: int = 45
    Open_Vulnerabilities: int = 25
    CVSS_Score: float = 7.2
    Security_Audit_Score: float = 60.0
    Data_Exfiltration_GB: float = 10.0
    Firewall: int = 1
    MFA: int = 0
    EDR: int = 0
    Security_Training: int = 0

class OptimizeInput(BaseModel):
    telemetry: TelemetryInput
    budget_usd: float

def compute_engineered_features(data_dict: dict) -> pd.DataFrame:
    df_in = pd.DataFrame([data_dict])

    # Feature engineering matching notebook logic
    df_in['Patch_Vuln_Risk'] = df_in['Patch_Age_Days'] * df_in['Open_Vulnerabilities']
    df_in['CVSS_Exfil_Impact'] = df_in['CVSS_Score'] * df_in['Data_Exfiltration_GB']
    df_in['Control_Shield_Count'] = (
        df_in['Firewall'].astype(int) + 
        df_in['MFA'].astype(int) + 
        df_in['EDR'].astype(int) + 
        df_in['Security_Training'].astype(int)
    )
    df_in['Unprotected_Risk_Ratio'] = (df_in['CVSS_Score'] * df_in['Data_Exfiltration_GB']) / (df_in['Control_Shield_Count'] + 1)

    return df_in

def get_financial_loss_prediction(df_in: pd.DataFrame) -> float:
    X_proc = preprocessor.transform(df_in)
    pred_log = model.predict(X_proc)[0]
    pred_usd = float(np.expm1(pred_log))
    return max(0.0, pred_usd)

@app.get("/")
def root():
    return {"status": "Online", "service": "SIH26105 Risk Engine"}

@app.post("/predict_risk")
def predict_risk(data: TelemetryInput):
    df_in = compute_engineered_features(data.dict())
    pred_loss = get_financial_loss_prediction(df_in)

    tier = "CRITICAL" if pred_loss > 500000 else "HIGH" if pred_loss > 200000 else "MEDIUM"
    return {"predicted_financial_loss_usd": round(pred_loss, 2), "risk_tier": tier}

@app.post("/optimize_investment")
def optimize_investment(data: OptimizeInput):
    base_dict = data.telemetry.dict()
    budget = data.budget_usd

    base_df = compute_engineered_features(base_dict)
    base_loss = get_financial_loss_prediction(base_df)

    controls = {
        "Enable MFA": {"field": "MFA", "cost": 15000},
        "Deploy EDR": {"field": "EDR", "cost": 30000},
        "Security Training": {"field": "Security_Training", "cost": 10000}
    }

    allocations = []
    rem_budget = budget
    current_loss = base_loss

    for name, item in controls.items():
        if base_dict[item["field"]] == 0 and rem_budget >= item["cost"]:
            temp_dict = base_dict.copy()
            temp_dict[item["field"]] = 1

            temp_df = compute_engineered_features(temp_dict)
            new_loss = get_financial_loss_prediction(temp_df)

            savings = current_loss - new_loss
            if savings > 0:
                allocations.append({
                    "control": name,
                    "cost_usd": item["cost"],
                    "risk_reduction_usd": round(savings, 2)
                })
                rem_budget -= item["cost"]
                base_dict[item["field"]] = 1
                current_loss = new_loss

    return {
        "baseline_loss_usd": round(base_loss, 2),
        "post_investment_loss_usd": round(current_loss, 2),
        "total_risk_reduced_usd": round(base_loss - current_loss, 2),
        "remaining_budget_usd": rem_budget,
        "recommendations": allocations
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
