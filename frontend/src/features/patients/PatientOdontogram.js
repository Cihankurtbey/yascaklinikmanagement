import React, { useState, useEffect } from 'react';
import { treatmentService } from '../../services/treatmentService';
import { toast } from 'react-toastify';
import './PatientOdontogram.css';

const PatientOdontogram = ({ patientId }) => {
  const [toothType, setToothType] = useState('permanent'); // 'permanent' or 'primary'
  const [odontogram, setOdontogram] = useState(null);
  const [loading, setLoading] = useState(true);
  const [treatmentTypes, setTreatmentTypes] = useState([]);
  const [selectedTooth, setSelectedTooth] = useState(null);

  useEffect(() => {
    loadOdontogram();
    loadTreatmentTypes();
  }, [patientId, toothType]);

  const loadOdontogram = async () => {
    try {
      setLoading(true);
      const data = await treatmentService.getOdontogram(patientId);
      setOdontogram(data.results?.[0] || data);
    } catch (error) {
      console.error('Odontogram load error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTreatmentTypes = async () => {
    try {
      const data = await treatmentService.getTreatmentTypes();
      setTreatmentTypes(data.results || data);
    } catch (error) {
      console.error('Treatment types load error:', error);
    }
  };

  const handleToothClick = (toothNumber) => {
    setSelectedTooth(toothNumber);
  };

  const getToothStatus = (toothNumber) => {
    if (!odontogram) return 'healthy';
    const teeth = toothType === 'primary' 
      ? odontogram.primary_teeth 
      : odontogram.permanent_teeth;
    
    if (!teeth || !teeth[toothNumber] || teeth[toothNumber].length === 0) {
      return 'healthy';
    }
    
    // Son tedaviyi al
    const lastTreatment = teeth[toothNumber][teeth[toothNumber].length - 1];
    return lastTreatment.treatment_type || 'healthy';
  };

  const getToothColor = (status) => {
    const colors = {
      healthy: '#ffffff',
      'Dolgu': '#3b82f6',
      'Kanal Tedavisi': '#ef4444',
      'Kron': '#fbbf24',
      'Çekildi': '#6b7280',
      'İmplant': '#a855f7',
      'Detartraj': '#10b981',
    };
    return colors[status] || colors.healthy;
  };

  // Olgun dişler (FDI notasyonu)
  const permanentTeeth = {
    upper: { right: [18, 17, 16, 15, 14, 13, 12, 11], left: [21, 22, 23, 24, 25, 26, 27, 28] },
    lower: { right: [48, 47, 46, 45, 44, 43, 42, 41], left: [31, 32, 33, 34, 35, 36, 37, 38] },
  };

  // Süt dişleri (FDI notasyonu)
  const primaryTeeth = {
    upper: { right: [55, 54, 53, 52, 51], left: [61, 62, 63, 64, 65] },
    lower: { right: [85, 84, 83, 82, 81], left: [71, 72, 73, 74, 75] },
  };

  const teeth = toothType === 'primary' ? primaryTeeth : permanentTeeth;

  if (loading) {
    return (
      <div className="odontogram-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="patient-odontogram">
      <div className="odontogram-header">
        <h2>Diş Şeması (Odontogram)</h2>
        <p className="instruction">Dişlere tıklayarak işlem ekleyebilirsiniz</p>
      </div>

      <div className="tooth-type-toggle">
        <button
          className={`toggle-btn ${toothType === 'permanent' ? 'active' : ''}`}
          onClick={() => setToothType('permanent')}
        >
          Olgun Dişler
        </button>
        <button
          className={`toggle-btn ${toothType === 'primary' ? 'active' : ''}`}
          onClick={() => setToothType('primary')}
        >
          Süt Dişleri
        </button>
      </div>

      <div className="odontogram-container">
        {/* Üst Çene */}
        <div className="jaw-section">
          <div className="jaw-label">Üst Çene</div>
          <div className="teeth-row">
            {teeth.upper.right.map((tooth) => {
              const status = getToothStatus(tooth.toString());
              return (
                <div
                  key={tooth}
                  className="tooth-box"
                  style={{ borderColor: getToothColor(status) }}
                  onClick={() => handleToothClick(tooth)}
                >
                  <div className="tooth-number">{tooth}</div>
                  <div className="tooth-status">{status === 'healthy' ? '0' : '1'}</div>
                </div>
              );
            })}
            {teeth.upper.left.map((tooth) => {
              const status = getToothStatus(tooth.toString());
              return (
                <div
                  key={tooth}
                  className="tooth-box"
                  style={{ borderColor: getToothColor(status) }}
                  onClick={() => handleToothClick(tooth)}
                >
                  <div className="tooth-number">{tooth}</div>
                  <div className="tooth-status">{status === 'healthy' ? '0' : '1'}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Alt Çene */}
        <div className="jaw-section">
          <div className="jaw-label">Alt Çene</div>
          <div className="teeth-row">
            {teeth.lower.right.map((tooth) => {
              const status = getToothStatus(tooth.toString());
              return (
                <div
                  key={tooth}
                  className="tooth-box"
                  style={{ borderColor: getToothColor(status) }}
                  onClick={() => handleToothClick(tooth)}
                >
                  <div className="tooth-number">{tooth}</div>
                  <div className="tooth-status">{status === 'healthy' ? '0' : '1'}</div>
                </div>
              );
            })}
            {teeth.lower.left.map((tooth) => {
              const status = getToothStatus(tooth.toString());
              return (
                <div
                  key={tooth}
                  className="tooth-box"
                  style={{ borderColor: getToothColor(status) }}
                  onClick={() => handleToothClick(tooth)}
                >
                  <div className="tooth-number">{tooth}</div>
                  <div className="tooth-status">{status === 'healthy' ? '0' : '1'}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {selectedTooth && (
        <div className="tooth-selection">
          <h3>Diş {selectedTooth} - İşlem Seç</h3>
          <select className="treatment-select">
            <option>Sağlıklı</option>
            {treatmentTypes.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#ffffff' }}></div>
          <span>Sağlıklı</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#3b82f6' }}></div>
          <span>Dolgu</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
          <span>Kanal Tedavisi</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#fbbf24' }}></div>
          <span>Kron</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#6b7280' }}></div>
          <span>Çekildi</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#a855f7' }}></div>
          <span>İmplant</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#10b981' }}></div>
          <span>Detartraj</span>
        </div>
      </div>
    </div>
  );
};

export default PatientOdontogram;
