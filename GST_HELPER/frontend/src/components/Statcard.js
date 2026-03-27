export default function StatCard({ title, value}) {
  const cardStyle = {
    background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
    color: 'white',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'pointer'
  };

  const titleStyle = {
    fontSize: '13px',
    opacity: 0.9,
    marginBottom: '8px'
  };

  const valueStyle = {
    fontSize: '28px',
    fontWeight: 'bold'
  };

  const handleHover = (e) => {
    e.currentTarget.style.transform = 'translateY(-4px)';
    e.currentTarget.style.boxShadow = '0 8px 12px rgba(0, 0, 0, 0.15)';
  };

  const handleLeave = (e) => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
  };

  return (
    <div
      style={cardStyle}
      onMouseEnter={handleHover}
      onMouseLeave={handleLeave}
    >
      <div style={titleStyle}>{title}</div>
      <div style={valueStyle}>{value}</div>
    </div>
  );
}