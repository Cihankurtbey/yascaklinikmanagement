import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { patientService } from '../../services/patientService';
import { treatmentService } from '../../services/treatmentService';
import { formatDate } from '../../utils/helpers';
import { toast } from 'react-toastify';
import PatientProfile from './PatientProfile';
import PatientAnamnesis from './PatientAnamnesis';
import PatientTreatments from './PatientTreatments';
import PatientOdontogram from './PatientOdontogram';
import './PatientDetail.css';

const PatientDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatient();
  }, [id]);

  const loadPatient = async () => {
    try {
      setLoading(true);
      const data = await patientService.getById(id);
      setPatient(data);
    } catch (error) {
      toast.error('Hasta bilgileri yüklenirken hata oluştu');
      console.error(error);
      navigate('/patients');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="patient-detail-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="patient-detail-error">
        <p>Hasta bulunamadı</p>
        <button className="btn btn-primary" onClick={() => navigate('/patients')}>
          Geri Dön
        </button>
      </div>
    );
  }

  const tabs = [
    { id: 'profile', label: 'Profil Bilgileri' },
    { id: 'anamnesis', label: 'Anamnez' },
    { id: 'treatments', label: 'Tedavi Geçmişi' },
    { id: 'odontogram', label: 'Diş Şeması' },
  ];

  return (
    <div className="patient-detail">
      <div className="patient-header">
        <button className="back-btn" onClick={() => navigate('/patients')}>
          ← Geri
        </button>
        <div className="patient-info">
          <h1 className="patient-name">{patient.full_name || `${patient.first_name} ${patient.last_name}`}</h1>
          <div className="patient-id">Hasta ID: #{patient.id}</div>
        </div>
      </div>

      <div className="patient-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="patient-content">
        {activeTab === 'profile' && (
          <PatientProfile patient={patient} onUpdate={loadPatient} />
        )}
        {activeTab === 'anamnesis' && (
          <PatientAnamnesis patient={patient} onUpdate={loadPatient} />
        )}
        {activeTab === 'treatments' && (
          <PatientTreatments patientId={patient.id} />
        )}
        {activeTab === 'odontogram' && (
          <PatientOdontogram patientId={patient.id} />
        )}
      </div>
    </div>
  );
};

export default PatientDetail;
