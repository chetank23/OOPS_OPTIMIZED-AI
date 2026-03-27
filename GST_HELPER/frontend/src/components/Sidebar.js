export default function Sidebar({ setPage }) {
  const sidebarStyle = {
    width: '250px',
    height: '100vh',
    background: '#1e293b',
    color: 'white',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    borderRight: '1px solid #334155'
  };

  const logoStyle = {
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '30px',
    color: '#60a5fa'
  };

  const navStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px'
  };

  const buttonStyle = {
    background: 'transparent',
    color: 'white',
    padding: '12px 16px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    textAlign: 'left',
    transition: 'all 0.2s',
    borderLeft: '3px solid transparent'
  };

  const handleButtonHover = (e) => {
    e.target.style.background = '#334155';
    e.target.style.borderLeft = '3px solid #60a5fa';
  };

  const handleButtonLeave = (e) => {
    e.target.style.background = 'transparent';
    e.target.style.borderLeft = '3px solid transparent';
  };

  return (
    <div style={sidebarStyle}>
      <div style={logoStyle}>📊 GST Helper</div>
      <nav style={navStyle}>
        <button
          onClick={() => setPage("dashboard")}
          style={buttonStyle}
          onMouseEnter={handleButtonHover}
          onMouseLeave={handleButtonLeave}
        >
          📈 Dashboard
        </button>
        <button
          onClick={() => setPage("upload")}
          style={buttonStyle}
          onMouseEnter={handleButtonHover}
          onMouseLeave={handleButtonLeave}
        >
          📤 Upload
        </button>
      </nav>
    </div>
  );
}