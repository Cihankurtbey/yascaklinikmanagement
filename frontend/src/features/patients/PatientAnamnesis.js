import React, { useState, useEffect } from 'react';
import { patientService } from '../../services/patientService';
import { toast } from 'react-toastify';
import './PatientAnamnesis.css';

const PatientAnamnesis = ({ patient, onUpdate }) => {
  const [anamnesis, setAnamnesis] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    medical_history: '',
    allergies: '',
    medications: '',
    chronic_diseases: '',
    past_surgeries: '',
    family_history: '',
    smoking: '',
    alcohol: '',
    pregnancy_status: '',
    other_notes: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadAnamnesis();
  }, [patient.id]);

  const loadAnamnesis = async () => {
    try {
      setLoading(true);
      const data = await patientService.getAnamnesis(patient.id);
      setAnamnesis(data);
      if (data) {
        setFormData({
          medical_history: data.medical_history || '',
          allergies: data.allergies || '',
          medications: data.medications || '',
          chronic_diseases: data.chronic_diseases || '',
          past_surgeries: data.past_surgeries || '',
          family_history: data.family_history || '',
          smoking: data.smoking || '',
          alcohol: data.alcohol || '',
          pregnancy_status: data.pregnancy_status || '',
          other_notes: data.other_notes || '',
        });
      }
    } catch (error) {
      console.error('Anamnesis load error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      await patientService.updateAnamnesis(patient.id, formData);
      toast.success('Anamnez güncellendi');
      setIsEditing(false);
      loadAnamnesis();
      onUpdate();
    } catch (error) {
      toast.error('Güncelleme başarısız');
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Yükleniyor...</div>;
  }

  return (
    <div className="patient-anamnesis">
      <div className="section-header">
        <h2>Hasta Anamnezi</h2>
        <button
          className="btn btn-primary"
          onClick={() => setIsEditing(!isEditing)}
        >
          {isEditing ? 'İptal' : 'Anamnezi Düzenle'}
        </button>
      </div>

      {isEditing ? (
        <form onSubmit={handleSubmit} className="anamnesis-form">
          <div className="form-columns">
            <div className="form-column">
              <div className="form-group">
                <label>Tıbbi Geçmiş</label>
                <textarea
                  name="medical_history"
                  className="form-input"
                  rows="3"
                  value={formData.medical_history}
                  onChange={handleChange}
                  placeholder="Örn: Hipertansiyon tedavisi görüyor"
                />
              </div>

              <div className="form-group">
                <label className="allergy-label">
                  Alerjiler <span className="warning-icon">⚠️</span>
                </label>
                <input
                  type="text"
                  name="allergies"
                  className="form-input allergy-input"
                  value={formData.allergies}
                  onChange={handleChange}
                  placeholder="Örn: Penisilin"
                />
              </div>

              <div className="form-group">
                <label>Kullandığı İlaçlar</label>
                <textarea
                  name="medications"
                  className="form-input"
                  rows="2"
                  value={formData.medications}
                  onChange={handleChange}
                  placeholder="Örn: Ramipril 5mg (günde 1 kez)"
                />
              </div>

              <div className="form-group">
                <label>Kronik Hastalıklar</label>
                <input
                  type="text"
                  name="chronic_diseases"
                  className="form-input"
                  value={formData.chronic_diseases}
                  onChange={handleChange}
                  placeholder="Örn: Hipertansiyon"
                />
              </div>

              <div className="form-group">
                <label>Geçirdiği Ameliyatlar</label>
                <input
                  type="text"
                  name="past_surgeries"
                  className="form-input"
                  value={formData.past_surgeries}
                  onChange={handleChange}
                  placeholder="Örn: Apandisit (2010)"
                />
              </div>
            </div>

            <div className="form-column">
              <div className="form-group">
                <label>Aile Öyküsü</label>
                <input
                  type="text"
                  name="family_history"
                  className="form-input"
                  value={formData.family_history}
                  onChange={handleChange}
                  placeholder="Örn: Annede diyabet"
                />
              </div>

              <div className="form-group">
                <label>Sigara Kullanımı</label>
                <input
                  type="text"
                  name="smoking"
                  className="form-input"
                  value={formData.smoking}
                  onChange={handleChange}
                  placeholder="Örn: Evet, günde 10 adet"
                />
              </div>

              <div className="form-group">
                <label>Alkol Kullanımı</label>
                <input
                  type="text"
                  name="alcohol"
                  className="form-input"
                  value={formData.alcohol}
                  onChange={handleChange}
                  placeholder="Örn: Hayır"
                />
              </div>

              <div className="form-group">
                <label>Gebelik Durumu</label>
                <input
                  type="text"
                  name="pregnancy_status"
                  className="form-input"
                  value={formData.pregnancy_status}
                  onChange={handleChange}
                  placeholder="Örn: Uygulanmaz"
                />
              </div>

              <div className="form-group">
                <label>Diğer Notlar</label>
                <textarea
                  name="other_notes"
                  className="form-input notes-input"
                  rows="4"
                  value={formData.other_notes}
                  onChange={handleChange}
                  placeholder="Örn: Dental anksiyetesi var, işlemler öncesi bilgilendirme yapılmalı"
                />
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setIsEditing(false);
                loadAnamnesis();
              }}
            >
              İptal
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Kaydediliyor...' : 'Kaydet'}
            </button>
          </div>
        </form>
      ) : (
        <div className="anamnesis-display">
          <div className="display-columns">
            <div className="display-column">
              <div className="display-item">
                <label>Tıbbi Geçmiş</label>
                <div className="display-value">
                  {anamnesis?.medical_history || '-'}
                </div>
              </div>

              <div className="display-item">
                <label className="allergy-label">
                  Alerjiler <span className="warning-icon">⚠️</span>
                </label>
                <div className={`display-value ${anamnesis?.allergies ? 'allergy-warning' : ''}`}>
                  {anamnesis?.allergies || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Kullandığı İlaçlar</label>
                <div className="display-value">
                  {anamnesis?.medications || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Kronik Hastalıklar</label>
                <div className="display-value">
                  {anamnesis?.chronic_diseases || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Geçirdiği Ameliyatlar</label>
                <div className="display-value">
                  {anamnesis?.past_surgeries || '-'}
                </div>
              </div>
            </div>

            <div className="display-column">
              <div className="display-item">
                <label>Aile Öyküsü</label>
                <div className="display-value">
                  {anamnesis?.family_history || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Sigara Kullanımı</label>
                <div className="display-value">
                  {anamnesis?.smoking || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Alkol Kullanımı</label>
                <div className="display-value">
                  {anamnesis?.alcohol || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Gebelik Durumu</label>
                <div className="display-value">
                  {anamnesis?.pregnancy_status || '-'}
                </div>
              </div>

              <div className="display-item">
                <label>Diğer Notlar</label>
                <div className="display-value notes-value">
                  {anamnesis?.other_notes || '-'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientAnamnesis;
