import api from './api';

export const appointmentService = {
  getAll: async (params = {}) => {
    const response = await api.get('/appointments/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/appointments/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/appointments/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(`/appointments/${id}/`, data);
    return response.data;
  },

  updateStatus: async (id, status) => {
    const response = await api.patch(`/appointments/${id}/update_status/`, { status });
    return response.data;
  },

  getCalendar: async (view = 'daily', date = null, doctor = null) => {
    const params = { view };
    if (date) params.date = date;
    if (doctor) params.doctor = doctor;

    const response = await api.get('/appointments/calendar/', { params });
    // Backend'den gelen response direkt array olabilir
    return Array.isArray(response.data) ? response.data : (response.data.results || response.data);
  },

  getToday: async () => {
    const response = await api.get('/appointments/', { params: { today: 'true' } });
    return response.data;
  },

  getSettings: async () => {
    const response = await api.get('/appointments/settings/');
    return response.data;
  },

  updateSettings: async (data) => {
    const response = await api.put('/appointments/settings/1/', data);
    return response.data;
  },
};
