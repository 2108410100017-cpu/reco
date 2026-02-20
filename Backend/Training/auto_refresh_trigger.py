import subprocess
from drift_detector import compute_embedding_drift, compute_attribute_drift

if compute_embedding_drift() > 0.15 or compute_attribute_drift() > 0.25:
    print("DRIFT DETECTED → FULL RETRAIN")
    subprocess.run(["python", "train.py"])
else:
    print("No drift. System stable.")
