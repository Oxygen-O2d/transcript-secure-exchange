@echo off
set PYTHON_EXE=venv\Scripts\python.exe
echo running data/generate_mock_data.py
%PYTHON_EXE% data\generate_mock_data.py
echo running phase1_symmetric\encryption.py
%PYTHON_EXE% phase1_symmetric\encryption.py
echo running phase1_symmetric\avalanche.py
%PYTHON_EXE% phase1_symmetric\avalanche.py
echo running phase1_symmetric\ecb_vs_cbc.py
%PYTHON_EXE% phase1_symmetric\ecb_vs_cbc.py
echo running phase1_symmetric\benchmark.py
%PYTHON_EXE% phase1_symmetric\benchmark.py
echo running phase2_asymmetric\rsa_hybrid.py
%PYTHON_EXE% phase2_asymmetric\rsa_hybrid.py
echo running phase2_asymmetric\dh_exchange.py
%PYTHON_EXE% phase2_asymmetric\dh_exchange.py
echo running phase2_asymmetric\mitm_attack.py
%PYTHON_EXE% phase2_asymmetric\mitm_attack.py
echo running phase3_integrity\hashing.py
%PYTHON_EXE% phase3_integrity\hashing.py
echo running phase3_integrity\tamper_detect.py
%PYTHON_EXE% phase3_integrity\tamper_detect.py
echo running phase4_authentication\digital_signature.py
%PYTHON_EXE% phase4_authentication\digital_signature.py
echo running phase4_authentication\certificate.py
%PYTHON_EXE% phase4_authentication\certificate.py
echo running phase4_authentication\kerberos_mock.py
%PYTHON_EXE% phase4_authentication\kerberos_mock.py
echo running pipeline\run_pipeline.py
%PYTHON_EXE% pipeline\run_pipeline.py
echo running pipeline\run_pipeline.py --tamper
%PYTHON_EXE% pipeline\run_pipeline.py --tamper
echo running pipeline\table_generator.py
%PYTHON_EXE% pipeline\table_generator.py
echo running pipeline\generate_diagram.py
%PYTHON_EXE% pipeline\generate_diagram.py
