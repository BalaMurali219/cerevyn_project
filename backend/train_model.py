import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

# Create model directory if not exists
os.makedirs('model', exist_ok=True)

# Path to the dataset
data_path = r'..\archive\customer_conversion_traing_dataset .csv'

# Load dataset
df = pd.read_csv(data_path)

# Drop LeadID as it's not a feature
if 'LeadID' in df.columns:
    df.drop('LeadID', axis=1, inplace=True)

# Identify categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns

# Encode categorical columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    # Filling missing values just in case
    df[col] = df[col].fillna('Unknown')
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Prepare features and target
X = df.drop('Conversion (Target)', axis=1)
y = df['Conversion (Target)']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
from sklearn.metrics import accuracy_score
y_pred = model.predict(X_test_scaled)
print(f"Model Accuracy on training split: {accuracy_score(y_test, y_pred)}")

# Save the model, scaler, and encoders
joblib.dump(model, 'model/rf_model.joblib')
joblib.dump(scaler, 'model/scaler.joblib')
joblib.dump(label_encoders, 'model/label_encoders.joblib')

# Save expected columns
joblib.dump(list(X.columns), 'model/expected_columns.joblib')

print("Model, scaler, and encoders saved successfully.")
