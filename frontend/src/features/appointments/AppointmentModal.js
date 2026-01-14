import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { appointmentService } from '../../services/appointmentService';
import { patientService } from '../../services/patientService';
import { toast } from 'react-toastify';
import { APPOINTMENT_STATUS } from '../../utils/constants';
import './AppointmentModal.css';

const AppointmentModal = ({ appointment, slot, currentDate, onClose }) => {
  const [formData, setFormData] = useState({
    patient: '',
    appointment_date: slot
      ? format(slot.date, 'yyyy-MM-dd')
      : format(currentDate, 'yyyy-MM-dd'),
    appointment_time: slot ? slot.time : '',
    procedure: '',
    notes: '',
    status: APPOINTMENT_STATUS.PENDING,
  });
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (appointment) {
      setFormData({
        patient: appointment.patient || appointment.patient_detail?.id || '',
        appointment_date: appointment.appointment_date,
        appointment_time: appointment.appointment_time.substring(0, 5),
        procedure: appointment.procedure || '',
        notes: appointment.notes || '',
        status: appointment.status,
      });
    }
    loadPatients();
  }, [appointment]);

  const loadPatients = async () => {
    try {
      const data = await patientService.getAll();
      setPatients(data.results || data);
    } catch (error) {
      console.error('Patients load error:', error);
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
    setLoading(true);

    try {
      if (appointment) {
        // Güncelleme
        await appointmentService.update(appointment.id, formData);
        toast.success('Randevu güncellendi');
      } else {
        // Yeni randevu
        // Doctor ID'yi ekle (şimdilik ilk doktoru al, production'da kullanıcıdan alınmalı)
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const appointmentData = {
          ...formData,
          doctor: user.role === 'doctor' ? user.id : 1, // Eğer doktor ise kendi ID'si, değilse ilk doktor
        };
        await appointmentService.create(appointmentData);
        toast.success('Randevu oluşturuldu');
      }
      onClose();
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'Randevu kaydedilirken hata oluştu'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!appointment || !window.confirm('Bu randevuyu silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      await appointmentService.update(appointment.id, { status: APPOINTMENT_STATUS.CANCELLED });
      toast.success('Randevu iptal edildi');
      onClose();
    } catch (error) {
      toast.error('Randevu silinirken hata oluştu');
    }
  };

  const filteredPatients = patients.filter((p) => {
    const fullName = `${p.first_name} ${p.last_name}`.toLowerCase();
    const query = searchQuery.toLowerCase();
    return fullName.includes(query) || p.phone?.includes(query);
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{appointment ? 'Randevu Düzenle' : 'Yeni Randevu Ekle'}</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <p className="modal-description">
          {appointment
            ? 'Randevu bilgilerini düzenleyin.'
            : 'Randevu bilgilerini girin ve kaydedin.'}
        </p>

        <form onSubmit={handleSubmit} className="appointment-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="appointment_date">Tarih</label>
              <input
                type="date"
                id="appointment_date"
                name="appointment_date"
                className="form-input"
                value={formData.appointment_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="appointment_time">Saat</label>
              <input
                type="time"
                id="appointment_time"
                name="appointment_time"
                className="form-input"
                value={formData.appointment_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="patient">Hasta Adı Soyadı</label>
            <input
              type="text"
              id="patient_search"
              className="form-input"
              placeholder="Hasta ara..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setSearchQuery('')}
            />
            {searchQuery && filteredPatients.length > 0 && (
              <div className="patient-dropdown">
                {filteredPatients.slice(0, 5).map((patient) => (
                  <div
                    key={patient.id}
                    className="patient-option"
                    onClick={() => {
                      setFormData({ ...formData, patient: patient.id });
                      setSearchQuery(`${patient.first_name} ${patient.last_name}`);
                    }}
                  >
                    {patient.first_name} {patient.last_name} - {patient.phone}
                  </div>
                ))}
              </div>
            )}
            <select
              id="patient"
              name="patient"
              className="form-input"
              value={formData.patient}
              onChange={handleChange}
              required
            >
              <option value="">Hasta Seçin</option>
              {patients.map((patient) => (
                <option key={patient.id} value={patient.id}>
                  {patient.first_name} {patient.last_name} - {patient.phone}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="procedure">İşlem</label>
            <input
              type="text"
              id="procedure"
              name="procedure"
              className="form-input"
              placeholder="Örn: Dolgu, Kanal Tedavisi"
              value={formData.procedure}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notlar</label>
            <textarea
              id="notes"
              name="notes"
              className="form-input"
              rows="3"
              placeholder="Ek bilgiler..."
              value={formData.notes}
              onChange={handleChange}
            />
          </div>

          {appointment && (
            <div className="form-group">
              <label htmlFor="status">Durum</label>
              <select
                id="status"
                name="status"
                className="form-input"
                value={formData.status}
                onChange={handleChange}
              >
                <option value={APPOINTMENT_STATUS.PENDING}>Bekliyor</option>
                <option value={APPOINTMENT_STATUS.COMPLETED}>Tamamlandı</option>
                <option value={APPOINTMENT_STATUS.CANCELLED}>İptal</option>
                <option value={APPOINTMENT_STATUS.NO_SHOW}>Gelmedi</option>
              </select>
            </div>
          )}

          <div className="modal-actions">
            {appointment && (
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleDelete}
              >
                İptal Et
              </button>
            )}
            <div className="action-buttons">
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
          </div>
        </form>
      </div>
    </div>
  );
};

export default AppointmentModal;
