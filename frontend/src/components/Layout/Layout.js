import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../../services/authService';
import './Layout.css';

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const user = authService.getCurrentUser();

  const handleLogout = async () => {
    await authService.logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const getRoleLabel = (role) => {
    const labels = {
      admin: 'Yönetici',
      doctor: 'Diş Hekimi',
      assistant: 'Asistan',
    };
    return labels[role] || role;
  };

  return (
    <div className="layout">
      <header className="layout-header">
        <div className="header-left">
          <div className="logo">
            <div className="logo-circle">Y</div>
            <div className="logo-text">
              <div className="clinic-name">Yaşça Dental Klinik</div>
              <div className="user-role">{getRoleLabel(user?.role)}</div>
            </div>
          </div>
        </div>
        <div className="header-right">
          <button className="logout-btn" onClick={handleLogout}>
            <span>Çıkış</span>
          </button>
        </div>
      </header>

      <nav className="layout-nav">
        <button
          className={`nav-item ${isActive('/') ? 'active' : ''}`}
          onClick={() => navigate('/')}
        >
          <span>🏠</span>
          <span>Ana Sayfa</span>
        </button>
        <button
          className={`nav-item ${isActive('/appointments') ? 'active' : ''}`}
          onClick={() => navigate('/appointments')}
        >
          <span>📅</span>
          <span>Randevular</span>
        </button>
        <button
          className={`nav-item ${isActive('/patients') ? 'active' : ''}`}
          onClick={() => navigate('/patients')}
        >
          <span>👥</span>
          <span>Hastalar</span>
        </button>
      </nav>

      <main className="layout-main">
        {children}
      </main>
    </div>
  );
};

export default Layout;
