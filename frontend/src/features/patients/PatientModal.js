import React, { useState } from 'react';
import { patientService } from '../../services/patientService';
import { toast } from 'react-toastify';
import './PatientModal.css';

const PatientModal = ({ onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    tc_identity_number: '',
    birth_date: '',
    address: '',
    notes: '',
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
      await patientService.create(formData);
      toast.success('Hasta başarıyla eklendi');
      onSuccess();
      onClose();
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'Hasta eklenirken hata oluştu'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Yeni Hasta Ekle</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <p className="modal-description">
          Hasta bilgilerini girin ve kaydedin.
        </p>

        <form onSubmit={handleSubmit} className="patient-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">Ad</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                className="form-input"
                value={formData.first_name}
                onChange={handleChange}
                required
                placeholder="Örn: Ahmet"
              />
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Soyad</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                className="form-input"
                value={formData.last_name}
                onChange={handleChange}
                required
                placeholder="Örn: Yılmaz"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phone">Telefon</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                className="form-input"
                value={formData.phone}
                onChange={handleChange}
                required
                placeholder="0532 123 4567"
              />
            </div>

            <div className="form-group">
              <label htmlFor="tc_identity_number">TC Kimlik No</label>
              <input
                type="text"
                id="tc_identity_number"
                name="tc_identity_number"
                className="form-input"
                value={formData.tc_identity_number}
                onChange={handleChange}
                maxLength="11"
                placeholder="12345678901"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="birth_date">Doğum Tarihi</label>
            <input
              type="date"
              id="birth_date"
              name="birth_date"
              className="form-input"
              value={formData.birth_date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="address">Adres</label>
            <textarea
              id="address"
              name="address"
              className="form-input"
              rows="3"
              value={formData.address}
              onChange={handleChange}
              placeholder="Atatürk Mah. Cumhuriyet Cad. No:45 Daire:3 Ankara"
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notlar</label>
            <textarea
              id="notes"
              name="notes"
              className="form-input"
              rows="3"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Alerji, kronik hastalık vb."
            />
          </div>

          <div className="modal-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              İptal
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Kaydediliyor...' : 'Kaydet'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientModal;
