import api from './api';

export const treatmentService = {
  getAll: async (params = {}) => {
    const response = await api.get('/treatments/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/treatments/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/treatments/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(`/treatments/${id}/`, data);
    return response.data;
  },

  getByPatient: async (patientId) => {
    const response = await api.get('/treatments/', { params: { patient: patientId } });
    return response.data;
  },

  getTreatmentTypes: async () => {
    const response = await api.get('/treatments/types/');
    return response.data;
  },

  createTreatmentType: async (data) => {
    const response = await api.post('/treatments/types/', data);
    return response.data;
  },

  updateTreatmentType: async (id, data) => {
    const response = await api.patch(`/treatments/types/${id}/`, data);
    return response.data;
  },

  getOdontogram: async (patientId) => {
    const response = await api.get('/treatments/odontogram/', {
      params: { patient: patientId },
    });
    return response.data;
  },

  updateOdontogram: async (patientId, data) => {
    const response = await api.post('/treatments/odontogram/by_patient/', {
      patient_id: patientId,
      ...data,
    });
    return response.data;
  },
};
