import React, { useState } from 'react';
import { patientService } from '../../services/patientService';
import { formatDate } from '../../utils/helpers';
import { toast } from 'react-toastify';
import './PatientProfile.css';

const PatientProfile = ({ patient, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: patient.first_name,
    last_name: patient.last_name,
    phone: patient.phone,
    tc_identity_number: patient.tc_identity_number || '',
    birth_date: patient.birth_date || '',
    address: patient.address || '',
    notes: patient.notes || '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await patientService.update(patient.id, formData);
      toast.success('Hasta bilgileri güncellendi');
      setIsEditing(false);
      onUpdate();
    } catch (error) {
      toast.error('Güncelleme başarısız');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="patient-profile">
      <div className="profile-section">
        <div className="section-header">
          <h2>Kişisel Bilgiler</h2>
          {!isEditing && (
            <button className="btn btn-primary" onClick={() => setIsEditing(true)}>
              Düzenle
            </button>
          )}
        </div>

        {isEditing ? (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-row">
              <div className="form-group">
                <label>Ad</label>
                <input
                  type="text"
                  name="first_name"
                  className="form-input"
                  value={formData.first_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Soyad</label>
                <input
                  type="text"
                  name="last_name"
                  className="form-input"
                  value={formData.last_name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Telefon</label>
              <input
                type="tel"
                name="phone"
                className="form-input"
                value={formData.phone}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>TC Kimlik No</label>
                <input
                  type="text"
                  name="tc_identity_number"
                  className="form-input"
                  value={formData.tc_identity_number}
                  onChange={handleChange}
                  maxLength="11"
                />
              </div>
              <div className="form-group">
                <label>Doğum Tarihi</label>
                <input
                  type="date"
                  name="birth_date"
                  className="form-input"
                  value={formData.birth_date}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Adres</label>
              <textarea
                name="address"
                className="form-input"
                rows="3"
                value={formData.address}
                onChange={handleChange}
              />
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setIsEditing(false);
                  setFormData({
                    first_name: patient.first_name,
                    last_name: patient.last_name,
                    phone: patient.phone,
                    tc_identity_number: patient.tc_identity_number || '',
                    birth_date: patient.birth_date || '',
                    address: patient.address || '',
                    notes: patient.notes || '',
                  });
                }}
              >
                İptal
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Kaydediliyor...' : 'Kaydet'}
              </button>
            </div>
          </form>
        ) : (
          <div className="profile-info">
            <div className="info-item">
              <span className="info-icon">📞</span>
              <span className="info-label">Telefon:</span>
              <span className="info-value">{patient.phone}</span>
            </div>
            {patient.tc_identity_number && (
              <div className="info-item">
                <span className="info-icon">🆔</span>
                <span className="info-label">TC Kimlik No:</span>
                <span className="info-value">{patient.tc_identity_number}</span>
              </div>
            )}
            {patient.birth_date && (
              <div className="info-item">
                <span className="info-icon">📅</span>
                <span className="info-label">Doğum Tarihi:</span>
                <span className="info-value">{formatDate(patient.birth_date)}</span>
              </div>
            )}
            {patient.address && (
              <div className="info-item">
                <span className="info-icon">📍</span>
                <span className="info-label">Adres:</span>
                <span className="info-value">{patient.address}</span>
              </div>
            )}
          </div>
        )}
      </div>

      {patient.notes && (
        <div className="profile-section">
          <h2>Notlar</h2>
          <div className="notes-box">
            {patient.notes}
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientProfile;
