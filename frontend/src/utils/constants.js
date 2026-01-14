export const USER_ROLES = {
  ADMIN: 'admin',
  DOCTOR: 'doctor',
  ASSISTANT: 'assistant',
};

export const APPOINTMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  NO_SHOW: 'no_show',
};

export const APPOINTMENT_STATUS_LABELS = {
  [APPOINTMENT_STATUS.PENDING]: 'Bekliyor',
  [APPOINTMENT_STATUS.COMPLETED]: 'Tamamlandı',
  [APPOINTMENT_STATUS.CANCELLED]: 'İptal',
  [APPOINTMENT_STATUS.NO_SHOW]: 'Gelmedi',
};

export const TREATMENT_STATUS = {
  PLANNED: 'planned',
  COMPLETED: 'completed',
};

export const TREATMENT_STATUS_LABELS = {
  [TREATMENT_STATUS.PLANNED]: 'Yapılacak',
  [TREATMENT_STATUS.COMPLETED]: 'Tamamlanmış',
};

// Diş numaraları (FDI notasyonu)
export const PERMANENT_TEETH = {
  upper: {
    right: [18, 17, 16, 15, 14, 13, 12, 11],
    left: [21, 22, 23, 24, 25, 26, 27, 28],
  },
  lower: {
    right: [48, 47, 46, 45, 44, 43, 42, 41],
    left: [31, 32, 33, 34, 35, 36, 37, 38],
  },
};

export const PRIMARY_TEETH = {
  upper: {
    right: [55, 54, 53, 52, 51],
    left: [61, 62, 63, 64, 65],
  },
  lower: {
    right: [85, 84, 83, 82, 81],
    left: [71, 72, 73, 74, 75],
  },
};

export const TREATMENT_COLORS = {
  healthy: '#ffffff',
  filling: '#3b82f6', // blue
  root_canal: '#ef4444', // red
  crown: '#fbbf24', // yellow
  extracted: '#6b7280', // gray
  implant: '#a855f7', // purple
  cleaning: '#10b981', // green
};
