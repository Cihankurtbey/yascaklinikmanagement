import React, { useState, useEffect } from 'react';
import { format, addDays, subDays, startOfWeek, endOfWeek, isSameDay, parseISO } from 'date-fns';
import { tr } from 'date-fns/locale';
import { appointmentService } from '../../services/appointmentService';
import { patientService } from '../../services/patientService';
import { toast } from 'react-toastify';
import { APPOINTMENT_STATUS_LABELS } from '../../utils/constants';
import AppointmentModal from './AppointmentModal';
import './Appointments.css';

const Appointments = () => {
  const [view, setView] = useState('daily'); // 'daily' or 'weekly'
  const [currentDate, setCurrentDate] = useState(new Date());
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [settings, setSettings] = useState({
    start_time: '09:00',
    end_time: '18:00',
    slot_duration: 15,
  });

  useEffect(() => {
    loadSettings();
    loadAppointments();
  }, [view, currentDate]);

  const loadSettings = async () => {
    try {
      const data = await appointmentService.getSettings();
      setSettings(data);
    } catch (error) {
      console.error('Settings load error:', error);
    }
  };

  const loadAppointments = async () => {
    try {
      setLoading(true);
      const dateStr = format(currentDate, 'yyyy-MM-dd');
      const data = await appointmentService.getCalendar(view, dateStr);
      // Backend'den gelen data array veya object olabilir
      const appointmentsList = Array.isArray(data) ? data : (data.results || []);
      console.log('Loaded appointments:', appointmentsList); // Debug
      setAppointments(appointmentsList);
    } catch (error) {
      toast.error('Randevular yüklenirken hata oluştu');
      console.error('Appointment load error:', error);
      setAppointments([]);
    } finally {
      setLoading(false);
    }
  };

  const generateTimeSlots = () => {
    const slots = [];
    const [startHour, startMin] = settings.start_time.split(':').map(Number);
    const [endHour, endMin] = settings.end_time.split(':').map(Number);
    const duration = settings.slot_duration || 15;

    let currentHour = startHour;
    let currentMin = startMin;

    while (
      currentHour < endHour ||
      (currentHour === endHour && currentMin < endMin)
    ) {
      const timeStr = `${String(currentHour).padStart(2, '0')}:${String(currentMin).padStart(2, '0')}`;
      slots.push(timeStr);

      currentMin += duration;
      if (currentMin >= 60) {
        currentHour += 1;
        currentMin = 0;
      }
    }

    return slots;
  };

  const getAppointmentsForSlot = (timeSlot, date) => {
    return appointments.filter((apt) => {
      // Tarih karşılaştırması
      let aptDate;
      if (typeof apt.appointment_date === 'string') {
        // YYYY-MM-DD formatında string ise
        if (apt.appointment_date.includes('T')) {
          aptDate = parseISO(apt.appointment_date);
        } else {
          aptDate = new Date(apt.appointment_date + 'T00:00:00');
        }
      } else {
        aptDate = new Date(apt.appointment_date);
      }
      
      // Zaman karşılaştırması
      let aptTime = apt.appointment_time;
      if (typeof aptTime === 'string') {
        aptTime = aptTime.substring(0, 5); // HH:mm formatına çevir
      } else if (aptTime && aptTime.hours !== undefined) {
        // Time object ise
        aptTime = `${String(aptTime.hours).padStart(2, '0')}:${String(aptTime.minutes).padStart(2, '0')}`;
      }
      
      const dateMatch = isSameDay(aptDate, date);
      const timeMatch = aptTime === timeSlot;
      
      return dateMatch && timeMatch;
    });
  };

  const handleDateChange = (direction) => {
    if (direction === 'prev') {
      setCurrentDate((prev) => subDays(prev, view === 'daily' ? 1 : 7));
    } else if (direction === 'next') {
      setCurrentDate((prev) => addDays(prev, view === 'daily' ? 1 : 7));
    } else {
      setCurrentDate(new Date());
    }
  };

  const handleSlotClick = (timeSlot, date) => {
    const slotAppointments = getAppointmentsForSlot(timeSlot, date);
    if (slotAppointments.length > 0) {
      setSelectedAppointment(slotAppointments[0]);
      setShowModal(true);
    } else {
      setSelectedSlot({ time: timeSlot, date });
      setSelectedAppointment(null);
      setShowModal(true);
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
    setSelectedSlot(null);
    setSelectedAppointment(null);
    loadAppointments();
  };

  const getDateRange = () => {
    if (view === 'daily') {
      return format(currentDate, 'd MMM EEEE', { locale: tr });
    } else {
      const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
      const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });
      return `${format(weekStart, 'd MMM EEE', { locale: tr })} - ${format(weekEnd, 'd MMM EEE', { locale: tr })}`;
    }
  };

  const getWeekDays = () => {
    const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
    const days = [];
    for (let i = 0; i < 7; i++) {
      days.push(addDays(weekStart, i));
    }
    return days;
  };

  const timeSlots = generateTimeSlots();

  if (loading) {
    return (
      <div className="appointments-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="appointments">
      <div className="appointments-header">
        <h1 className="page-title">Randevu Takvimi</h1>
        <div className="view-controls">
          <div className="view-toggle">
            <button
              className={`view-btn ${view === 'daily' ? 'active' : ''}`}
              onClick={() => setView('daily')}
            >
              Günlük
            </button>
            <button
              className={`view-btn ${view === 'weekly' ? 'active' : ''}`}
              onClick={() => setView('weekly')}
            >
              Haftalık
            </button>
          </div>
          <div className="date-navigation">
            <button className="nav-btn" onClick={() => handleDateChange('prev')}>
              ‹
            </button>
            <button className="nav-btn today-btn" onClick={() => handleDateChange('today')}>
              Bugün
            </button>
            <button className="nav-btn" onClick={() => handleDateChange('next')}>
              ›
            </button>
          </div>
        </div>
      </div>

      <div className="current-date-display">{getDateRange()}</div>

      {view === 'daily' ? (
        <div className="daily-view">
          <div className="time-slots">
            {timeSlots.map((timeSlot) => {
              const slotAppointments = getAppointmentsForSlot(timeSlot, currentDate);
              const isEmpty = slotAppointments.length === 0;

              return (
                <div
                  key={timeSlot}
                  className={`time-slot ${isEmpty ? 'empty' : 'filled'}`}
                  onClick={() => handleSlotClick(timeSlot, currentDate)}
                >
                  <div className="slot-time">{timeSlot}</div>
                  <div className="slot-content">
                    {isEmpty ? (
                      <span className="empty-label">Boş</span>
                    ) : (
                      <div className="appointment-item">
                        <div className="appointment-patient">
                          {slotAppointments[0].patient_name || slotAppointments[0].patient_detail?.full_name || 'Hasta'}
                        </div>
                        <div className="appointment-procedure">
                          {slotAppointments[0].procedure || 'Randevu'}
                        </div>
                        <span className={`status-badge status-${slotAppointments[0].status || 'pending'}`}>
                          {APPOINTMENT_STATUS_LABELS[slotAppointments[0].status] || 'Bekliyor'}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="slot-action">+</div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="weekly-view">
          <div className="weekly-grid">
            <div className="time-column">
              <div className="time-header">Saat</div>
              {timeSlots.map((timeSlot) => (
                <div key={timeSlot} className="time-cell">
                  {timeSlot}
                </div>
              ))}
            </div>
            {getWeekDays().map((day, dayIndex) => (
              <div key={dayIndex} className="day-column">
                <div className="day-header">
                  {format(day, 'd MMM EEE', { locale: tr })}
                </div>
                {timeSlots.map((timeSlot) => {
                  const slotAppointments = getAppointmentsForSlot(timeSlot, day);
                  const isEmpty = slotAppointments.length === 0;

                  return (
                    <div
                      key={timeSlot}
                      className={`time-cell ${isEmpty ? 'empty' : 'filled'}`}
                      onClick={() => handleSlotClick(timeSlot, day)}
                    >
                      {!isEmpty && (
                        <div className="appointment-block">
                          <div className="appointment-patient">
                            {slotAppointments[0].patient_name || slotAppointments[0].patient_detail?.full_name || 'Hasta'}
                          </div>
                          <div className="appointment-time">
                            {typeof slotAppointments[0].appointment_time === 'string' 
                              ? slotAppointments[0].appointment_time.substring(0, 5)
                              : timeSlot}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      )}

      {showModal && (
        <AppointmentModal
          appointment={selectedAppointment}
          slot={selectedSlot}
          currentDate={currentDate}
          onClose={handleModalClose}
        />
      )}
    </div>
  );
};

export default Appointments;
