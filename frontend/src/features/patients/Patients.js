import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { patientService } from '../../services/patientService';
import { formatDate } from '../../utils/helpers';
import { toast } from 'react-toastify';
import PatientModal from './PatientModal';
import './Patients.css';

const Patients = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      setLoading(true);
      const data = await patientService.getAll();
      setPatients(data.results || data);
    } catch (error) {
      toast.error('Hastalar yüklenirken hata oluştu');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      loadPatients();
      return;
    }

    try {
      setLoading(true);
      const data = await patientService.search(searchQuery);
      setPatients(data.results || data);
    } catch (error) {
      toast.error('Arama yapılırken hata oluştu');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="patients-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="patients">
      <div className="patients-header">
        <h1 className="page-title">Hasta Yönetimi</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowModal(true)}
        >
          + Yeni Hasta Ekle
        </button>
      </div>

      <div className="patients-search">
        <form onSubmit={handleSearch} className="search-form">
          <label htmlFor="search" className="search-label">
            Hasta Ara
          </label>
          <div className="search-input-wrapper">
            <input
              type="text"
              id="search"
              className="search-input"
              placeholder="Ad, soyad veya telefon ile ara..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-button">
              🔍
            </button>
          </div>
        </form>
      </div>

      <div className="patients-table-container">
        <table className="patients-table">
          <thead>
            <tr>
              <th>Ad Soyad</th>
              <th>Telefon</th>
              <th>TC Kimlik No</th>
              <th>Son Ziyaret</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {patients.length === 0 ? (
              <tr>
                <td colSpan="5" className="empty-row">
                  Hasta bulunamadı
                </td>
              </tr>
            ) : (
              patients.map((patient) => (
                <tr key={patient.id}>
                  <td>{patient.full_name || `${patient.first_name} ${patient.last_name}`}</td>
                  <td>📞 {patient.phone}</td>
                  <td>{patient.tc_identity_number || '-'}</td>
                  <td>
                    {patient.last_visit
                      ? formatDate(patient.last_visit)
                      : '-'}
                  </td>
                  <td>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => navigate(`/patients/${patient.id}`)}
                    >
                      Detay
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <PatientModal
          onClose={() => setShowModal(false)}
          onSuccess={loadPatients}
        />
      )}
    </div>
  );
};

export default Patients;
