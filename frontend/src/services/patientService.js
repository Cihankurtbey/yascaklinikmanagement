import api from './api';

export const patientService = {
  getAll: async (params = {}) => {
    const response = await api.get('/patients/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/patients/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/patients/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(`/patients/${id}/`, data);
    return response.data;
  },

  search: async (query) => {
    const response = await api.get('/patients/', {
      params: { search: query },
    });
    return response.data;
  },

  getAnamnesis: async (id) => {
    const response = await api.get(`/patients/${id}/anamnesis/`);
    return response.data;
  },

  updateAnamnesis: async (id, data) => {
    const response = await api.put(`/patients/${id}/anamnesis/`, data);
    return response.data;
  },

  getDocuments: async (id) => {
    const response = await api.get(`/patients/${id}/documents/`);
    return response.data;
  },

  uploadDocument: async (id, file, title, fileType) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('file_type', fileType);

    const response = await api.post(`/patients/${id}/documents/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
