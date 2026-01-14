import React, { useState, useEffect } from 'react';
import { treatmentService } from '../../services/treatmentService';
import { formatDate, formatDateTime } from '../../utils/helpers';
import { TREATMENT_STATUS_LABELS } from '../../utils/constants';
import { toast } from 'react-toastify';
import './PatientTreatments.css';

const PatientTreatments = ({ patientId }) => {
  const [treatments, setTreatments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTreatments();
  }, [patientId]);

  const loadTreatments = async () => {
    try {
      setLoading(true);
      const data = await treatmentService.getByPatient(patientId);
      setTreatments(data.results || data);
    } catch (error) {
      toast.error('Tedavi geçmişi yüklenirken hata oluştu');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="treatments-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="patient-treatments">
      <h2>Tedavi Geçmişi</h2>
      {treatments.length === 0 ? (
        <div className="empty-state">
          Bu hasta için henüz tedavi kaydı bulunmamaktadır.
        </div>
      ) : (
        <div className="treatments-list">
          {treatments.map((treatment) => (
            <div key={treatment.id} className="treatment-card">
              <div className="treatment-icon">📅</div>
              <div className="treatment-content">
                <div className="treatment-header">
                  <h3 className="treatment-type">
                    {treatment.treatment_type_name || treatment.treatment_type_detail?.name || 'Tedavi'}
                  </h3>
                  {treatment.tooth_number && (
                    <span className="tooth-number">Diş: {treatment.tooth_number}</span>
                  )}
                </div>
                <div className="treatment-meta">
                  {formatDate(treatment.treatment_date)} • {treatment.doctor_name || treatment.doctor_detail?.full_name || 'Doktor'}
                </div>
                <div className="treatment-description">
                  {treatment.description}
                </div>
                <div className="treatment-status">
                  <span className={`status-badge status-${treatment.status}`}>
                    {TREATMENT_STATUS_LABELS[treatment.status]}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PatientTreatments;
