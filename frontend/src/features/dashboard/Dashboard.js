import React, { useState, useEffect } from 'react';
import { appointmentService } from '../../services/appointmentService';
import { patientService } from '../../services/patientService';
import { formatTime } from '../../utils/helpers';
import { APPOINTMENT_STATUS_LABELS } from '../../utils/constants';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    todayAppointments: 0,
    completedAppointments: 0,
    waitingPatients: 0,
    totalPatients: 0,
  });
  const [todayAppointments, setTodayAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Bugünün randevuları
      const appointments = await appointmentService.getToday();
      const completed = appointments.filter(a => a.status === 'completed').length;
      
      // Toplam hasta sayısı
      const patients = await patientService.getAll();
      
      setStats({
        todayAppointments: appointments.length,
        completedAppointments: completed,
        waitingPatients: appointments.filter(a => a.status === 'pending').length,
        totalPatients: patients.length,
      });
      
      setTodayAppointments(appointments);
    } catch (error) {
      console.error('Dashboard data load error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Hoş Geldiniz</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <div className="stat-number">{stats.todayAppointments}</div>
            <div className="stat-label">Bugünkü Randevular</div>
            <div className="stat-sublabel">
              {stats.completedAppointments} tamamlandı
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-number">{stats.waitingPatients}</div>
            <div className="stat-label">Bekleyen Hastalar</div>
            <div className="stat-sublabel">Bugün için</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✓</div>
          <div className="stat-content">
            <div className="stat-number">{stats.totalPatients}</div>
            <div className="stat-label">Toplam Hasta</div>
            <div className="stat-sublabel">Aktif kayıtlar</div>
          </div>
        </div>
      </div>

      <div className="today-appointments">
        <h2 className="section-title">Bugünün Randevuları</h2>
        <div className="appointments-list">
          {todayAppointments.length === 0 ? (
            <div className="empty-state">Bugün için randevu bulunmamaktadır.</div>
          ) : (
            todayAppointments.map((appointment) => (
              <div key={appointment.id} className="appointment-card">
                <div className="appointment-time">
                  <span className="time-icon">🕐</span>
                  <span>{formatTime(appointment.appointment_time)}</span>
                </div>
                <div className="appointment-info">
                  <div className="appointment-patient">
                    {appointment.patient_name}
                  </div>
                  <div className="appointment-procedure">
                    {appointment.procedure || 'Randevu'}
                  </div>
                </div>
                <div className="appointment-status">
                  <span
                    className={`status-badge status-${appointment.status}`}
                  >
                    {APPOINTMENT_STATUS_LABELS[appointment.status]}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
