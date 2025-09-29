"""
Simple test script to verify CRUD operations for Patients and Doctors
Run this after starting the server with: uvicorn app.main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_patients_crud():
    print("=== Testing Patients CRUD ===")
    
    # 1. CREATE Patient
    patient_data = {
        "full_name": "Juan Pérez",
        "email": "juan.perez@email.com",
        "phone": "123456789",
        "dni": "12345678A"
    }
    
    print("1. Creating patient...")
    response = requests.post(f"{BASE_URL}/pacientes", json=patient_data)
    if response.status_code == 201:
        patient = response.json()
        patient_id = patient["id"]
        print(f"✅ Patient created with ID: {patient_id}")
    else:
        print(f"❌ Failed to create patient: {response.status_code}")
        return
    
    # 2. GET Patient by ID
    print("2. Getting patient by ID...")
    response = requests.get(f"{BASE_URL}/pacientes/{patient_id}")
    if response.status_code == 200:
        print("✅ Patient retrieved successfully")
    else:
        print(f"❌ Failed to get patient: {response.status_code}")
    
    # 3. LIST Patients
    print("3. Listing all patients...")
    response = requests.get(f"{BASE_URL}/pacientes")
    if response.status_code == 200:
        patients = response.json()
        print(f"✅ Retrieved {len(patients)} patients")
    else:
        print(f"❌ Failed to list patients: {response.status_code}")
    
    # 4. UPDATE Patient
    print("4. Updating patient...")
    update_data = {"phone": "987654321"}
    response = requests.put(f"{BASE_URL}/pacientes/{patient_id}", json=update_data)
    if response.status_code == 200:
        updated_patient = response.json()
        print(f"✅ Patient updated. New phone: {updated_patient['phone']}")
    else:
        print(f"❌ Failed to update patient: {response.status_code}")
    
    # 5. DELETE Patient
    print("5. Deleting patient...")
    response = requests.delete(f"{BASE_URL}/pacientes/{patient_id}")
    if response.status_code == 204:
        print("✅ Patient deleted successfully")
    else:
        print(f"❌ Failed to delete patient: {response.status_code}")

def test_doctors_crud():
    print("\n=== Testing Doctors CRUD ===")
    
    # First, we need a specialty ID. Let's assume ID 1 exists or create one
    print("0. Checking/Creating specialty...")
    specialty_data = {"name": "Medicina General"}
    requests.post(f"{BASE_URL}/especialidades", json=specialty_data)
    
    # 1. CREATE Doctor
    doctor_data = {
        "full_name": "Dr. María González",
        "specialty_id": 1,
        "work_start_hour": 8,
        "work_end_hour": 16,
        "slot_minutes": 30
    }
    
    print("1. Creating doctor...")
    response = requests.post(f"{BASE_URL}/medicos", json=doctor_data)
    if response.status_code == 201:
        doctor = response.json()
        doctor_id = doctor["id"]
        print(f"✅ Doctor created with ID: {doctor_id}")
    else:
        print(f"❌ Failed to create doctor: {response.status_code}")
        print(response.text)
        return
    
    # 2. GET Doctor by ID
    print("2. Getting doctor by ID...")
    response = requests.get(f"{BASE_URL}/medicos/{doctor_id}")
    if response.status_code == 200:
        print("✅ Doctor retrieved successfully")
    else:
        print(f"❌ Failed to get doctor: {response.status_code}")
    
    # 3. LIST Doctors
    print("3. Listing all doctors...")
    response = requests.get(f"{BASE_URL}/medicos")
    if response.status_code == 200:
        doctors = response.json()
        print(f"✅ Retrieved {len(doctors)} doctors")
    else:
        print(f"❌ Failed to list doctors: {response.status_code}")
    
    # 4. UPDATE Doctor
    print("4. Updating doctor...")
    update_data = {"slot_minutes": 45}
    response = requests.put(f"{BASE_URL}/medicos/{doctor_id}", json=update_data)
    if response.status_code == 200:
        updated_doctor = response.json()
        print(f"✅ Doctor updated. New slot_minutes: {updated_doctor['slot_minutes']}")
    else:
        print(f"❌ Failed to update doctor: {response.status_code}")
    
    # 5. DELETE Doctor
    print("5. Deleting doctor...")
    response = requests.delete(f"{BASE_URL}/medicos/{doctor_id}")
    if response.status_code == 204:
        print("✅ Doctor deleted successfully")
    else:
        print(f"❌ Failed to delete doctor: {response.status_code}")

if __name__ == "__main__":
    print("Starting CRUD tests...")
    print("Make sure the server is running on http://localhost:8000")
    
    try:
        test_patients_crud()
        test_doctors_crud()
        print("\n🎉 All tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
